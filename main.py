import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import mplcursors
# Kumulativni Dohodek 12/24 mesecev

# Assuming your Excel file has columns: year, month, income
df = pd.read_excel('dohodki.xlsx', names=['year', 'month', 'income'])

# Convert date columns
df["date"] = pd.to_datetime(df[["year", "month"]].assign(day=1))
df = df.sort_values("date").reset_index(drop=True)

# Strip leading and trailing rows with income 0
non_zero = df[df["income"] != 0]
if not non_zero.empty:
    first_non_zero = non_zero.index[0]
    last_non_zero = non_zero.index[-1]
    df = df.loc[first_non_zero:last_non_zero].reset_index(drop=True)

# Compute rolling cumulative income
df["cumulative_income_12"] = df["income"].rolling(window=12, min_periods=1).sum()
df["cumulative_income_24"] = df["income"].rolling(window=24, min_periods=1).sum()

# Dark mode styling
plt.style.use("dark_background")

# Create subplots
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(12, 10), sharex=True)

# Colors
income_color = "#00bfff"  # Light blue
cum_income_12_color = "#ff4500"  # Orange-red
cum_income_24_color = "#32cd32"  # Lime green
line_color_12 = "#ff6347"  # Tomato
line_color_24 = "#00ff00"  # Green

# Plot income and cumulative income (12 months) on first subplot
ax1 = axes[0]
ax1.plot(df["date"], df["income"], marker="o", linestyle="-", label="Income", color=income_color, linewidth=2, markersize=6)
ax1.set_ylabel("Income (€)", color=income_color, fontsize=12, fontweight="bold")
ax1.tick_params(axis="y", labelcolor=income_color)
ax2 = ax1.twinx()  # Second y-axis for cumulative income (12 months)
line1, = ax2.plot(df["date"], df["cumulative_income_12"], marker="s", linestyle="--", label="Cumulative Income (12 months)", color=cum_income_12_color, linewidth=2, markersize=6)
ax2.set_ylabel("Cumulative Income (12 months)", color=cum_income_12_color, fontsize=12, fontweight="bold")
ax2.tick_params(axis="y", labelcolor=cum_income_12_color)
ax2.axhline(y=60000, color=line_color_12, linestyle='-', linewidth=2, label='60000 €')
ax1.legend(loc='upper left', fontsize=11, frameon=True, facecolor="#222", edgecolor="white")
ax2.legend(loc='upper right', fontsize=11, frameon=True, facecolor="#222", edgecolor="white")

# Highlight maximum cumulative income (12 months)
max_cum_income_12 = df["cumulative_income_12"].max()
max_date_12 = df["date"][df["cumulative_income_12"].idxmax()]
ax2.annotate(f"Max: {max_cum_income_12:.0f} €",
             xy=(max_date_12, max_cum_income_12),
             xytext=(max_date_12, max_cum_income_12 + 5000),
             arrowprops=dict(facecolor='white', shrink=0.05),
             fontsize=12, fontweight="bold", color="white")

# Plot income and cumulative income (24 months) on second subplot
ax3 = axes[1]
ax3.plot(df["date"], df["income"], marker="o", linestyle="-", label="Income", color=income_color, linewidth=2, markersize=6)
ax3.set_ylabel("Income (€)", color=income_color, fontsize=12, fontweight="bold")
ax3.tick_params(axis="y", labelcolor=income_color)
ax4 = ax3.twinx()  # Second y-axis for cumulative income (24 months)
line2, = ax4.plot(df["date"], df["cumulative_income_24"], marker="^", linestyle="-.", label="Cumulative Income (24 months)", color=cum_income_24_color, linewidth=2, markersize=6)
ax4.set_ylabel("Cumulative Income (24 months)", color=cum_income_24_color, fontsize=12, fontweight="bold")
ax4.tick_params(axis="y", labelcolor=cum_income_24_color)
ax4.axhline(y=120000, color=line_color_24, linestyle='-', linewidth=2, label='120000 €')
ax3.legend(loc='upper left', fontsize=11, frameon=True, facecolor="#222", edgecolor="white")
ax4.legend(loc='upper right', fontsize=11, frameon=True, facecolor="#222", edgecolor="white")

# Highlight maximum cumulative income (24 months)
max_cum_income_24 = df["cumulative_income_24"].max()
max_date_24 = df["date"][df["cumulative_income_24"].idxmax()]
ax4.annotate(f"Max: {max_cum_income_24:.0f} €",
             xy=(max_date_24, max_cum_income_24),
             xytext=(max_date_24, max_cum_income_24 + 5000),
             arrowprops=dict(facecolor='white', shrink=0.05),
             fontsize=12, fontweight="bold", color="white")

# Format x-axis to display only every third month
ax3.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
ax3.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
plt.xticks(rotation=45, fontsize=11, fontweight="bold", color="white")

# Titles and labels
ax1.set_title("Income and Cumulative Income (12 months)", fontsize=14, fontweight="bold", color="white")
ax3.set_title("Income and Cumulative Income (24 months)", fontsize=14, fontweight="bold", color="white")
fig.tight_layout()

# Enable interactive tooltips
cursor1 = mplcursors.cursor(line1, hover=True)
cursor2 = mplcursors.cursor(line2, hover=True)

# Format tooltip display
@cursor1.connect("add")
def on_hover(sel):
    sel.annotation.set_text(f"{sel.target[1]:,.0f} €")
    sel.annotation.get_bbox_patch().set(fc="black", alpha=0.7)

@cursor2.connect("add")
def on_hover(sel):
    sel.annotation.set_text(f"{sel.target[1]:,.0f} €")
    sel.annotation.get_bbox_patch().set(fc="black", alpha=0.7)

# Show the plot
plt.show()