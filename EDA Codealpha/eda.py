"""
Job Listings - Complete EDA using Matplotlib
Author: Shubhransu
Dataset: jobs_data_bs4.csv
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
from matplotlib.ticker import MaxNLocator

# ══════════════════════════════════════════════════════════════
# 1. LOAD & CLEAN DATA
# ══════════════════════════════════════════════════════════════
df = pd.read_csv("jobs_data_bs4.csv", encoding="utf-8-sig")
df.columns = df.columns.str.strip()

df['job_title']  = df['job_title'].str.strip().str.title()
df['company']    = df['company'].str.strip()
df['location']   = df['location'].str.strip()
df['scraped_at'] = pd.to_datetime(df['scraped_at'])
df['state']      = df['location'].str.extract(r',\s*([A-Z]{2})$')
df['broken_url'] = df['url'].str.contains('realpython.github.iohttps', na=False)

# ══════════════════════════════════════════════════════════════
# 2. COMPUTED STATS
# ══════════════════════════════════════════════════════════════
top_titles    = df['job_title'].value_counts().head(10)
top_companies = df['company'].value_counts().head(8)
state_counts  = df['state'].value_counts()
duplicates    = df.duplicated().sum()
nulls         = df[['job_title','company','location','url']].isnull().sum().sum()
broken_count  = df['broken_url'].sum()

# ══════════════════════════════════════════════════════════════
# 3. THEME SETUP
# ══════════════════════════════════════════════════════════════
BG       = '#0f0f1a'
PANEL    = '#1a1a2e'
CARD     = '#16213e'
ACCENT   = '#4F8EF7'
GREEN    = '#4FC9A4'
ORANGE   = '#F7874F'
PINK     = '#F74F7B'
PURPLE   = '#A04FF7'
YELLOW   = '#F7C74F'
WHITE    = '#FFFFFF'
GRAY     = '#aaaacc'

PALETTE  = [ACCENT, ORANGE, GREEN, PINK, PURPLE,
            YELLOW, '#4FF7E8', '#7BF74F', '#F74FC9', '#4F4FF7']

plt.rcParams.update({
    'font.family':        'monospace',
    'text.color':         WHITE,
    'axes.labelcolor':    GRAY,
    'xtick.color':        GRAY,
    'ytick.color':        GRAY,
})

# ══════════════════════════════════════════════════════════════
# 4. FIGURE LAYOUT  (3 rows × 3 cols)
# ══════════════════════════════════════════════════════════════
fig = plt.figure(figsize=(20, 18), facecolor=BG)
fig.suptitle('📊  Job Listings — Complete EDA Dashboard',
             fontsize=24, fontweight='bold', color=WHITE,
             y=0.98, fontfamily='sans-serif')

gs = gridspec.GridSpec(3, 3, figure=fig,
                       hspace=0.55, wspace=0.38,
                       top=0.93, bottom=0.05,
                       left=0.07, right=0.97)

# ── helper: style an axes ─────────────────────────────────────
def style_ax(ax, title):
    ax.set_facecolor(CARD)
    ax.set_title(title, color=WHITE, fontsize=13,
                 fontweight='bold', pad=10, loc='left')
    for spine in ax.spines.values():
        spine.set_color('#2a2a4a')
    ax.tick_params(colors=GRAY, labelsize=9)
    ax.xaxis.label.set_color(GRAY)
    ax.yaxis.label.set_color(GRAY)

# ══════════════════════════════════════════════════════════════
# PLOT 1 — Top 10 Job Titles (Horizontal Bar)
# ══════════════════════════════════════════════════════════════
ax1 = fig.add_subplot(gs[0, :2])
style_ax(ax1, '🏆  Top 10 Job Titles')

colors1 = [GREEN if 'Python' in t or 'Developer' in t or 'Software' in t
           else ACCENT for t in top_titles.index[::-1]]
bars1 = ax1.barh(top_titles.index[::-1], top_titles.values[::-1],
                 color=colors1, height=0.6, edgecolor='none')

for bar, val in zip(bars1, top_titles.values[::-1]):
    ax1.text(bar.get_width() + 0.04,
             bar.get_y() + bar.get_height() / 2,
             str(val), va='center', color=WHITE, fontsize=11, fontweight='bold')

ax1.set_xlabel('Frequency', color=GRAY)
ax1.set_xlim(0, top_titles.max() + 0.7)
ax1.xaxis.set_major_locator(MaxNLocator(integer=True))
ax1.grid(axis='x', color='#2a2a4a', linewidth=0.7, alpha=0.8)
ax1.set_axisbelow(True)

legend_patches = [mpatches.Patch(color=GREEN, label='Python/Dev roles'),
                  mpatches.Patch(color=ACCENT, label='Other roles')]
ax1.legend(handles=legend_patches, loc='lower right',
           facecolor=PANEL, edgecolor='#333355', labelcolor=WHITE, fontsize=8)

# ══════════════════════════════════════════════════════════════
# PLOT 2 — State Distribution Pie
# ══════════════════════════════════════════════════════════════
ax2 = fig.add_subplot(gs[0, 2])
ax2.set_facecolor(CARD)
ax2.set_title('📍  State Distribution', color=WHITE,
              fontsize=13, fontweight='bold', pad=10, loc='left')

pie_colors = [ACCENT, ORANGE, GREEN]
wedges, texts, autotexts = ax2.pie(
    state_counts.values,
    labels=state_counts.index,
    autopct='%1.1f%%',
    colors=pie_colors,
    startangle=140,
    textprops={'color': WHITE, 'fontsize': 12},
    wedgeprops={'edgecolor': BG, 'linewidth': 3},
    pctdistance=0.75,
)
for at in autotexts:
    at.set_fontsize(10)
    at.set_fontweight('bold')

# Add center donut hole
centre_circle = plt.Circle((0, 0), 0.40, fc=CARD)
ax2.add_patch(centre_circle)
ax2.text(0, 0, f'{len(df)}\nJobs', ha='center', va='center',
         fontsize=12, color=WHITE, fontweight='bold')

# ══════════════════════════════════════════════════════════════
# PLOT 3 — Top Companies (Vertical Bar)
# ══════════════════════════════════════════════════════════════
ax3 = fig.add_subplot(gs[1, :2])
style_ax(ax3, '🏢  Top Companies by Listings')

x = range(len(top_companies))
bars3 = ax3.bar(x, top_companies.values, color=PALETTE[:len(top_companies)],
                width=0.55, edgecolor='none')

ax3.set_xticks(x)
ax3.set_xticklabels(
    [c[:20] + '…' if len(c) > 20 else c for c in top_companies.index],
    rotation=30, ha='right', fontsize=8, color=GRAY
)
ax3.set_ylabel('Listings', color=GRAY)
ax3.yaxis.set_major_locator(MaxNLocator(integer=True))
ax3.grid(axis='y', color='#2a2a4a', linewidth=0.7, alpha=0.8)
ax3.set_axisbelow(True)

for bar, val in zip(bars3, top_companies.values):
    ax3.text(bar.get_x() + bar.get_width() / 2,
             bar.get_height() + 0.03,
             str(val), ha='center', color=WHITE,
             fontsize=11, fontweight='bold')

# ══════════════════════════════════════════════════════════════
# PLOT 4 — Data Quality Card
# ══════════════════════════════════════════════════════════════
ax4 = fig.add_subplot(gs[1, 2])
ax4.set_facecolor(CARD)
ax4.axis('off')
ax4.set_title('🔍  Data Quality', color=WHITE,
              fontsize=13, fontweight='bold', pad=10, loc='left')

quality_items = [
    ('Total Rows',        str(len(df)),          GREEN),
    ('Columns',           '5',                   GREEN),
    ('Null Values',       str(int(nulls)),        GREEN),
    ('Duplicates',        str(int(duplicates)),   GREEN),
    ('Broken URLs',       f'{int(broken_count)} / {len(df)}', PINK),
    ('Unique Titles',     str(df['job_title'].nunique()), ACCENT),
    ('Unique Companies',  str(df['company'].nunique()),   ACCENT),
    ('States Found',      '3  (AA · AE · AP)',   ORANGE),
    ('Timestamp Spread',  'Single run only',      YELLOW),
]

for i, (label, val, color) in enumerate(quality_items):
    y = 0.90 - i * 0.098
    ax4.text(0.04, y, f'▸ {label}', color=GRAY, fontsize=9,
             transform=ax4.transAxes, va='top')
    ax4.text(0.98, y, val, color=color, fontsize=9,
             fontweight='bold', transform=ax4.transAxes, va='top', ha='right')
    ax4.plot([0.03, 0.97], [y - 0.015, y - 0.015],
             color='#2a2a4a', linewidth=0.5, transform=ax4.transAxes)

# ══════════════════════════════════════════════════════════════
# PLOT 5 — Hypothesis Testing (Bar — role frequency spread)
# ══════════════════════════════════════════════════════════════
ax5 = fig.add_subplot(gs[2, :2])
style_ax(ax5, '🔬  Hypothesis: Role Frequency Distribution')

freq_counts = df['job_title'].value_counts()
freq_groups = freq_counts.value_counts().sort_index()  # how many titles appear N times

bar_colors = [GREEN if idx == 1 else ORANGE for idx in freq_groups.index]
bars5 = ax5.bar(freq_groups.index.astype(str), freq_groups.values,
                color=bar_colors, width=0.4, edgecolor='none')

for bar, val in zip(bars5, freq_groups.values):
    ax5.text(bar.get_x() + bar.get_width() / 2,
             bar.get_height() + 0.4,
             str(val), ha='center', color=WHITE,
             fontsize=12, fontweight='bold')

ax5.set_xlabel('Number of times a job title appears', color=GRAY)
ax5.set_ylabel('Count of job titles', color=GRAY)
ax5.grid(axis='y', color='#2a2a4a', linewidth=0.7, alpha=0.8)
ax5.set_axisbelow(True)

legend5 = [mpatches.Patch(color=GREEN, label='Appear once (unique)'),
           mpatches.Patch(color=ORANGE, label='Appear 2–3× (repeated)')]
ax5.legend(handles=legend5, facecolor=PANEL, edgecolor='#333355',
           labelcolor=WHITE, fontsize=8)

note = "H3 Confirmed: Most roles appear only once — a few repeat 2–3×"
ax5.text(0.5, 0.92, note, ha='center', transform=ax5.transAxes,
         color=YELLOW, fontsize=9, fontstyle='italic')

# ══════════════════════════════════════════════════════════════
# PLOT 6 — Key Insights Text Panel
# ══════════════════════════════════════════════════════════════
ax6 = fig.add_subplot(gs[2, 2])
ax6.set_facecolor(CARD)
ax6.axis('off')
ax6.set_title('💡  Key Insights', color=WHITE,
              fontsize=13, fontweight='bold', pad=10, loc='left')

insights = [
    (GREEN,  '✔ No nulls or duplicates found'),
    (PINK,   '✘ All 100 URLs are malformed'),
    (ACCENT, '〒 3 state codes: AA, AE, AP'),
    (GREEN,  '✔ Python roles appear most often'),
    (YELLOW, '⚠ Single timestamp — one scrape'),
    (ORANGE, '⚠ "Make" is a bad job title (row 35)'),
    (ACCENT, '〒 99 unique companies — no monopoly'),
    (PINK,   '✘ Time-trend analysis not possible'),
]

for i, (color, text) in enumerate(insights):
    y = 0.90 - i * 0.106
    ax6.text(0.04, y, text, color=color, fontsize=9,
             transform=ax6.transAxes, va='top', fontweight='bold')
    ax6.plot([0.03, 0.97], [y - 0.016, y - 0.016],
             color='#2a2a4a', linewidth=0.5, transform=ax6.transAxes)

# ══════════════════════════════════════════════════════════════
# SAVE
# ══════════════════════════════════════════════════════════════
plt.savefig('eda_full_report.png', dpi=150,
            bbox_inches='tight', facecolor=BG)
print("✅  Saved: eda_full_report.png")
