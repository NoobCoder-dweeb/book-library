from django.core.management.base import BaseCommand, CommandError, CommandParser
from app.models import Book
import os
import re
import pandas as pd

class Command(BaseCommand):
    help = "Import book data from file into the database"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("file_path", type=str, nargs="+", default="../../dataset/main_dataset.csv")

    def collect_from_csv(self, file_path):
        """
        Collects data from a CSV file and returns a cleaned DataFrame.
        
        Args:
            file_path (str): The path to the CSV file.
        Returns:
            pd.DataFrame: A DataFrame containing the cleaned data.
        """
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        
        df = pd.read_csv(file_path)

        # Clean up the DataFrame
        df.drop(columns=["image", 'format', "old_price"], axis=1, inplace=True, errors='ignore')
        df.rename(columns={"name": "title", "img_paths": "cover_image", "book_depository_stars": "rating"}, inplace=True)
        str_case = r"[^\d.]+" # Regex to match non-numeric characters except for dot
        df["price"]=df["price"].apply(lambda x: re.sub(str_case, "", str(x)) if re.search(str_case, str(x)) else str(x))
        df["cover_image"] = df["cover_image"].apply(lambda x: str(x).replace("dataset/", ""))

        # apply data types
        df["price"] = df["price"].astype("float64")
        df["category"] = df["category"].astype("category")

        return df

    def handle(self, *args, **kwargs)-> None:
        file_path = kwargs["file_path"]
        if not file_path:
            raise CommandError("File path is required.")
        
        if isinstance(file_path, list):
            file_path = file_path[0]
        
        if not os.path.exists(file_path):
            raise CommandError(f"The file {file_path} does not exist.")
        
        df = self.collect_from_csv(file_path)

        for _, row in df.iterrows():
            book = Book(
                title=row["title"],
                author=row["author"],
                category=row["category"] if "category" in row else None,
                price = row["price"],
                isbn=row["isbn"],
                cover_image=row["cover_image"] if "cover_image" in row else None,
                rating=row["rating"] if "rating" in row else 0.0,
            )

            book.save()

        self.stdout.write(self.style.SUCCESS("Data imported successfully."))
