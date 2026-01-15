import argparse
import pathlib
import warnings
from typing import Optional, Tuple

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

from config import mm, colors, ci, VIOLIN_MAP, SCOPES_MAP
import json

PROCESSED_DATA_PATH = pathlib.Path("data/processed/listening_test.csv")

VIOLINS = ["Klimke", "Levaggi", "Stoppani"]
PLAYERS = ["Norimi", "SMD"]


def plot(dataset_path: pathlib.Path):
    # --- 1. Load Data (Pandas) ---
    df_diff = pd.read_csv(dataset_path)
    # TODO : fix "scope" column in the dataset creation
    df_diff["scope"] = "Control"

    # --- 2. Compute difference ---
    df = df_diff.melt(
        id_vars=[
            "scope",
            "listener",
            "violin",
            "player",
        ],  # Columns to keep as identifiers
        value_vars=["11", "12"],  # Columns to stack/melt
        var_name="phase",  # Name for the new category column
        value_name="score",  # Name for the new value column
    )

    # --- 3. Plotting ---
    fig, axes = plt.subplots(
        nrows=len(VIOLINS) + 1,
        ncols=len(PLAYERS),
        sharex="col",
        sharey="row",
    )

    # A. Main Grid (Violin vs Violinist)
    for i, violin in enumerate(VIOLINS):
        for j, player in enumerate(PLAYERS):
            ax = axes[i, j]

            # Filter data for this specific cell
            subset = df[(df["violin"] == violin) & (df["player"] == player)]
            print(subset)

            # Pointplot
            sns.pointplot(
                data=subset,
                x="scope",
                y="score",
                hue="phase",
                errorbar=ci,
                estimator="mean",
                dodge=0.2,
                linestyle="none",
                palette=[colors[1], colors[2]],
                # order=["Control group", "Test violinist"],
                # hue_order=[1, 2],
                ax=ax,
                # legend=False,
            )

            if j == 0:
                ax.set_ylabel(f"{VIOLIN_MAP[violin.lower()]}\n$\\Delta$")
                ax.sharey(axes[0, 0])
            if i == 0:
                ax.set_title(
                    "Player: Control violinist" if j == 0 else "Player: Test violinist"
                )
            ax.grid(True, alpha=0.3)

    # --- 3.2 Row 4 : Differences ---
    for j, player in enumerate(PLAYERS):
        ax = axes[-1, j]
        subset = df_diff[(df_diff["player"] == player)]
        sns.pointplot(
            data=subset,
            x="scope",
            y="diff",
            hue="violin",
            palette=[colors["klimke"], colors["levaggi"], colors["stoppani"]],
            hue_order=["Klimke", "Levaggi", "Stoppani"],
            ax=ax,
            linestyle="none",
            errorbar=ci,
            dodge=0.4,
        )
        ax.set_xlabel("")
        ax.set_xticklabels(["Listener:\n Control group", "Listener:\n Test violinist"])
    axes[-1, 0].set_ylabel("$\\Delta_{31} - \\Delta_{21}$")

    for ax in axes.flat:
        ax.get_legend().remove()

    # --- 3.4 Legends ---
    target_ax = axes[1, -1]
    handles_top, labels_top = target_ax.get_legend_handles_labels()
    target_ax.legend(
        handles_top[:2],
        ["$\\Delta_{11}$", "$\\Delta_{21}$"],
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

    # --- 4. Saving Figure ---
    output_png = pathlib.Path("reports/figures/recordings.png")
    output_svg = pathlib.Path("reports/figures/recordings.svg")
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
