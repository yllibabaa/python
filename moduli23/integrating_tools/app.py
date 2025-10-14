import streamlit as st
import requests
import pandas as pd

st.title("project management app")

st.header("Add Developer")
dev_name = st.text_input("Developer Name")
dev_experience = st.number_input("Experience (years)", min_value=0, max_value=50, value=0)

if st.button("create Developer"):
    dev_data = {"name": dev_name, "experience": dev_experience}
    response = requests.post("http//:/localhost:8000/developers/", json=dev_data)
    st.json(response.json())

st.header("Add Project")
proj_title = st.text_input("Project Title")
proj_desc = st.text_area("Project Description")
proj_langs = st.date_input("languages used (cpmma-separated)")
lead_dev_name = st.text_input("lead developer name")
lead_dev_exp = st.number_input("lead developer experience (years)", min_value=0, max_value=50, value=0)

if st.button("create Project"):
    lead_dev_data = {"name": lead_dev_name, "experience": lead_dev_exp}
    pro_data = {
        "title": proj_title,
        "description": proj_desc,
        "languages": proj_langs.split(","),
        "lead_developer": lead_dev_data
    }
    response = requests.post("http://localhost:8000/projects/", json=pro_data)
    projects_data = (response.json())

    st.header("Projects dashboard")

    if st.button("get projects"):
        response = requests.get("http://localhost:8000/projects/")
        projects_data = response.json()['projects']

        if projects_data:
            projects_df = pd.DataFrame(projects_data)

            st.subheader("Projects overview")
            st.dataframe(projects_df)

            st.subheader("Projects details")
            for project in projects_data:
                st.markdown(f"**title:** {project['title']})")
                st.markdown(f"**Description:** {project['description']}")
                st.markdown(f"**Languages:** {', '.join(project['languages'])}")
                st.markdown(f"**Lead Developer:** {project['name']} ({project['experience']} years experience)")
                st.markdown("---")
            else:
                st.warning("No projects found.")



