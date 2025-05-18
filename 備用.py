import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# 讀取電影資料
df = pd.read_csv('movies.csv')
df.info()      # 顯示資料欄位與型態
df.describe()  # 顯示數值欄位的統計摘要

# 計算每年平均預算與票房
avg_budget_gross = df.groupby('year')[['budget', 'gross']].mean()
plt.figure(figsize=(6, 4))
plt.plot(avg_budget_gross.index, avg_budget_gross['budget'], label='Average Budget', marker='o', color='b')
plt.plot(avg_budget_gross.index, avg_budget_gross['gross'], label='Average Gross Revenue', marker='o', color='r')
plt.title("Average Budget and Gross Revenue Over the Years", fontsize=16)
plt.xlabel("Year", fontsize=14)
plt.ylabel("Amount (in dollars)", fontsize=14)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.6)
plt.show()

# 分析各類型電影的平均票房與平均評分人數
df['genre'].nunique()  # 計算不同類型數量
genre_analysis = df.groupby('genre')[['gross', 'votes']].mean().sort_values(by='gross', ascending=False)

# 繪製各類型平均票房長條圖
plt.figure(figsize=(8, 6))
genre_analysis['gross'].sort_values(ascending=False).plot(kind='bar', color='green')
plt.title("Most Popular Genres (Based on Gross Revenue)", fontsize=16)
plt.xlabel("Genre", fontsize=14)
plt.ylabel("Average Gross Revenue", fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# 繪製各類型平均評分人數長條圖
plt.figure(figsize=(8, 6))
genre_analysis['votes'].sort_values(ascending=False).plot(kind='bar', color='blue')
plt.title("Most Popular Genres (Based on Votes)", fontsize=16)
plt.xlabel("Genre", fontsize=14)
plt.ylabel("Average Votes", fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# 統計各分級電影數量並繪製長條圖
rating_counts = df['rating'].value_counts()
plt.figure(figsize=(6, 4))
rating_counts.plot(kind='bar', color='skyblue')
plt.title("Most Common Movie Ratings", fontsize=16)
plt.xlabel("Rating", fontsize=14)
plt.ylabel("Number of Movies", fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

movies_by_country = df['country'].value_counts().head(10)
plt.figure(figsize=(6, 4))
movies_by_country.plot(kind='bar', color='orange')
plt.title("Top 10 Movie-Producing Countries", fontsize=16)
plt.xlabel("Country", fontsize=14)
plt.ylabel("Number of Movies", fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

genre_counts = df['genre'].value_counts()
plt.figure(figsize=(6, 4))
sns.barplot(x=genre_counts.values, y=genre_counts.index, palette='viridis')
plt.title("Most Common Movie Genres", fontsize=16)
plt.xlabel("Number of Movies", fontsize=14)
plt.ylabel("Genres", fontsize=14)
plt.grid(alpha=0.3)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()