
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json

st.set_page_config(page_title="📊 YouTube Habit Dashboard", layout="wide")
st.title("📺 The YouTube Habit Report")

# ---- Load Data ----
with open("watch-history.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# ---- Original Notebook Parsing + Analysis ----
# Converted from notebook cells

import json
import pandas as pd

with open("watch-history.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Convert to records
records = []
for item in data:
    if "title" in item and "time" in item:
        records.append({
            "title": item.get("title"),
            "video_url": item.get("titleUrl"),
            "channel": item.get("subtitles", [{}])[0].get("name"),
            "channel_url": item.get("subtitles", [{}])[0].get("url"),
            "watched_at": pd.to_datetime(item.get("time")),
            "platform": ", ".join(item.get("products", []))
        })

df = pd.DataFrame(records)

# Extract time-based features
df["date"] = df["watched_at"].dt.date
df["hour"] = df["watched_at"].dt.hour
df["month"] = df["watched_at"].dt.to_period("M")
df["year"] = df["watched_at"].dt.year
df["weekday"] = df["watched_at"].dt.day_name()

df.head()

import matplotlib.pyplot as plt

def styled_bar_chart(data, title, xlabel="", ylabel="", rotation=45, color="#b92e34"):
    plt.figure(figsize=(12, 6))
    bars = data.plot(
        kind="bar",
        color=color,
        edgecolor="black"
    )
    
    # YouTube Style
    plt.title(title, fontsize=18, fontweight="bold", color="#282828")
    plt.xlabel(xlabel, fontsize=14, fontweight="semibold")
    plt.ylabel(ylabel, fontsize=14, fontweight="semibold")
    plt.xticks(rotation=rotation, ha="right", fontsize=12)
    plt.yticks(fontsize=12)
    
    # Remove spines
    for spine in ["top", "right"]:
        plt.gca().spines[spine].set_visible(False)
    
    # Add value labels
    for i, v in enumerate(data):
        plt.text(i, v + max(data)*0.01, f"{v:,}", ha="center", fontsize=11, fontweight="medium")
    
    plt.tight_layout()
    plt.show()


top_channels = df["channel"].value_counts().head(20)
styled_bar_chart(top_channels, "Top 10 Channels by Views", xlabel="Channel", ylabel="Views")

monthly_counts = df.groupby("month").size()
plt.figure(figsize=(12,6))
monthly_counts.plot(kind="line", marker="o", color="#b92e34", linewidth=2)

# Style
plt.title("Monthly YouTube Watch History", fontsize=18, fontweight="bold", color="#282828")
plt.xlabel("Month", fontsize=14, fontweight="semibold")
plt.ylabel("Views", fontsize=14, fontweight="semibold")
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)
for spine in ["top", "right"]:
    plt.gca().spines[spine].set_visible(False)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()


hourly_counts = df.groupby("hour").size()
styled_bar_chart(hourly_counts, "YouTube Watching Activity by Hour", xlabel="Hour of Day", ylabel="Views")

weekday_counts = df["weekday"].value_counts()
styled_bar_chart(weekday_counts, "Most Watched Days of the Week", xlabel="Day", ylabel="Views")

yearly_counts = df.groupby("year").size()
plt.figure(figsize=(12,6))
yearly_counts.plot(kind="line", marker="o", color="#b92e34", linewidth=2)

plt.title("Yearly YouTube Watch Trends", fontsize=18, fontweight="bold", color="#282828")
plt.xlabel("Year", fontsize=14, fontweight="semibold")
plt.ylabel("Views", fontsize=14, fontweight="semibold")
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)
for spine in ["top", "right"]:
    plt.gca().spines[spine].set_visible(False)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

import seaborn as sns

heatmap_data = df.groupby(["weekday", "hour"]).size().unstack(fill_value=0)

plt.figure(figsize=(12,6))
sns.heatmap(heatmap_data, cmap="Reds", annot=False, cbar=True)
plt.title("YouTube Watch Heatmap (Day vs Hour)", fontsize=18, fontweight="bold", color="#282828")
plt.xlabel("Hour of Day", fontsize=14, fontweight="semibold")
plt.ylabel("Day of Week", fontsize=14, fontweight="semibold")
plt.tight_layout()
plt.show()

late_night_df = df[(df["hour"] >= 23) | (df["hour"] <= 3)]
late_night_creators = late_night_df["channel"].value_counts().head(10)

plt.figure(figsize=(10,6))
bars = late_night_creators.plot(
    kind="barh",
    color="#b92e34",
    edgecolor="black"
)

plt.title("Top 10 Late-Night Creators (11 PM – 3 AM)", fontsize=16, fontweight="bold", color="#282828")
plt.xlabel("Views", fontsize=14, fontweight="semibold")
plt.ylabel("Channel", fontsize=14, fontweight="semibold")
plt.gca().invert_yaxis()  # highest at the top
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)


for i, v in enumerate(late_night_creators):
    plt.text(v + max(late_night_creators)*0.01, i, f"{v:,}", va="center", fontsize=11, fontweight="medium")

plt.tight_layout()
plt.show()

daily_counts = df.groupby("date").size()
longest_day = daily_counts.idxmax()
print(f"🔥 Your biggest binge day was {longest_day} with {daily_counts.max()} videos!")

# Find longest binge day
daily_counts = df.groupby("date").size()
longest_day = daily_counts.idxmax()

# Filter for that day
longest_day_data = df[df["date"] == longest_day]

# Count creators
creator_counts = longest_day_data["channel"].value_counts()

# Find the max watch count
max_watches = creator_counts.max()

# Filter all creators with that max count
top_creators = creator_counts[creator_counts == max_watches]

print(f"🔥 On your biggest binge day ({longest_day}), these were your top creators:")
for creator, count in top_creators.items():
    print(f"  - {creator}: {count} videos")

df = df.sort_values("watched_at")
df["time_diff"] = df["watched_at"].diff().dt.total_seconds().div(60)
binge_sessions = df[df["time_diff"] < 30].shape[0]
print(f"🔥 You had {binge_sessions} binge sessions (videos <30 mins apart).")

# ---- Layout: display figures ----
# Note: The notebook code already creates plots with matplotlib/seaborn.
# In Streamlit, replace plt.show() with st.pyplot(fig).
# We'll attempt to catch active figures and display them.

import matplotlib.pyplot as plt

# Collect all figures created
figs = [plt.figure(n) for n in plt.get_fignums()]

# Safety check: make sure we have 7 figures
if len(figs) < 7:
    st.warning(f"Expected 7 figures, found {len(figs)}. Check your notebook-to-dashboard conversion.")
else:
    # Row 1 (3 graphs)
    row1 = st.columns(3)
    for i in range(3):
        with row1[i]:
            st.pyplot(figs[i])

    # Row 2 (3 graphs)
    row2 = st.columns(3)
    for i in range(3, 6):
        with row2[i - 3]:
            st.pyplot(figs[i])

    # Row 3 (1 graph centered)
    row3 = st.columns([1,2,1])  # middle column wider
    with row3[1]:
        st.pyplot(figs[6])