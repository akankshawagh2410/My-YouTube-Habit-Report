# 📺 YouTube Watch History Analysis

This project analyzes **personal YouTube watch history** data exported from **Google Takeout**. Using Python, I performed **data cleaning, exploratory data analysis (EDA), and visualization** to uncover trends in content consumption, binge-watching habits, and channel preferences.

---

## 🚀 Project Overview
This project demonstrates:
- Extracting and cleaning JSON data from Google Takeout.
- Feature engineering (date, time, weekday, hour).
- Descriptive analytics and visualization to uncover trends.
- Binge-watching detection (videos watched <30 minutes apart).
- Identifying top creators, binge days, and activity patterns over time.

---

## 🔍 Analyses Performed
| Analysis | Description |
|----------|-------------|
| **Top Channels** | Ranked top 10 most-watched creators. |
| **Monthly & Yearly Trends** | Line charts showing watch activity over time. |
| **Hourly & Day-of-Week Patterns** | Viewing habits by time of day and weekdays. |
| **Heatmap** | Visualized watch frequency by day and hour. |
| **Longest Binge Day** | Found the day with the highest video count and top creators. |
| **Binge Transitions** | Counted how often I watched videos back-to-back (<30 minutes apart). |
| **Keyword Insights** | Extracted top keywords from video titles. |

---

## 📂 How to Download Your YouTube Data
1. Go to [Google Takeout](https://takeout.google.com/).  
2. **Deselect all** products, then scroll down and select **YouTube and YouTube Music**.  
3. Choose **JSON** format for your watch history.  
4. Export and download your data.  
5. Locate the file named `watch-history.json`.  
6. Place it in your project folder.

---

## 🛠️ Tech Stack
- **Python**: Data processing & analysis
- **Pandas**: Data cleaning and feature engineering
- **Matplotlib & Seaborn**: Visualization
- **Jupyter Notebook**: Exploratory workflow

---

## 🏁 How to Run
1. Clone this repository or download the files.  
2. Install dependencies:
   ```bash
   pip install pandas matplotlib seaborn
