"""Streamlit frontend for VideoGame Rater.

Run:
    streamlit run app.py

It talks to the FastAPI backend configured by BASE_URL.
"""

from __future__ import annotations

import os
from datetime import datetime

import pandas as pd
import plotly.express as px
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000/api").rstrip("/")

st.set_page_config(page_title="VideoGame Rater", layout="wide")


# ----------------------------
# HTTP helpers
# ----------------------------

def _headers(api_key: str | None) -> dict:
    return {"api-key": api_key} if api_key else {}


def api_get(path: str, params: dict | None = None) -> requests.Response:
    return requests.get(f"{BASE_URL}{path}", params=params, timeout=15)


def api_post(path: str, json: dict, api_key: str | None = None) -> requests.Response:
    return requests.post(f"{BASE_URL}{path}", json=json, headers=_headers(api_key), timeout=15)


def api_put(path: str, json: dict, api_key: str | None = None) -> requests.Response:
    return requests.put(f"{BASE_URL}{path}", json=json, headers=_headers(api_key), timeout=15)


def api_delete(path: str, api_key: str | None = None) -> requests.Response:
    return requests.delete(f"{BASE_URL}{path}", headers=_headers(api_key), timeout=15)


def validate_api_key(api_key: str) -> bool:
    r = requests.get(f"{BASE_URL}/validate_key/", headers={"api-key": api_key}, timeout=15)
    return r.status_code == 200


# ----------------------------
# Data loaders
# ----------------------------

def load_manufacturers() -> list[dict]:
    r = api_get("/manufacturers/")
    return r.json() if r.status_code == 200 else []


def load_airplanes(filters: dict | None = None) -> list[dict]:
    r = api_get("/airplanes/", params=filters)
    return r.json() if r.status_code == 200 else []


def load_ratings(game_id: int, limit: int = 50) -> list[dict]:
    # note: the backend expects `game_id` param name for compatibility with ratings router
    r = api_get("/ratings/", params={"game_id": game_id, "limit": limit})
    return r.json() if r.status_code == 200 else []


# ----------------------------
# UI
# ----------------------------

st.sidebar.title("VideoGame Rater")
st.sidebar.caption(f"API: {BASE_URL}")

api_key = st.sidebar.text_input("Admin API key (optional)", type="password")
admin_ok = False
if api_key:
    admin_ok = validate_api_key(api_key)
    st.sidebar.success("Admin key valid" if admin_ok else "Invalid key")

page = st.sidebar.radio("Navigate", ["Browse", "Rate a game", "Admin"], index=0)


def page_browse() -> None:
    st.title("Browse airplanes")

    manufacturers = load_manufacturers()
    manufacturer_map = {s["name"]: s["id"] for s in manufacturers}

    c1, c2, c3 = st.columns(3)
    with c1:
        q = st.text_input("Search", placeholder="e.g., 747")
    with c2:
        manufacturer_name = st.selectbox("Manufacturer", ["All"] + sorted(manufacturer_map.keys()))
    with c3:
        min_votes = st.number_input("Leaderboard min votes", min_value=0, value=3, step=1)

    filters = {}
    if q.strip():
        filters["q"] = q.strip()
    if manufacturer_name != "All":
        filters["manufacturer_id"] = manufacturer_map[manufacturer_name]

    airplanes = load_airplanes(filters)
    if not airplanes:
        st.info("No airplanes found. Add some in Admin, then come back.")
        return

    df = pd.DataFrame(airplanes)
    df_display = df[["model", "manufacture_year", "average_score", "ratings_count", "manufacturer_id"]].copy()

    # show manufacturer names
    id_to_name = {s["id"]: s["name"] for s in manufacturers}
    df_display["manufacturer"] = df_display["manufacturer_id"].map(id_to_name)
    df_display = df_display.drop(columns=["manufacturer_id"])

    st.subheader("Airplanes")
    st.dataframe(df_display.sort_values(["average_score", "ratings_count"], ascending=False), use_container_width=True)

    st.subheader("Leaderboard")
    top_r = api_get("/airplanes/leaderboard/top", params={"limit": 10, "min_votes": int(min_votes)})
    if top_r.status_code == 200 and top_r.json():
        top_df = pd.DataFrame(top_r.json())[["model", "average_score", "ratings_count"]]
        st.dataframe(top_df, use_container_width=True)
    else:
        st.caption("Not enough ratings yet for the leaderboard.")

    selected_model = st.selectbox("View airplane", df["model"].tolist())
    airplane = df[df["model"] == selected_model].iloc[0].to_dict()

    st.markdown(f"### {airplane['model']}")
    meta_cols = st.columns(4)
    meta_cols[0].metric("Average score", f"{airplane['average_score']:.2f}")
    meta_cols[1].metric("Ratings", int(airplane["ratings_count"]))
    meta_cols[2].metric("Manufacture year", airplane.get("manufacture_year") or "—")
    meta_cols[3].metric("Manufacturer", id_to_name.get(airplane["manufacturer_id"], "—"))

    if airplane.get("image_url"):
        st.image(airplane["image_url"], width=220)

    st.caption("Capacity: " + (str(airplane.get("capacity")) or "—"))
    st.caption("Types: " + (", ".join(airplane.get("types", [])) or "—"))

    ratings = load_ratings(int(airplane["id"]), limit=200)
    if not ratings:
        st.info("No ratings yet. Be the first to rate this airplane!")
        return

    r_df = pd.DataFrame(ratings)
    r_df["created_at"] = pd.to_datetime(r_df["created_at"], errors="coerce")

    left, right = st.columns([2, 1])
    with right:
        fig = px.histogram(r_df, x="score", nbins=10)
        st.plotly_chart(fig, use_container_width=True)

    with left:
        show_cols = ["score", "username", "comment", "created_at"]
        r_show = r_df[show_cols].sort_values("created_at", ascending=False)
        st.dataframe(r_show, use_container_width=True)


