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

def load_studios() -> list[dict]:
    r = api_get("/studios/")
    return r.json() if r.status_code == 200 else []


def load_games(filters: dict | None = None) -> list[dict]:
    r = api_get("/games/", params=filters)
    return r.json() if r.status_code == 200 else []


def load_ratings(game_id: int, limit: int = 50) -> list[dict]:
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
    st.title("Browse games")

    studios = load_studios()
    studio_map = {s["name"]: s["id"] for s in studios}

    c1, c2, c3 = st.columns(3)
    with c1:
        q = st.text_input("Search", placeholder="e.g., Zelda")
    with c2:
        studio_name = st.selectbox("Studio", ["All"] + sorted(studio_map.keys()))
    with c3:
        min_votes = st.number_input("Leaderboard min votes", min_value=0, value=3, step=1)

    filters = {}
    if q.strip():
        filters["q"] = q.strip()
    if studio_name != "All":
        filters["studio_id"] = studio_map[studio_name]

    games = load_games(filters)
    if not games:
        st.info("No games found. Add some in Admin, then come back.")
        return

    df = pd.DataFrame(games)
    df_display = df[["title", "release_year", "average_score", "ratings_count", "studio_id"]].copy()

    # show studio names
    id_to_name = {s["id"]: s["name"] for s in studios}
    df_display["studio"] = df_display["studio_id"].map(id_to_name)
    df_display = df_display.drop(columns=["studio_id"])

    st.subheader("Games")
    st.dataframe(df_display.sort_values(["average_score", "ratings_count"], ascending=False), use_container_width=True)

    st.subheader("Leaderboard")
    top_r = api_get("/games/leaderboard/top", params={"limit": 10, "min_votes": int(min_votes)})
    if top_r.status_code == 200 and top_r.json():
        top_df = pd.DataFrame(top_r.json())[["title", "average_score", "ratings_count"]]
        st.dataframe(top_df, use_container_width=True)
    else:
        st.caption("Not enough ratings yet for the leaderboard.")

    selected_title = st.selectbox("View game", df["title"].tolist())
    game = df[df["title"] == selected_title].iloc[0].to_dict()

    st.markdown(f"### {game['title']}")
    meta_cols = st.columns(4)
    meta_cols[0].metric("Average score", f"{game['average_score']:.2f}")
    def load_games(filters: dict | None = None) -> list[dict]:
    meta_cols[2].metric("Release year", game.get("release_year") or "—")
    meta_cols[3].metric("Studio", id_to_name.get(game["studio_id"], "—"))

    def load_manufacturers() -> list[dict]:
        r = api_get("/manufacturers/")
        return r.json() if r.status_code == 200 else []
    if game.get("cover_url"):
        st.image(game["cover_url"], width=220)

    st.caption("Platforms: " + (", ".join(game.get("platforms", [])) or "—"))
    st.caption("Genres: " + (", ".join(game.get("genres", [])) or "—"))

    ratings = load_ratings(int(game["id"]), limit=200)
    if not ratings:
        st.info("No ratings yet. Be the first to rate this game!")
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


    page = st.sidebar.radio("Navigate", ["Browse", "Rate an airplane", "Admin"], index=0)
    st.title("Rate a game")
    games = load_games()
    if not games:
        st.info("No games available yet. Ask an admin to add games first.")
        return

    df = pd.DataFrame(games)
    title_to_id = {row["title"]: int(row["id"]) for _, row in df.iterrows()}

    c1, c2 = st.columns([2, 1])
    with c1:
        title = st.selectbox("Game", sorted(title_to_id.keys()))
        score = st.slider("Score", min_value=1, max_value=10, value=8)
        username = st.text_input("Name (optional)")
        comment = st.text_area("Short review (optional)")

        if st.button("Submit rating"):
            payload = {
                "game_id": title_to_id[title],
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

    tabs = st.tabs(["Studios", "Games", "Moderation"])

    # ---------- Studios ----------
    with tabs[0]:
        st.subheader("Studios")
        studios = load_studios()
        st.dataframe(pd.DataFrame(studios), use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Add studio")
            name = st.text_input("Studio name")
            if st.button("Add studio"):
                r = api_post("/studios/", json={"name": name}, api_key=api_key)
                if r.status_code in (200, 201):
                    st.success("Studio added")
                    st.experimental_rerun()
                else:
                    st.error(r.text)

        with c2:
            st.markdown("#### Update / delete")
            if studios:
                studio_name = st.selectbox("Select", [s["name"] for s in studios])
                studio_id = next(s["id"] for s in studios if s["name"] == studio_name)
                new_name = st.text_input("New name", value=studio_name)
                b1, b2 = st.columns(2)
                with b1:
                    if st.button("Update studio"):
                        r = api_put(f"/studios/{studio_id}", json={"name": new_name}, api_key=api_key)
                        if r.status_code == 200:
                            st.success("Updated")
                            st.experimental_rerun()
                        else:
                            st.error(r.text)
                with b2:
                    if st.button("Delete studio"):
                        r = api_delete(f"/studios/{studio_id}", api_key=api_key)
                        if r.status_code == 200:
                            st.success("Deleted")
                            st.experimental_rerun()
                        else:
                            st.error(r.text)
            else:
                st.info("No studios yet.")

    # ---------- Games ----------
    with tabs[1]:
        st.subheader("Games")
        studios = load_studios()
        if not studios:
            st.info("Create a studio first.")
        else:
            studio_map = {s["name"]: s["id"] for s in studios}
            games = load_games()
            st.dataframe(pd.DataFrame(games), use_container_width=True)

            st.markdown("#### Add game")
            c1, c2, c3 = st.columns(3)
            with c1:
                title = st.text_input("Title", key="g_title")
                studio = st.selectbox("Studio", list(studio_map.keys()), key="g_studio")
            with c2:
                release_year = st.number_input("Release year", min_value=1970, max_value=2100, value=2020)
                platforms = st.text_input("Platforms (comma-separated)", placeholder="PC, PS5")
            with c3:
                genres = st.text_input("Genres (comma-separated)", placeholder="RPG, Action")
                cover_url = st.text_input("Cover URL (optional)")

            if st.button("Add game"):
                payload = {
                    "title": title,
                    "studio_id": studio_map[studio],
                    "release_year": int(release_year) if release_year else None,
                    "platforms": [p.strip() for p in platforms.split(",") if p.strip()],
                    "genres": [g.strip() for g in genres.split(",") if g.strip()],
                    "cover_url": cover_url.strip() or None,
                }
                r = api_post("/games/", json=payload, api_key=api_key)
                if r.status_code in (200, 201):
                    st.success("Game added")
                    st.experimental_rerun()
                else:
                    st.error(r.text)

            st.markdown("#### Update / delete")
            if games:
                title_to_game = {g["title"]: g for g in games}
                pick = st.selectbox("Select game", list(title_to_game.keys()))
                g = title_to_game[pick]

                c1, c2 = st.columns(2)
                with c1:
                    new_title = st.text_input("Title", value=g["title"], key="u_title")
                    new_studio = st.selectbox(
                        "Studio",
                        list(studio_map.keys()),
                        index=list(studio_map.values()).index(g["studio_id"]),
                        key="u_studio",
                    )
                    new_year = st.number_input("Release year", min_value=1970, max_value=2100, value=int(g.get("release_year") or 2020), key="u_year")
                with c2:
                    new_platforms = st.text_input("Platforms", value=", ".join(g.get("platforms", [])), key="u_platforms")
                    new_genres = st.text_input("Genres", value=", ".join(g.get("genres", [])), key="u_genres")
                    new_cover = st.text_input("Cover URL", value=g.get("cover_url") or "", key="u_cover")

                b1, b2 = st.columns(2)
                with b1:
                    if st.button("Update game"):
                        payload = {
                            "title": new_title,
                            "studio_id": studio_map[new_studio],
                            "release_year": int(new_year) if new_year else None,
                            "platforms": [p.strip() for p in new_platforms.split(",") if p.strip()],
                            "genres": [x.strip() for x in new_genres.split(",") if x.strip()],
                            "cover_url": new_cover.strip() or None,
                        }
                        r = api_put(f"/games/{int(g['id'])}", json=payload, api_key=api_key)
                        if r.status_code == 200:
                            st.success("Updated")
                            st.experimental_rerun()
                        else:
                            st.error(r.text)
                with b2:
                    if st.button("Delete game"):
                        r = api_delete(f"/games/{int(g['id'])}", api_key=api_key)
                        if r.status_code == 200:
                            st.success("Deleted")
                            st.experimental_rerun()
                        else:
                            st.error(r.text)
            else:
                st.caption("No games yet.")

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
elif page == "Rate a game":
    page_rate()
else:
    page_admin()
