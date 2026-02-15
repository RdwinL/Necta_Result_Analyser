import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import plotly.express as px

# ==============================
# CONFIGURATION
# ==============================

DATA_DIR = "data"
CENTRE_FILE = f"{DATA_DIR}/necta_centres.csv"
MAX_WORKERS = 5
REQUEST_TIMEOUT = 10

os.makedirs(DATA_DIR, exist_ok=True)

st.set_page_config(
    page_title="NECTA Enterprise Analyzer",
    layout="wide"
)

# ==============================
# NETWORK SESSION (Faster)
# ==============================

session = requests.Session()

# ==============================
# GET SCHOOL LINKS
# ==============================

@st.cache_data(ttl=3600)
def get_school_links():
    base_url = "https://matokeo.necta.go.tz/results/2025/csee/"
    index_url = f"{base_url}index.htm"

    try:
        r = session.get(index_url, timeout=REQUEST_TIMEOUT)
        soup = BeautifulSoup(r.content, "html.parser")

        schools = []
        for link in soup.find_all("a", href=True):
            href = link["href"]
            if href.endswith(".htm") and "results/" in href:
                code = href.split("/")[-1].replace(".htm", "")
                schools.append({
                    "code": code,
                    "name": link.text.strip(),
                    "url": base_url + href
                })
        return schools
    except:
        return []

# ==============================
# EXTRACT CENTRE DATA (Lightweight)
# ==============================

def extract_centre(url, code, name):
    try:
        r = session.get(url, timeout=REQUEST_TIMEOUT)
        soup = BeautifulSoup(r.content, "html.parser")
        text = soup.get_text()

        # Region
        region = "Unknown"
        m = re.search(r"REGION\s*([A-Z ]+)", text)
        if m:
            region = m.group(1).strip()

        # GPA
        gpa = None
        m = re.search(r"GPA\s*([\d.]+)", text)
        if m:
            gpa = float(m.group(1))

        # Division I count
        div1 = 0
        m = re.search(r"DIVISION I\s*(\d+)", text)
        if m:
            div1 = int(m.group(1))

        # Total Passed
        total_passed = 0
        m = re.search(r"PASSED CANDIDATES\s*(\d+)", text)
        if m:
            total_passed = int(m.group(1))

        return {
            "code": code,
            "name": name,
            "region": region,
            "gpa": gpa,
            "div1": div1,
            "total_passed": total_passed
        }

    except:
        return None

# ==============================
# PARALLEL SCRAPER
# ==============================

def run_scraper(schools):
    results = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(extract_centre, s["url"], s["code"], s["name"]): s
            for s in schools
        }

        progress = st.progress(0)
        total = len(futures)

        for i, future in enumerate(as_completed(futures)):
            data = future.result()
            if data:
                results.append(data)

            progress.progress((i + 1) / total)

    return results

# ==============================
# LOAD EXISTING DATA
# ==============================

def load_data():
    if os.path.exists(CENTRE_FILE):
        return pd.read_csv(CENTRE_FILE)
    return pd.DataFrame()

# ==============================
# SAVE DATA
# ==============================

def save_data(df):
    df.to_csv(CENTRE_FILE, index=False)

# ==============================
# STREAMLIT UI
# ==============================

st.title("📊 NECTA Enterprise Analyzer 2025")

schools = get_school_links()

if not schools:
    st.error("Failed to load schools")
    st.stop()

st.sidebar.success(f"{len(schools)} centres found")

mode = st.sidebar.radio(
    "Mode",
    ["Sample (50)", "Batch (200)", "Full"]
)

if mode == "Sample (50)":
    selected = schools[:50]
elif mode == "Batch (200)":
    selected = schools[:200]
else:
    selected = schools

if st.sidebar.button("Start Extraction"):

    existing = load_data()

    processed_codes = set(existing["code"]) if not existing.empty else set()

    to_process = [s for s in selected if s["code"] not in processed_codes]

    st.info(f"Processing {len(to_process)} new centres")

    new_data = run_scraper(to_process)

    if new_data:
        df_new = pd.DataFrame(new_data)
        df_all = pd.concat([existing, df_new], ignore_index=True)
        save_data(df_all)
        st.success("Data saved successfully")

# ==============================
# DASHBOARD
# ==============================

df = load_data()

if not df.empty:

    st.header("Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Centres", len(df))
    col2.metric("Avg GPA", round(df["gpa"].dropna().mean(), 2))
    col3.metric("Total Division I", int(df["div1"].sum()))

    # Regional performance
    st.subheader("Regional Performance")

    reg = df.groupby("region").agg({
        "gpa": "mean",
        "div1": "sum",
        "code": "count"
    }).rename(columns={"code": "centres"}).reset_index()

    fig = px.bar(reg, x="region", y="gpa", title="Average GPA by Region")
    st.plotly_chart(fig, use_container_width=True)

    # Top performers
    st.subheader("Top 20 Centres")

    top = df.dropna(subset=["gpa"]).nsmallest(20, "gpa")
    st.dataframe(top, use_container_width=True)

    # Download
    csv = df.to_csv(index=False)
    st.download_button("Download Data", csv, "necta_enterprise.csv")
