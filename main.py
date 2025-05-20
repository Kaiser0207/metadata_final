import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 載入資料
df = pd.read_csv('TMDB_movie_dataset_v11.csv')

# 排除無用資訊
columns_to_drop = [
    'poster_path', 'backdrop_path', 'homepage', 'imdb_id', 'overview', 'tagline', 'keywords'
]
df.drop(columns=[col for col in columns_to_drop if col in df.columns], inplace=True)

# 檢查資料集的基本資訊(是否完整)
print("\nMissing Values Before Handling:\n", df.isnull().sum())
df[['genres', 'title','original_title','release_date', 'production_companies', 'production_countries', 'spoken_languages']] = df[['genres', 'title','original_title','release_date', 'production_companies', 'production_countries', 'spoken_languages']].fillna('Unknown')
print("\nMissing Values Before Handling:\n", df.isnull().sum())

# 移除重複值
df.drop_duplicates(inplace=True)
print("\nDuplicate Rows After Removal:", df.duplicated().sum())

# 預處理 release_date，並提取年份
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
df['release_year'] = df['release_date'].dt.year

# ==============================
# 排除異常值
# ==============================
df_clean = df.copy()

# 濾掉 budget, revenue 為 0 的資料
df_clean = df_clean[(df_clean['budget'] > 0) & (df_clean['revenue'] > 0)]
# 濾掉 runtime 小於 30 分鐘的資料
df_clean = df_clean[df_clean['runtime'] >= 30]
# 濾掉 release_year 為 NaN 的資料
df_clean = df_clean[df_clean['release_year'].notna()]
df_clean = df_clean[df_clean['release_year'] >= 1950]
df_clean = df_clean[df_clean['release_year'] <= 2023]

# ==============================
# 1. 平均電影長度是否逐年上升？
# ==============================

yearly_runtime = df_clean.groupby('release_year')['runtime'].mean()

plt.figure(figsize=(12,6))
sns.lineplot(x=yearly_runtime.index, y=yearly_runtime.values, color='purple', marker='o')
plt.title('Average Movie Runtime Over the Years', fontsize=16)
plt.xlabel('Release Year', fontsize=14)
plt.ylabel('Average Runtime (minutes)', fontsize=14)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# ==============================
# 2. 電影是否越來越難賺錢？（平均預算 vs 平均收入）
# ==============================

yearly_money = df_clean.groupby('release_year')[['budget', 'revenue']].mean()

plt.figure(figsize=(12,6))
sns.lineplot(x=yearly_money.index, y=yearly_money['budget'], label='Average Budget', marker='o', color='gray')
sns.lineplot(x=yearly_money.index, y=yearly_money['revenue'], label='Average Revenue', marker='o', color='orange')
plt.title('Average Budget vs Revenue Over the Years', fontsize=16)
plt.xlabel('Release Year', fontsize=14)
plt.ylabel('Amount (USD)', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# ==============================
# 3. 額外：平均「淨利」變化趨勢
# ==============================

df_clean['profit'] = df_clean['revenue'] - df_clean['budget']
yearly_profit = df_clean.groupby('release_year')['profit'].mean()

plt.figure(figsize=(12,6))
sns.lineplot(x=yearly_profit.index, y=yearly_profit.values, color='green', marker='o')
plt.title('Average Movie Profit Over the Years', fontsize=16)
plt.xlabel('Release Year', fontsize=14)
plt.ylabel('Average Profit (USD)', fontsize=14)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# ==============================
# 4.電影數量隨時間變化
# ==============================

plt.figure(figsize=(12,6))
sns.histplot(df['release_year'].dropna(), bins=50, kde=True, color='blue')
plt.xlabel('Year')
plt.ylabel('Number of Movies')
plt.title('Number of Movies Released Over the Years')
plt.xlim(1950, 2025)
plt.show()

# ==============================
# 5.電影類型與收入的關係
# ==============================
# 取出前10個類型
df['first_genre'] = df['genres'].apply(lambda x: x.split(",")[0] if isinstance(x, str) else "Unknown")
genre_revenue = df.groupby('first_genre')['revenue'].mean().sort_values(ascending=False).head(10)

plt.figure(figsize=(12,6))
sns.barplot(x=genre_revenue.index, y=genre_revenue.values, palette='viridis')
plt.xlabel('Genre')
plt.ylabel('Average Revenue')
plt.title('Top 10 Most Profitable Genres')
plt.xticks(rotation=45)
plt.show()
