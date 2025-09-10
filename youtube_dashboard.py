import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from collections import Counter
import re

st.set_page_config(page_title="YouTube Watch History Dashboard", layout="wide")

# ---------------------------
# File Upload
# ---------------------------
st.title("📺 YouTube Watch History Dashboard")
uploaded_file = st.file_uploader("Upload your watch-history.json from Google Takeout", type="json")

if uploaded_file:
    # Load JSON
    data = json.load(uploaded_file)

    # Parse JSON
    records = []
    for item in data:
        if "title" in item and "time" in item:
            records.append({
                "title": item.get("title"),
                "video_url": item.get("titleUrl"),
                "channel": item.get("subtitles", [{}])[0].get("name"),
                "watched_at": pd.to_datetime(item.get("time")),
                "platform": ", ".join(item.get("products", []))
            })

    df = pd.DataFrame(records)
    df["date"] = df["watched_at"].dt.date
    df["hour"] = df["watched_at"].dt.hour
    df["month"] = df["watched_at"].dt.to_period("M")
    df["year"] = df["watched_at"].dt.year
    df["weekday"] = df["watched_at"].dt.day_name()

    st.success(f"✅ Loaded {len(df)} watch records!")

    # ---------------------------
    # Key Metrics
    # ---------------------------
    total_videos = len(df)
    total_days = df["date"].nunique()
    top_channel = df["channel"].value_counts().idxmax()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Videos Watched", f"{total_videos:,}")
    col2.metric("Unique Days Active", f"{total_days:,}")
    col3.metric("Top Channel", top_channel)

    # ---------------------------
    # 1. Top 10 Channels
    # ---------------------------
    st.subheader("🎯 Top 10 Channels by Views")
    top_channels = df["channel"].value_counts().head(10)

    fig, ax = plt.subplots(figsize=(10, 5))
    top_channels.plot(kind="bar", color="#FF0000", edgecolor="black", ax=ax)
    ax.set_title("Top 10 Channels by Views", fontsize=16, fontweight="bold")
    ax.set_xlabel("Channel")
    ax.set_ylabel("Views")
    plt.xticks(rotation=45, ha="right")
    for i, v in enumerate(top_channels):
        ax.text(i, v + max(top_channels)*0.01, f"{v:,}", ha="center", fontsize=9)
    st.pyplot(fig)

    # ---------------------------
    # 2. Monthly Trend
    # ---------------------------
    st.subheader("📅 Monthly Watch History")
    monthly_counts = df.groupby("month").size()

    fig, ax = plt.subplots(figsize=(10,5))
    monthly_counts.plot(kind="line", marker="o", color="#FF0000", linewidth=2, ax=ax)
    ax.set_title("Monthly YouTube Watch History", fontsize=16, fontweight="bold")
    ax.set_xlabel("Month")
    ax.set_ylabel("Views")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # ---------------------------
    # 3. Hourly Watch Pattern
    # ---------------------------
    st.subheader("⏰ Watching Activity by Hour")
    hourly_counts = df.groupby("hour").size()

    fig, ax = plt.subplots(figsize=(10,5))
    hourly_counts.plot(kind="bar", color="#FF0000", edgecolor="black", ax=ax)
    ax.set_title("YouTube Activity by Hour", fontsize=16, fontweight="bold")
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Views")
    plt.xticks(rotation=0)
    st.pyplot(fig)

    # ---------------------------
    # 4. Day of Week Pattern
    # ---------------------------
    st.subheader("📆 Most Watched Days of the Week")
    weekday_counts = df["weekday"].value_counts()

    fig, ax = plt.subplots(figsize=(10,5))
    weekday_counts.plot(kind="bar", color="#FF0000", edgecolor="black", ax=ax)
    ax.set_title("Most Watched Days", fontsize=16, fontweight="bold")
    plt.xticks(rotation=30)
    st.pyplot(fig)

    # ---------------------------
    # 5. Heatmap (Day vs Hour)
    # ---------------------------
    st.subheader("🔥 Heatmap: Watch Activity by Day & Hour")
    heatmap_data = df.groupby(["weekday", "hour"]).size().unstack(fill_value=0)

    fig, ax = plt.subplots(figsize=(12,6))
    sns.heatmap(heatmap_data, cmap="Reds", ax=ax)
    ax.set_title("YouTube Watch Heatmap (Day vs Hour)", fontsize=16, fontweight="bold")
    st.pyplot(fig)

    # ---------------------------
    # 6. Longest Binge Day
    # ---------------------------
    st.subheader("🍿 Longest Binge Day")
    daily_counts = df.groupby("date").size()
    longest_day = daily_counts.idxmax()
    st.write(f"**Your biggest binge day was {longest_day} with {daily_counts.max()} videos.**")

    # ---------------------------
    # 7. Binge Transitions (<30 mins apart)
    # ---------------------------
    df = df.sort_values("watched_at")
    df["time_diff"] = df["watched_at"].diff().dt.total_seconds().div(60)
    binge_transitions = df[df["time_diff"] < 30].shape[0]
    st.write(f"🔥 You had **{binge_transitions} binge transitions** (videos started within 30 minutes of the previous one).")

    # ---------------------------
    # 8. Keyword Analysis
    # ---------------------------
    st.subheader("🔍 Top Keywords in Titles")
    words = []
    for title in df["title"]:
        words.extend(re.findall(r'\w+', str(title).lower()))

    common_words = Counter(words).most_common(20)
    word_df = pd.DataFrame(common_words, columns=["Keyword", "Count"])

    fig, ax = plt.subplots(figsize=(10,5))
    word_df.set_index("Keyword")["Count"].plot(kind="bar", color="#FF0000", edgecolor="black", ax=ax)
    ax.set_title("Top 20 Keywords in Video Titles", fontsize=16, fontweight="bold")
    plt.xticks(rotation=45)
    st.pyplot(fig)

else:
    st.info("👆 Upload your `watch-history.json` to see your stats!")
