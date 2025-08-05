# Book Library
This project aims to develop an AI agent capable of summarising large context from files and publish it in the Web-based interface. 

# Tech Stack
1. Django (backend)
2. UV (dependency management)
3. SQLite (database)
4. LangFlow (AI builder)

# Requirements
1. Clone this repository.
2. Download uv on local machine.
3. Install Python 3.10 with command `uv python install 3.10` and pin it using `uv python pin 3.10`.
4. Create a virtual environment using `uv venv .venv` and change to it using `source .venv/bin/activate`.
5. Install dependencies using the command `uv pip install -r requirements.txt`.
6. Verify if LangFlow runs error-free with the command `langflow run`. Solve issues if required.
7. Change directory to `onlinelib` and run the application using command `python manage.py runserver`.

# Note!!
- `env.example` is invalid and must be renamed to `.env` use environmental variables.
- Some API keys are not provided alongside the code and requires user to extract from personal Google AI Studio, LangFlow and AstraDB.
