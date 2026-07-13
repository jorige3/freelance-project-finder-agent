import sys
import subprocess

def main():
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "api":
            print("Starting FastAPI backend...")
            subprocess.run(["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8010"])
            return
        elif command == "dashboard":
            print("Starting Streamlit dashboard...")
            subprocess.run(["streamlit", "run", "dashboard/app.py"])
            return
            
    print("Usage: python main.py [api|dashboard]")
    print("\nOr run the helper scripts:")
    print("  ./scripts/run.sh     - Run both services locally")
    print("  ./scripts/deploy.sh  - Run both services via Docker Compose")

if __name__ == "__main__":
    main()

