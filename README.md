# The YouTube Habit Report
This project analyzes **personal YouTube watch history** data exported from **Google Takeout**. Using Python, I performed **data cleaning, exploratory data analysis (EDA), and visualization** to uncover trends in content consumption, binge-watching habits, and channel preferences.

## Tech Stack
- **Python**: Data processing & analysis
- **Pandas**: Data cleaning and feature engineering
- **Matplotlib & Seaborn**: Visualization
- **Jupyter Notebook**: Exploratory workflow
- **Streamlit**: Interactive Dashboard

## Overview
This project explores personal YouTube watch history (from **Google Takeout**) to uncover patterns, habits, and insights.  
It includes:
- **Exploratory Data Analysis** (EDA) in Jupyter Notebook  
- **7 key visualizations** (channels, time trends, binge behavior, etc.)  
- A **Streamlit Dashboard** version of the notebook for interactive exploration  


## How to download your own YouTube Data
1. Go to [Google Takeout](https://takeout.google.com/).  
2. Deselect everything, then select only **YouTube and YouTube Music → History**.  
3. Export and download as **JSON**.  
4. Extract the ZIP and find `watch-history.json`.  
5. Place it in your project folder.

## Analyses Performed
| Analysis | Description |
|----------|-------------|
| **Top Channels** | Ranked top 10 most-watched creators. |
| **Monthly & Yearly Trends** | Line charts showing watch activity over time. |
| **Hourly & Day-of-Week Patterns** | Viewing habits by time of day and weekdays. |
| **Heatmap** | Visualized watch frequency by day and hour. |
| **Longest Binge Day** | Found the day with the highest video count and top creators. |
| **Binge Transitions** | Counted how often I watched videos back-to-back (<30 minutes apart). |
| **Keyword Insights** | Extracted top keywords from video titles. |

## Create environment
```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

## Install requirements (You can refer the one I attached)
```bash
pip install -r requirements.txt
```

## Running the Jupyter Notebook
```bash
jupyter notebook analysis_notebook.ipynb
```


## Running the Streamlit Dashboard
```bash
streamlit run dashboard.py
```

- The app will open at [http://localhost:8501](http://localhost:8501).  
- Ensure `watch-history.json` is in the same folder.  
- You’ll see all **7 charts**:  
  

## Insights Covered
The analysis uncovers trends like:
- Most watched creators & channels  
- Hourly and daily viewing patterns  
- Weekly and monthly time trends  
- Binge-watching sessions  
- Hidden habits (e.g. late-night viewing)  
