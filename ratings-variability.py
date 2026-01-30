import argparse
import pathlib
import warnings
from typing import Optional, Tuple

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import pandas as pd
import seaborn as sns

from config import mm, colors, ci, VIOLIN_MAP, SCOPES_MAP, CRITERION_MAP

VIOLINS = ["klimke", "levaggi", "stoppani"]
SCOPES = ["control", "test"]
CRITERION = ["P", "F", "T"]

PROCESSED_DATA_PATH = pathlib.Path("data/processed/ratings.csv")

colors = {
    1: "#9EcAE1",
    2: "#4292C6",
    3: "#08519C",
    "klimke": "#7570B3",
    "levaggi": "#D95F02",
    "stoppani": "#1B9E77",
    "own": "C1",
}

colors = [
    "#b4b1d5",
    "#7570B3",
    "#fd9241",
    "#D95F02",
    "#3edeae",
    "#1B9E77",
]


def plot(dataset_path: pathlib.Path):
    # --- 1. Load Data (Pandas) ---
    df = pd.read_csv(dataset_path)

    # --- 2. Compute difference ---
    pivoted = df.pivot_table(
        index=["scope", "violin", "player", "criterion"],
        columns="session",
        values="rating",
        aggfunc="mean",  # Handles duplicate ratings if any
    )
    pivoted["2-1"] = pivoted[2] - pivoted[1]
    pivoted["3-1"] = pivoted[3] - pivoted[1]
    df_flat = pivoted[["2-1", "3-1"]].reset_index()
    df_flat = df_flat.dropna(subset=["2-1", "3-1"])
    df_diff = df_flat.melt(
        id_vars=["scope", "violin", "player", "criterion"],  # Identifiers to keep
        value_vars=["2-1", "3-1"],  # Columns to unpivot
        var_name="difference_type",  # Name for the new categorical column
        value_name="difference",  # Name for the new value column
    )
    df_diff["difference_abs"] = np.abs(df_diff["difference"])

    control_players = sorted(df_diff[df_diff["scope"] == "control"]["player"].unique())
    test_players = df_diff[df_diff["scope"] == "test"]["player"].unique()
    player_order = list(control_players) + list(test_players)

    # --- 3. Plotting ---
    fig, axes = plt.subplots(
        nrows=len(CRITERION),
        ncols=2,
        sharex="col",
        sharey=True,
        width_ratios=[len(player_order), 1],
    )

    # A. Main Grid (Violin vs Violinist)
    for i, criterion in enumerate(CRITERION):
        ax = axes[i, 0]

        # Filter data for this specific cell
        subset = df_diff[
            (df_diff["criterion"] == criterion) & (df_diff["difference_type"] == "2-1")
        ]

        # Stripplot
        sns.pointplot(
            data=subset,
            x="player",
            y="difference",
            hue="violin",
            order=player_order,
            # alpha=0.2,
            palette=colors[::2],
            # order=["control", "test"],
            hue_order=["Klimke", "Levaggi", "Stoppani"],
            # legend=False,
            ax=ax,
            dodge=0.3,
            linestyle="none",
        )

        sns.pointplot(
            data=subset,
            # x="violin",
            y="difference_abs",
            # hue="violin",
            # order=player_order,
            # alpha=0.2,
            palette=colors[::2],
            # order=["control", "test"],
            # order=["Klimke", "Levaggi", "Stoppani"],
            # hue_order=["Klimke", "Levaggi", "Stoppani"],
            # legend=False,
            ax=axes[i, 1],
            # dodge=0.3,
            linestyle="none",
        )

        ax.get_legend().remove()
        ax.set_ylabel(f"{CRITERION_MAP[criterion]}\nRating difference")

    xtick_labels = [str(i) for i in range(1, len(control_players) + 1)] + ["Test"]
    axes[-1, 0].set_xticks(range(len(player_order)))
    axes[-1, 0].set_xticklabels(xtick_labels)

    for ax in axes.flat:
        ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(1))

    # --- 3.4 Legends ---
    target_ax_top = axes[0, 0]
    handles_top, labels_top = target_ax_top.get_legend_handles_labels()
    axes[1, 1].legend(
        handles_top[:3],
        labels_top[:3],
        title="Violin",
        loc="center left",
        bbox_to_anchor=(1.3, 0.5),
        borderaxespad=0,
    )

    plt.tight_layout()

    # --- 4. Saving Figure ---
    output_png = pathlib.Path("reports/figures/ratings-variability.png")
    output_svg = pathlib.Path("reports/figures/ratings-variability.svg")
    output_png.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_png)
    plt.savefig(output_svg)
    print(f"Figures saved to {output_png} and {output_svg}")


def main():
    parser = argparse.ArgumentParser(description="Process and plot violin recordings.")
    parser.add_argument("--process", action="store_true", help="Process raw .mat files")
    parser.add_argument("--plot", action="store_true", help="Generate plots")

    args = parser.parse_args()

    # If no args provided, run both
    if not args.process and not args.plot:
        args.process = True
        args.plot = True

    # if args.process:
    # ds = build_dataset()
    # save_dataset(ds, PROCESSED_DATA_PATH)

    if args.plot:
        plot(PROCESSED_DATA_PATH)


if __name__ == "__main__":
    main()