def page_rate() -> None:
    st.title("Rate an airplane")
    airplanes = load_airplanes()
    if not airplanes:
        st.info("No airplanes available yet. Ask an admin to add airplanes first.")
        return

    df = pd.DataFrame(airplanes)
    model_to_id = {row["model"]: int(row["id"]) for _, row in df.iterrows()}

    c1, c2 = st.columns([2, 1])
    with c1:
        model = st.selectbox("Airplane", sorted(model_to_id.keys()))
        score = st.slider("Score", min_value=1, max_value=10, value=8)
        username = st.text_input("Name (optional)")
        comment = st.text_area("Short review (optional)")

        if st.button("Submit rating"):
            payload = {
                "airplane_id": model_to_id[model],
                "score": int(score),
                "username": username.strip() or None,
                "comment": comment.strip() or None,
            }
            r = api_post("/ratings/", json=payload)
            if r.status_code in (200, 201):
                st.success("Thanks! Your rating was saved.")
            else:
                st.error(f"Could not save rating: {r.text}")

    with c2:
        st.subheader("Tips")
        st.write("- Use 1–10 (10 = all-time favorite)")
        st.write("- Keep comments short and helpful")
        st.write("- Refresh Browse to see updated averages")


def page_admin() -> None:
    st.title("Admin")

    if not admin_ok:
        st.warning("Enter a valid admin key in the sidebar to use Admin features.")
        return

    tabs = st.tabs(["Manufacturers", "Airplanes", "Moderation"])

    # ---------- Manufacturers ----------
    with tabs[0]:
        st.subheader("Manufacturers")
        manufacturers = load_manufacturers()
        st.dataframe(pd.DataFrame(manufacturers), use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Add manufacturer")
            name = st.text_input("Manufacturer name")
            if st.button("Add manufacturer"):
                r = api_post("/manufacturers/", json={"name": name}, api_key=api_key)
                if r.status_code in (200, 201):
                    st.success("Manufacturer added")
                    st.experimental_rerun()
                else:
                    st.error(r.text)

        with c2:
            st.markdown("#### Update / delete")
            if manufacturers:
                m_name = st.selectbox("Select", [s["name"] for s in manufacturers])
                m_id = next(s["id"] for s in manufacturers if s["name"] == m_name)
                new_name = st.text_input("New name", value=m_name)
                b1, b2 = st.columns(2)
                with b1:
                    if st.button("Update manufacturer"):
                        r = api_put(f"/manufacturers/{m_id}", json={"name": new_name}, api_key=api_key)
                        if r.status_code == 200:
                            st.success("Updated")
                            st.experimental_rerun()
                        else:
                            st.error(r.text)
                with b2:
                    if st.button("Delete manufacturer"):
                        r = api_delete(f"/manufacturers/{m_id}", api_key=api_key)
                        if r.status_code == 200:
                            st.success("Deleted")
                            st.experimental_rerun()
                        else:
                            st.error(r.text)
            else:
                st.info("No manufacturers yet.")

    # ---------- Airplanes ----------
    with tabs[1]:
        st.subheader("Airplanes")
        manufacturers = load_manufacturers()
        if not manufacturers:
            st.info("Create a manufacturer first.")
        else:
            manufacturer_map = {s["name"]: s["id"] for s in manufacturers}
            airplanes = load_airplanes()
            st.dataframe(pd.DataFrame(airplanes), use_container_width=True)

            st.markdown("#### Add airplane")
            c1, c2, c3 = st.columns(3)
            with c1:
                model = st.text_input("Model", key="g_title")
                manufacturer = st.selectbox("Manufacturer", list(manufacturer_map.keys()), key="g_studio")
            with c2:
                manufacture_year = st.number_input("Manufacture year", min_value=1903, max_value=2100, value=2000)
                capacity = st.number_input("Capacity", min_value=1, value=100)
            with c3:
                types = st.text_input("Types (comma-separated)", placeholder="Passenger, Cargo")
                image_url = st.text_input("Image URL (optional)")

            if st.button("Add airplane"):
                payload = {
                    "model": model,
                    "manufacturer_id": manufacturer_map[manufacturer],
                    "manufacture_year": int(manufacture_year) if manufacture_year else None,
                    "capacity": int(capacity) if capacity else None,
                    "types": [p.strip() for p in types.split(",") if p.strip()],
                    "image_url": image_url.strip() or None,
                }
                r = api_post("/airplanes/", json=payload, api_key=api_key)
                if r.status_code in (200, 201):
                    st.success("Airplane added")
                    st.experimental_rerun()
                else:
                    st.error(r.text)

            st.markdown("#### Update / delete")
            if airplanes:
                model_to_airplane = {g["model"]: g for g in airplanes}
                pick = st.selectbox("Select airplane", list(model_to_airplane.keys()))
                g = model_to_airplane[pick]

                c1, c2 = st.columns(2)
                with c1:
                    new_model = st.text_input("Model", value=g["model"], key="u_title")
                    new_manufacturer = st.selectbox(
                        "Manufacturer",
                        list(manufacturer_map.keys()),
                        index=list(manufacturer_map.values()).index(g["manufacturer_id"]),
                        key="u_studio",
                    )
                    new_year = st.number_input("Manufacture year", min_value=1903, max_value=2100, value=int(g.get("manufacture_year") or 2000), key="u_year")
                with c2:
                    new_capacity = st.number_input("Capacity", value=int(g.get("capacity") or 0), key="u_capacity")
                    new_types = st.text_input("Types", value=", ".join(g.get("types", [])), key="u_types")
                    new_image = st.text_input("Image URL", value=g.get("image_url") or "", key="u_cover")

                b1, b2 = st.columns(2)
                with b1:
                    if st.button("Update airplane"):
                        payload = {
                            "model": new_model,
                            "manufacturer_id": manufacturer_map[new_manufacturer],
                            "manufacture_year": int(new_year) if new_year else None,
                            "capacity": int(new_capacity) if new_capacity else None,
                            "types": [p.strip() for p in new_types.split(",") if p.strip()],
                            "image_url": new_image.strip() or None,
                        }
                        r = api_put(f"/airplanes/{int(g['id'])}", json=payload, api_key=api_key)
                        if r.status_code == 200:
                            st.success("Updated")
                            st.experimental_rerun()
                        else:
                            st.error(r.text)
                with b2:
                    if st.button("Delete airplane"):
                        r = api_delete(f"/airplanes/{int(g['id'])}", api_key=api_key)
                        if r.status_code == 200:
                            st.success("Deleted")
                            st.experimental_rerun()
                        else:
                            st.error(r.text)
            else:
                st.caption("No airplanes yet.")

    # ---------- Moderation ----------
    with tabs[2]:
        st.subheader("Recent ratings")
        r = api_get("/ratings/recent", params={"limit": 50})
        if r.status_code != 200:
            st.error(r.text)
            return

        ratings = r.json()
        if not ratings:
            st.caption("No ratings yet.")
            return

        df = pd.DataFrame(ratings)
        st.dataframe(df, use_container_width=True)

        rating_id = st.number_input("Rating id to delete", min_value=1, value=int(df.iloc[0]["id"]))
        if st.button("Delete rating"):
            del_r = api_delete(f"/ratings/{int(rating_id)}", api_key=api_key)
            if del_r.status_code == 200:
                st.success("Deleted")
                st.experimental_rerun()
            else:
                st.error(del_r.text)


if page == "Browse":
    page_browse()
elif page == "Rate an airplane":
    page_rate()
else:
    page_admin()
