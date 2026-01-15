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


def plot(dataset_path: pathlib.Path):
    # --- 1. Load Data (Pandas) ---
    df = pd.read_csv(dataset_path)

    # --- 2. Compute difference ---
    pivoted = df.pivot_table(
        index=["scope", "violin", "player", "criterion"],
        columns="phase",
        values="rating",
        aggfunc="mean",  # Handles duplicate ratings if any
    )
    df_diff = (pivoted[2] - pivoted[1]).reset_index(name="difference")

    # --- 3. Plotting ---
    fig, axes = plt.subplots(
        nrows=len(VIOLINS) + 1,
        ncols=len(CRITERION),
        sharex="col",
        sharey="row",
    )

    # A. Main Grid (Violin vs Violinist)
    for i, violin in enumerate(VIOLINS):
        for j, criterion in enumerate(CRITERION):
            ax = axes[i, j]

            # Filter data for this specific cell
            subset = df[
                (df["violin"] == violin.capitalize()) & (df["criterion"] == criterion)
            ]

            # Stripplot
            sns.stripplot(
                data=subset,
                x="scope",
                y="rating",
                hue="phase",
                dodge=True,
                alpha=0.2,
                palette=[colors[1], colors[2]],
                order=["control", "test"],
                hue_order=[1, 2],
                legend=False,
                ax=ax,
            )

            # Pointplot
            sns.pointplot(
                data=subset,
                x="scope",
                y="rating",
                hue="phase",
                errorbar=ci,
                estimator="mean",
                dodge=0.2,
                linestyle="none",
                palette=[colors[1], colors[2]],
                order=["control", "test"],
                hue_order=[1, 2],
                ax=ax,
                # legend=False,
            )

            ax.set_xticklabels(["Control Group", "Test Violinist"])

            ax.set_xlabel("")
            ax.get_legend().remove()

            if j == 0:
                ax.sharey(axes[0, 0])
                ax.set_ylabel(f"{VIOLIN_MAP[violin]}\nRating (0-10)")
            else:
                ax.set_ylabel("")

            # Titles only on the top row
            if i == 0:
                ax.set_title(CRITERION_MAP[criterion])

    # --- 3.2 Row 4 : Differences ---
    for col, criteria in enumerate(CRITERION):
        ax = axes[-1, col]
        subset = df_diff[(df_diff["criterion"] == criteria)]
        sns.pointplot(
            data=subset,
            x="scope",
            y="difference",
            hue="violin",
            palette=[colors["klimke"], colors["levaggi"], colors["stoppani"]],
            ax=ax,
            linestyle="none",
            errorbar=ci,
            dodge=0.4,
        )
        ax.get_legend().remove()
        if col == 0:
            ax.set_ylabel("Rating difference")
        else:
            ax.set_ylabel("")

        ax.set_xlabel("")

    # --- 3.4 Legends ---
    target_ax_top = axes[1, -1]
    handles_top, labels_top = target_ax_top.get_legend_handles_labels()
    target_ax_top.legend(
        handles_top[:2],
        labels_top[:2],
        title="Phase",
        loc="center left",
        bbox_to_anchor=(1.02, 0.5),
        borderaxespad=0,
    )

    target_ax_bottom = axes[3, -1]
    handles_top, labels_top = target_ax_bottom.get_legend_handles_labels()
    target_ax_bottom.legend(
        handles_top[:3],
        ["Klimke", "Levaggi", "Stoppani"],
        title="Violin",
        loc="center left",
        bbox_to_anchor=(1.02, 0.5),
        borderaxespad=0,
    )

    plt.tight_layout()

    # --- 4. Saving Figure ---
    output_png = pathlib.Path("reports/figures/ratings.png")
    output_svg = pathlib.Path("reports/figures/ratings.svg")
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
