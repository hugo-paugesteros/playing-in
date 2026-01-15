import sys

sys.path.append("/home/hugo/Thèse/mocap/")

from take import Take
import matplotlib.pyplot as plt
from pathlib import Path
from config import mm, colors, ci, VIOLIN_MAP, SCOPES_MAP, CRITERION_MAP
import pandas as pd
import seaborn as sns
import pathlib
import numpy as np

bad = [
    "own_P1_open_strings_1.csv",
    "own_P1_glazounov_1.csv",
    "stoppani_P1_tchaikovsky_3.csv",
]

VIOLINS = ["klimke", "own", "stoppani"]
EXCERPTS = [
    "open_strings",
    "bach",
    "tchaikovsky",
    "glazounov",
]

VALIDITY = {
    "long_sustained_note": [],
    "open_strings": [170, 3000],
    "bach": [100, 850],
    "tchaikovsky": [100, 1860],
    "glazounov": [170, 2600],
}

DESCRIPTORS = ["vs", "xs", "hairstring", "tilt", "skewness", "beta"]
UNITS = {
    "vs": "mm/s",
    "xs": "mm",
    "hairstring": "mm",
    "tilt": "",
    "skewness": "",
    "beta": "mm",
}
descriptor = "skewness"

base_path = Path("data/raw/mocap/")


def build_dataset():
    data_frames = []
    for i, excerpt in enumerate(EXCERPTS):
        first_take = None

        for j, violin in enumerate(VIOLINS):
            for phase in [1, 2]:
                path = base_path / f"phase_{phase}" / violin / excerpt
                files = list(path.glob("*.csv"))
                for file in files[:]:
                    print(file)
                    if str(file.name) in bad:
                        print(f"bad : {file.name}")
                        continue

                    take = Take(file)

                    if first_take is None:
                        first_take = take
                    else:
                        take.align(first_take)
                        pass

                    time = first_take.df_time["Frame"].to_numpy()
                    if VALIDITY[excerpt]:
                        start, end = VALIDITY[excerpt]
                        valid = (time > start) & (time < end)
                    else:
                        valid = time > 0

                    compute_func = getattr(take, f"compute_{descriptor}", None)

                    t_vals = time[valid]
                    t_vals = np.arange(len(t_vals)) / 120
                    f_vals = take.warp(compute_func())[valid]

                    df_tmp = pd.DataFrame({"time": t_vals, "feature": f_vals})

                    df_tmp["violin"] = violin
                    df_tmp["excerpt"] = excerpt
                    df_tmp["phase"] = phase

                    data_frames.append(df_tmp)

    df = pd.concat(data_frames, ignore_index=True)
    print(df)
    df.to_csv("test.csv")


build_dataset()

df = pd.read_csv("test.csv")
df_diff = pd.merge(
    df[df["phase"] == 2],
    df[df["phase"] == 1],
    on=["violin", "excerpt", "time"],
    suffixes=("_p2", "_p1"),
)
df_diff["difference"] = df_diff["feature_p2"] - df_diff["feature_p1"]


fig, axes = plt.subplots(
    nrows=len(VIOLINS) + 1,
    ncols=len(EXCERPTS),
    sharex="col",
    sharey="row",
)

for i, violin in enumerate(VIOLINS):
    for j, excerpt in enumerate(EXCERPTS):
        ax = axes[i, j]

        sns.lineplot(
            data=df[(df["violin"] == violin) & (df["excerpt"] == excerpt)],
            x="time",
            y="feature",
            hue="phase",
            errorbar=ci,
            estimator="mean",
            palette=[colors[1], colors[2]],
            ax=ax,
            err_kws={"linewidth": 0},
        )

        if i == 0:
            ax.set_title(excerpt.replace("_", " ").title())

        if j == 0:
            ax.sharey(axes[0, 0])
            ax.set_ylabel(f"{VIOLIN_MAP[violin]}\n{descriptor} ({UNITS[descriptor]})")
        ax.get_legend().remove()

# --- 3.2 Row 4 : Differences ---
for j, excerpt in enumerate(EXCERPTS):
    ax = axes[-1, j]
    sns.lineplot(
        data=df_diff[df_diff["excerpt"] == excerpt],
        x="time",
        y="difference",
        hue="violin",
        errorbar=ci,
        estimator="mean",
        ax=ax,
        err_kws={"linewidth": 0},
    )
    ax.set_xlabel("Time (s)")
    ax.get_legend().remove()
axes[-1, 0].set_ylabel("Diff (P2 - P1)")

# Styling
for ax in axes.flat:
    ax.grid(True, which="both", alpha=0.3)

# --- 3.4 Legends ---
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
    ["Klimke", "Test player's", "Stoppani"],
    title="Violin",
    loc="center left",
    bbox_to_anchor=(1.02, 0.5),
    borderaxespad=0,
)

fig.tight_layout()
# --- 4. Saving Figure ---
output_png = pathlib.Path(f"reports/figures/mocap_{descriptor}.png")
output_svg = pathlib.Path(f"reports/figures/mocap_{descriptor}.svg")
output_png.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(output_png)
plt.savefig(output_svg)
print(f"Figures saved to {output_png} and {output_svg}")
