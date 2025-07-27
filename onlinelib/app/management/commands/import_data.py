from django.core.management.base import BaseCommand, CommandError, CommandParser
from app.models import Book
import os
import re
import pandas as pd

class Command(BaseCommand):
    help = "Import book data from file into the database"

    def add_arguments(self, parser: CommandParser) -> None:
        # parser.add_argument("file_path", type=str, nargs="+", default="../../dataset/main_dataset.csv")
        parser.add_argument("--book", type=str, nargs="+")
        parser.add_argument("--rating", type=str, nargs="+")
        parser.add_argument("--file-path", type=str, nargs="?")

    def collect_from_csv(self, book_file: str, rating_file: str) -> pd.DataFrame:
        """
        Collects data from a CSV file and returns a cleaned DataFrame.
        
        Args:
            file_path (str): The path to the CSV file.
        Returns:
            pd.DataFrame: A DataFrame containing the cleaned data.
        """
        if not os.path.exists(book_file):
            raise FileNotFoundError(f"The file {book_file} does not exist.")
        if not os.path.exists(rating_file):
            raise FileNotFoundError(f"The file {rating_file} does not exist.")
        
        # Load the datasets
        books = pd.read_csv(book_file, sep=';', encoding="ISO-8859-1", on_bad_lines="warn")
        ratings = pd.read_csv(rating_file, sep=";", encoding="ISO-8859-1", on_bad_lines="warn")

        # Convert columns to appropriate data types
        books["Year-Of-Publication"] = pd.to_numeric(books["Year-Of-Publication"], errors='coerce')
        books["Year-Of-Publication"] = books["Year-Of-Publication"].fillna(books["Year-Of-Publication"].mode()[0]).astype(int)

        ratings["Book-Rating"] = pd.to_numeric(ratings["Book-Rating"], errors='coerce')
        ratings["Book-Rating"] = ratings["Book-Rating"].fillna(ratings["Book-Rating"].mean())

        # Merge the datasets on ISBN
        df = pd.merge(books, ratings, left_on="ISBN", right_on="ISBN", how="inner")

        # drop unnecessary columns
        df.drop(columns=["Image-URL-L"], inplace=True, errors='ignore')

        # aggregate the data
        aggregated_df = df. \
            groupby(['ISBN', 'Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher', 
       'Image-URL-S', 'Image-URL-M']).agg({"Book-Rating":"mean"}).   \
        reset_index().rename(columns={"Book-Rating":"Avg_Rating"})
        
        # Rename columns for clarity
        new_columns = {
            "ISBN": "isbn",
            "Book-Title": "title",
            "Book-Author": "author",
            "Year-Of-Publication": "year",
            "Publisher": "publisher",
            "Image-URL-S": "image_url_s",
            "Image-URL-M": "image_url_m",
            "Avg_Rating": "ratings",
        }

        aggregated_df.rename(columns=new_columns, inplace=True)
        aggregated_df["ratings"] = aggregated_df["ratings"].round(2)    

        return aggregated_df

    def handle(self, *args, **kwargs)-> None:
        book_file = kwargs["book"][0]
        rating_file = kwargs["rating"][0]
        cleaned = kwargs.get("file_path", None)

        if cleaned:
            df = pd.read_csv("app/dataset/cleaned.csv")
        
        else:
            if not book_file or not rating_file:
                raise CommandError("Please provide both book and rating files.")

            df = self.collect_from_csv(book_file=book_file, rating_file=rating_file)

        for _, row in df.iterrows():
            book = Book(
                title=row["title"],
                author=row["author"],
                year=row["year"],
                publisher=row["publisher"],
                isbn=row["isbn"],
                image_url_s=row["image_url_s"],
                image_url_m=row["image_url_m"],
                rating=row["ratings"],
            )

            book.save()

        # TODO: Check the dataset
        df.to_csv("app/dataset/cleaned.csv", index=False)

        self.stdout.write(self.style.SUCCESS("Data imported successfully."))
