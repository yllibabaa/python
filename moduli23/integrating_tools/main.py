from fastapi import FastAPI
from models import Developer, Project


app = FastAPI()


@app.post("/developers/")
def create_developer(developer: Developer):
    return {"message": "Developer created successfully", "developer": developer}


@app.post("/projects/")
def create_project(project: Project):
    return {"message": "Project created successfully", "project": project}


@app.get("/projects/")
def get_projects():
    # This is a placeholder; in a real application, you'd fetch this from a database
    sample_project = Project(
        title="Sample Project",
        description="This is a sample project",
        languages=["Python", "JavaScript"],
        lead_developer=Developer(name="Jane Doe", experience=5)
    )
    return {"projects": [sample_project]}