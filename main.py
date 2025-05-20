import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 載入資料
df = pd.read_csv('TMDB_movie_dataset_v11.csv')

# 預處理 release_date，並提取年份
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
df['release_year'] = df['release_date'].dt.year

# 濾除未填年份或異常年份
df = df[(df['release_year'] >= 1950) & (df['release_year'] <= 2025)]

# ====================================================
# 1. 平均電影長度是否逐年上升？
# ====================================================
yearly_runtime = df.groupby('release_year')['runtime'].mean().dropna()

plt.figure(figsize=(12,6))
sns.lineplot(x=yearly_runtime.index, y=yearly_runtime.values, color='purple', marker='o')
plt.title('Average Movie Runtime Over the Years', fontsize=16)
plt.xlabel('Release Year', fontsize=14)
plt.ylabel('Average Runtime (minutes)', fontsize=14)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# ====================================================
# 2. 電影是否越來越難賺錢？（平均預算 vs 平均收入）
# ====================================================
yearly_money = df.groupby('release_year')[['budget', 'revenue']].mean().dropna()

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

# ====================================================
# 3. 額外：平均「淨利」變化趨勢
# ====================================================
df['profit'] = df['revenue'] - df['budget']
yearly_profit = df.groupby('release_year')['profit'].mean().dropna()

plt.figure(figsize=(12,6))
sns.lineplot(x=yearly_profit.index, y=yearly_profit.values, color='green', marker='o')
plt.title('Average Movie Profit Over the Years', fontsize=16)
plt.xlabel('Release Year', fontsize=14)
plt.ylabel('Average Profit (USD)', fontsize=14)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
