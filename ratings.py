import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pathlib
from config import mm, colors


def ci(a):
    m = np.mean(a)
    s = 1.96 * np.std(a) / np.sqrt(len(a))
    return m - s, m + s


# --- Load Data (Same as before) ---
df = pd.read_csv("data/processed/ratings.csv")

CRITERION_MAP = {
    "P": "Power",
    "F": "Ease of Playing",
    "T": "Tone",
}


VIOLIN_MAP = {
    "Klimke": "Klimke (Test)",
    "Levaggi": "Levaggi (Control)",
    "Stoppani": "Stoppani (Control)",
}


SCOPE_MAP = {"control": "Control group", "test": "Test violinist"}

# Create pretty columns upfront to simplify plotting logic later
df["scope_pretty"] = df["scope"].map(SCOPE_MAP)
df["criterion_pretty"] = df["criterion"].map(CRITERION_MAP)
df["violin_pretty"] = df["violin"].map(VIOLIN_MAP)

# --- Configuration ---
sns.set_theme(style="whitegrid")
mpl.style.use("/home/hugo/Thèse/common/styles.mplstyle")

WIDTH = 190 * mm  # Total width
RATIO = 4 / 3
NUM_ROWS = 4  # 3 Violins + 1 Manual Row
NUM_COLS = 3

# Define the grid layout manually
# sharex='col' keeps columns aligned, sharey='row' allows the new row to have different Y-scale if needed
fig, axes = plt.subplots(
    nrows=NUM_ROWS,
    ncols=NUM_COLS,
    figsize=(WIDTH, WIDTH / RATIO),  # Adjust height calculation
    sharex="col",
    sharey="row",
)

# Lists to iterate over for the standard part
violins = list(VIOLIN_MAP.values())
criteria = list(CRITERION_MAP.values())

# --- 1. Automated Plotting (First 3 Rows) ---
for i, violin in enumerate(violins):
    for j, criterion in enumerate(criteria):
        ax = axes[i, j]

        # Filter data for this specific cell
        subset = df[
            (df["violin_pretty"] == violin) & (df["criterion_pretty"] == criterion)
        ]

        # Stripplot
        sns.stripplot(
            data=subset,
            x="scope_pretty",
            y="rating",
            hue="phase",
            dodge=True,
            alpha=0.2,
            palette=[colors[1], colors[2]],
            order=["Control group", "Test violinist"],
            hue_order=[1, 2],
            legend=False,
            ax=ax,
        )

        # Pointplot
        sns.pointplot(
            data=subset,
            x="scope_pretty",
            y="rating",
            hue="phase",
            errorbar=ci,
            estimator="mean",
            dodge=0.2,
            linestyle="none",
            palette=[colors[1], colors[2]],
            order=["Control group", "Test violinist"],
            hue_order=[1, 2],
            ax=ax,
            # legend=False,
        )

        ax.set_xlabel("")
        ax.get_legend().remove()

        # Y-labels only on the left column
        if j == 0:
            ax.sharey(axes[0, 0])
            ax.set_ylabel(f"{violin}\nRating (0-10)")
        else:
            ax.set_ylabel("")

        # Titles only on the top row
        if i == 0:
            ax.set_title(criterion)

# --- 2. Manual Plotting (The New 4th Row) ---
manual_axes = axes[3, :]
for j, ax in enumerate(manual_axes):
    criterion = criteria[j]
    subset = df[(df["criterion_pretty"] == criterion)]

    mean = subset.groupby(["scope_pretty", "violin_pretty", "phase", "player"])[
        "rating"
    ].agg("mean")
    df_pivoted = mean.unstack(level="phase")
    diff = df_pivoted[2] - df_pivoted[1]
    df_diff = diff.reset_index(name="rating")
    sns.pointplot(
        data=df_diff,
        x="scope_pretty",
        y="rating",
        hue="violin_pretty",
        palette=[colors["klimke"], colors["levaggi"], colors["stoppani"]],
        ax=ax,
        linestyle="none",
        errorbar=ci,
        dodge=0.4,
    )
    ax.get_legend().remove()
    if j == 0:
        ax.set_ylabel(f"Rating difference")
    else:
        ax.set_ylabel("")

    ax.set_xlabel("")

# --- 3. Final Polish ---
target_ax = axes[1, -1]
handles_top, labels_top = target_ax.get_legend_handles_labels()
target_ax.legend(
    handles_top[:2],
    labels_top[:2],
    title="Phase",
    loc="center left",
    bbox_to_anchor=(1.02, 0.5),
    borderaxespad=0,
)

target_ax = axes[-1, -1]
handles_top, labels_top = target_ax.get_legend_handles_labels()
target_ax.legend(
    handles_top[:3],
    ["Klimke", "Levaggi", "Stoppani"],
    title="Violin",
    loc="center left",
    bbox_to_anchor=(1.02, 0.5),
    borderaxespad=0,
)


plt.tight_layout()
plt.subplots_adjust(right=0.9)

output_png = pathlib.Path("reports/figures/ratings.png")
output_svg = pathlib.Path("reports/figures/ratings.svg")
output_png.parent.mkdir(parents=True, exist_ok=True)

plt.savefig(output_png)
plt.savefig(output_svg)
plt.show()
print(f"Figures saved to {output_png} and {output_svg}")
