from django.apps import AppConfig
import subprocess
import os
import sys

class AppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"

    def ready(self):
        # Check if the 'langflow' package is installed
        try:
            import langflow  # noqa: F401
        except ImportError:
            # If not installed, run the installation command
            subprocess.run(["pip", "install", "langflow"], check=True)
            print("langflow package installed successfully.")
        else:   
            print("langflow package is already installed.")
            
            if os.environ.get("RUN_MAIN", None) != "true":
                return
            
            if "runserver" in sys.argv:
                try:
                    # Start the Langflow server
                    subprocess.Popen(["langflow", "run", "--port", "7860"])
                    print("✅ LangFlow started on port 7860")
                except Exception as e:
                    print(f"❌ Failed to start LangFlow: {e}")
