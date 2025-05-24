import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.gridspec as gridspec
from matplotlib.lines import Line2D


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
df_clean = df.copy() #

# 濾掉 budget, revenue 為 0 的資料
df_clean = df_clean[(df_clean['budget'] > 0) & (df_clean['revenue'] > 0)]
# 濾掉 runtime 小於 45 分鐘的資料
df_clean = df_clean[df_clean['runtime'] >= 45]
# 濾掉 release_year 為 NaN 的資料
df_clean = df_clean[df_clean['release_year'].notna()]
df_clean = df_clean[df_clean['release_year'] >= 1990]
df_clean = df_clean[df_clean['release_year'] <= 2023]

# ==============================
# 平均電影長度是否逐年上升？
# ==============================

# 計算平均片長
yearly_runtime = df_clean.groupby('release_year')['runtime'].mean()

# 取收入前10名電影
top10_revenue_movies = df_clean.sort_values(by='revenue', ascending=False).head(10).copy()

# 為每部電影分配一種顏色
colors = sns.color_palette("tab10", n_colors=10)
top10_revenue_movies['color'] = colors

plt.figure(figsize=(16,6))  # 拉長寬度給右側標註用
gs = gridspec.GridSpec(1, 2, width_ratios=[4, 1])  # 左邊圖大，右邊圖小

# ========== 左邊主圖 ==========
ax0 = plt.subplot(gs[0])
sns.lineplot(x=yearly_runtime.index, y=yearly_runtime.values, color='purple', marker='o', label='Average Runtime', ax=ax0)

# 畫出收入前10名電影的點（不同顏色）
for idx, row in top10_revenue_movies.iterrows():
    ax0.scatter(row['release_year'], row['runtime'], color=row['color'], s=100, edgecolor='black')

ax0.set_title('Average Movie Runtime Over the Years\nwith Top 10 Revenue Movies Highlighted', fontsize=16)
ax0.set_xlabel('Release Year', fontsize=14)
ax0.set_ylabel('Runtime (minutes)', fontsize=14)
ax0.set_yticks(np.arange(100, 200, 5))  # 每5分鐘一格
ax0.grid(True, alpha=0.3)

# ========== 右側說明欄（圖例樣式） ==========
ax1 = plt.subplot(gs[1])
ax1.axis('off')  # 不顯示軸

# 顯示電影名稱與對應顏色點
for i, (_, row) in enumerate(top10_revenue_movies.iterrows()):
    ax1.scatter(0, 10 - i, color=row['color'], s=100)  # 畫點
    ax1.text(0.01, 10 - i, f"{i+1}.{row['title']}", fontsize=10, va='center')  # 顯示文字

#儲存照片
plt.savefig('average_runtime_over_years.png')
plt.tight_layout()
plt.show()

# ==============================
# 2. 電影是否越來越難賺錢？（平均預算 vs 平均收入 vs 净利润）
# ==============================

# 計算年度平均預算與收入
yearly_money = df_clean.groupby('release_year')[['budget', 'revenue']].mean()

# 計算年度平均淨利
df_clean['profit'] = df_clean['revenue'] - df_clean['budget']
yearly_profit = df_clean.groupby('release_year')['profit'].mean()

# 創建子圖
fig, axes = plt.subplots(2, 1, figsize=(12, 12), sharex=True)

# 子圖1：預算 vs 收入折線圖
sns.lineplot(ax=axes[0], x=yearly_money.index, y=yearly_money['budget'], label='Average Budget', marker='o', color='gray')
sns.lineplot(ax=axes[0], x=yearly_money.index, y=yearly_money['revenue'], label='Average Revenue', marker='o', color='orange')
axes[0].set_title('Average Budget vs Revenue Over the Years', fontsize=16)
axes[0].set_ylabel('Amount (USD)', fontsize=14)
axes[0].legend(fontsize=12)
axes[0].grid(True, alpha=0.3)

# 子圖2：平均淨利柱狀圖
axes[1].bar(yearly_profit.index, yearly_profit.values, color='green')
axes[1].set_title('Average Movie Profit Over the Years', fontsize=16)
axes[1].set_xlabel('Release Year', fontsize=14)
axes[1].set_ylabel('Average Profit (USD)', fontsize=14)
axes[1].grid(True, axis='y', alpha=0.3)

#儲存照片
plt.savefig('average_budget_revenue_profit_over_years.png')
# 自動調整布局
plt.tight_layout()
plt.show()

# ==============================
# 電影類型與预算收入的關係
# ==============================

df['first_genre'] = df['genres'].apply(lambda x: x.split(",")[0] if isinstance(x, str) else "Unknown")

# 計算所有類型的平均收入
all_genre_revenue = df.groupby('first_genre')['revenue'].mean().sort_values(ascending=False)

# 選出前 10 個
top10_genre_revenue = all_genre_revenue.head(10)

# 計算其他類型的平均收入總和
others_sum = all_genre_revenue.iloc[10:].sum()

# 將 "Others" 加入資料中
top10_plus_others = top10_genre_revenue.copy()
top10_plus_others['Others'] = others_sum

# 畫圖：新的圓餅圖（所有類型佔比 + Others）
fig, axs = plt.subplots(1, 2, figsize=(16, 6))

color = sns.color_palette('viridis', n_colors=len(top10_plus_others))

wedges, texts, autotexts = axs[0].pie(
    top10_plus_others.values,
    labels=None,  # 不直接標籤
    autopct='%1.1f%%',
    startangle=140,
    colors=color,
    textprops={'fontsize': 9}
)

# 加上圖例
axs[0].legend(wedges, top10_plus_others.index, title="Genres", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

axs[0].set_title('Revenue Share by Genre (Top 10 + Others)')
axs[0].axis('equal')  # 保持圓形

# 右圖照舊：前 10 類型的平均成本與收入
bar_width = 0.4
x = range(len(top10_genre_revenue.index))

# 成本與收入統計資料
genre_stats = df[df['first_genre'].isin(top10_genre_revenue.index)].groupby('first_genre')[['revenue', 'budget']].mean().loc[top10_genre_revenue.index]

axs[1].bar([i - bar_width/2 for i in x], genre_stats['budget'], width=bar_width, label='Average Budget', color='skyblue')
axs[1].bar([i + bar_width/2 for i in x], genre_stats['revenue'], width=bar_width, label='Average Revenue', color='darkgreen')

axs[1].set_xticks(x)
axs[1].set_xticklabels(genre_stats.index, rotation=45)
axs[1].set_ylabel('Amount (Same Scale)')
axs[1].set_title('Average Budget and Revenue by Genre (Top 10)')
axs[1].legend()

#儲存照片
plt.savefig('genre_revenue_budget_analysis.png')
plt.tight_layout()
plt.show()
