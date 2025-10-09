from fastapi import FastAPI
from models import Developer, Project

app = FastAPI()

@app.post("/developers/")
def create_developer(developer: Developer):
    return {"message": "Developer created sucessullf", "developer": developer}


@app.post("/projects/")
def create_project(project: Project):
    return {"message": "Project created successfully", "project": project}


@app.get("/projects/")
def get_projects():
    sample_project = Project(
        title="sample project",
        description="this is a description.",
        languages=["Python", "JavaScript"],
        lead_developer=Developer(name="Alice", experience=5)
    )
    return {"projects": [sample_project]}


