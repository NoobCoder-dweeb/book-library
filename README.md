# 📚 Book Library

Book Library is a web-based AI-powered application that can **summarize large amounts of content from uploaded files** and present the summaries in an intuitive interface.  
It leverages **LangFlow** to build and integrate the AI agent into the Django backend.

---

## 🚀 Tech Stack
- **Backend:** [Django](https://www.djangoproject.com/)
- **Dependency Management:** [UV](https://github.com/astral-sh/uv)
- **Database:** SQLite
- **AI Workflow Builder:** [LangFlow](https://www.langflow.org/)

---

## 📦 Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

### 2️⃣ Install UV
Follow the official [UV](https://github.com/astral-sh/uv) installation guide for your operating system.

### 3️⃣ Install Python 3.10 and Pin It
```bash
uv python install 3.10
uv python pin 3.10
```

### 4️⃣ Create and Activate Virtual Environment
```bash
uv venv .venv
source .venv/bin/activate
```

### 5️⃣ Install Dependencies
```bash
uv pip install -r requirements.txt
```

### 6️⃣ Run Database Migrations
```bash
cd onlinelib
python manage.py makemigrations
python manage.py migrate
```
### 7️⃣ Import Initial Data
```bash
 python manage.py import_data --book="app/dataset/books.csv" --rating="app/dataset/ratings.csv"
```

### 8️⃣ Test LangFlow Installation
```bash
langflow run
```
!!!⚠️ If errors occur, resolve them before proceeding.

### 9️⃣ Run the Django Application

```bash
cd onlinelib
python manage.py runserver
```

## 
🗂 Project Structure
```bash
BookLibrary/
├── onlinelib/           # Main Django app
├── requirements.txt     # Project dependencies
├── env.example          # Example environment variables
└── README.md            # Project documentation
```

🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss the proposed updates.
