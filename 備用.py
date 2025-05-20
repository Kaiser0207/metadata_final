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

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# 讀取電影資料
df = pd.read_csv('movies.csv')
df.info()      # 顯示資料欄位與型態
df.describe()  # 顯示數值欄位的統計摘要

# 分析各類型電影的平均票房與平均評分人數
df['genre'].nunique()  # 計算不同類型數量
genre_analysis = df.groupby('genre')[['gross', 'votes']].mean().sort_values(by='gross', ascending=False)

# 計算每年平均利潤
df['profit'] = df['gross'] - df['budget']
profit_by_year = df.groupby('year')['profit'].mean()
plt.figure(figsize=(8, 5))
profit_by_year.plot(marker='o', color='purple')
plt.title('Average Profit by Year', fontsize=16)
plt.xlabel('Year', fontsize=14)
plt.ylabel('Average Profit', fontsize=14)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# 平均票房最高的前 10 名導演
top_directors = df.groupby('director')['gross'].mean().sort_values(ascending=False).head(10)
plt.figure(figsize=(8, 5))
top_directors.plot(kind='bar', color='darkgreen')
plt.title('Top 10 Directors by Average Gross', fontsize=16)
plt.xlabel('Director', fontsize=14)
plt.ylabel('Average Gross', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# 平均評分最高的前 10 名演員
top_stars = df.groupby('star')['votes'].mean().sort_values(ascending=False).head(10)
plt.figure(figsize=(8, 5))
top_stars.plot(kind='bar', color='steelblue')
plt.title('Top 10 Stars by Average Votes', fontsize=16)
plt.xlabel('Star', fontsize=14)
plt.ylabel('Average Votes', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# 計算每年平均評分
refined_rating_map = {
    'TV-Y': 'Kids (0–6)',
    'TV-Y7': 'Kids (7+)',
    'TV-Y7-FV': 'Kids (7+)',
    'TV-G': 'General Family',
    'G': 'General Family',
    'PG': 'Parental Guidance',
    'PG-13': '13+',
    'TV-PG': '13+',
    'TV-14': '13+',
    'GP': '13+',
    'R': '18+',
    'TV-MA': '18+',
    'NC-17': '18+',
    'X': '18+',
    'M': '18+',
    'Approved': 'General Family',
    'Passed': 'General Family',
    'Not Rated': 'Unknown',
    'Unrated': 'Unknown'
}
# 替換分類
df['refined_rating'] = df['rating'].map(refined_rating_map)
df_clean = df.dropna(subset=['score'])
df_clean = df_clean[df_clean['refined_rating'] != 'Unknown']
# 分組計算平均評分
score_by_refined_rating = df_clean.groupby('refined_rating')['score'].mean().sort_values(ascending=False)
plt.figure(figsize=(8, 5))
score_by_refined_rating.plot(kind='bar', color='lightseagreen')
plt.title('Average Score by Refined Rating Group', fontsize=16)
plt.xlabel('Rating Group', fontsize=14)
plt.ylabel('Average Score', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()



# 計算每個國家的平均預算與票房
country_data = df.groupby('country')[['budget', 'gross']].mean().sort_values(by='gross', ascending=False).head(10)
country_data.plot(kind='bar', figsize=(10, 6), color=['gray', 'orange'])
plt.title('Top 10 Countries: Average Budget vs Gross', fontsize=16)
plt.xlabel('Country', fontsize=14)
plt.ylabel('Amount', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.legend(['Average Budget', 'Average Gross'], fontsize=12)
plt.tight_layout()
plt.show()

# 計算預算與票房的相關性
plt.figure(figsize=(8, 6))
corr = df[['budget', 'gross', 'votes', 'score']].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", square=True)
plt.title("Correlation Heatmap of Numeric Features", fontsize=16)
plt.tight_layout()
plt.show()

# 電影有沒有越拍越長
year_runtime = df.groupby('year')['runtime'].mean()
plt.figure(figsize=(10, 6))
year_runtime.plot(kind='line', marker='o', color='purple')
plt.title('Average Movie Runtime Over the Years', fontsize=16)
plt.xlabel('Year', fontsize=14)
plt.ylabel('Average Runtime (minutes)', fontsize=14)
plt.grid(True, alpha=0.5)
plt.tight_layout()
plt.show()

