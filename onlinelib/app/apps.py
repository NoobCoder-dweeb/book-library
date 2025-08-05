from django.apps import AppConfig
import subprocess
import os
import sys
from pathlib import Path
import atexit

class AppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"

    def ready(self):
        if os.environ.get("RUN_MAIN") != "true":
            return  # Ensure RUN_MAIN is set for the server
        
        if "runserver" in sys.argv:
            lock_file = Path("tmp/langflow.lock")

            if lock_file.exists():
                print("LangFlow is already running. Skipping startup.")
                return
            try:
                # Start the Langflow server
                subprocess.Popen(["langflow", "run", "--port", "7860"])
                lock_file.write_text("LangFlow is running")
                print("✅ LangFlow started on port 7860")
            except Exception as e:
                print(f"❌ Failed to start LangFlow: {e}")


def cleanup():
    lock_file = Path("tmp/langflow.lock")
    if lock_file.exists():
        lock_file.unlink()
        print("✅ LangFlow lock file removed on exit.")
        
atexit.register(cleanup)
