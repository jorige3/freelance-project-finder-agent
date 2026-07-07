from fastapi import FastAPI

app = FastAPI(
    title="Freelance Project Finder AI Agent",
    version="0.1.0",
    description="AI agent to collect, rank, and recommend freelance projects."
)

@app.get("/")
def root():
    return {
        "status": "running",
        "project": "Freelance Project Finder AI Agent",
        "version": "0.1.0"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}
