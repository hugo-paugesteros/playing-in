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
    ).dropna()

    control_players = sorted(df_diff[df_diff["scope"] == "control"]["player"].unique())
    test_players = df_diff[df_diff["scope"] == "test"]["player"].unique()
    player_order = list(control_players) + list(test_players)

    # --- 3. Plotting ---
    fig, axes = plt.subplots(
        nrows=len(CRITERION),
        sharex=True,
        sharey=True,
    )

    # A. Main Grid (Violin vs Violinist)
    for i, criterion in enumerate(CRITERION):
        ax = axes[i]

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

        # Filter data for this specific cell
        subset = df_diff[
            (df_diff["criterion"] == criterion) & (df_diff["difference_type"] == "3-1")
        ]

        # Stripplot
        sns.pointplot(
            data=subset,
            x="player",
            y="difference",
            hue="violin",
            order=player_order,
            # alpha=0.2,
            palette=colors[1::2],
            # order=["control", "test"],
            hue_order=["Klimke", "Levaggi", "Stoppani"],
            # legend=False,
            ax=ax,
            dodge=0.3,
            linestyle="none",
        )
        ax.get_legend().remove()
        ax.set_ylabel(f"{CRITERION_MAP[criterion]}\nRating difference")

    xtick_labels = [str(i) for i in range(1, len(control_players) + 1)] + ["Test"]
    axes[-1].set_xticks(range(len(player_order)))
    axes[-1].set_xticklabels(xtick_labels)

    # # --- 3.2 Row 4 : Differences ---
    # for col, criteria in enumerate(CRITERION):
    #     ax = axes[-1, col]
    #     subset = df_diff[(df_diff["criterion"] == criteria)]
    #     sns.pointplot(
    #         data=subset,
    #         x="scope",
    #         y="difference",
    #         hue="violin",
    #         palette=[colors["klimke"], colors["levaggi"], colors["stoppani"]],
    #         ax=ax,
    #         linestyle="none",
    #         errorbar=ci,
    #         dodge=0.4,
    #     )
    #     ax.get_legend().remove()
    #     if col == 0:
    #         ax.set_ylabel("Rating difference")
    #     else:
    #         ax.set_ylabel("")

    #     ax.set_xlabel("")

    # for ax in axes.flat:
    #     ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(1))

    # --- 3.4 Legends ---
    target_ax_top = axes[-1]
    handles_top, labels_top = target_ax_top.get_legend_handles_labels()
    fig.legend(
        handles_top[:6],
        [
            "Klimke / 2-1",
            "Levaggi / 2-1",
            "Stoppani / 2-1",
            "Klimke / 3-1",
            "Levaggi / 3-1",
            "Stoppani / 3-1",
        ],
        title="Violin / Session",
        loc="center left",
        bbox_to_anchor=(1.02, 0.5),
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
