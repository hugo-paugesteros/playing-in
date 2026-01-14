import argparse
import pathlib
import warnings
from typing import Optional, Tuple

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import scipy.io
import xarray as xr
import pandas as pd
import seaborn as sns

import identification.dataset

from config import mm, colors, ci

# Constants
RAW_DATA_DIR = pathlib.Path("data/raw/")
PROCESSED_DATA_PATH = pathlib.Path("data/processed/recordings.nc")
SR = 51200
N_FFT = 32768

PHASES = [1, 2]
VIOLINS = ["klimke", "levaggi", "stoppani"]
SCOPES = ["control", "test"]


def build_dataset() -> xr.Dataset:
    """
    Iterate over raw files and build an xarray Dataset.
    """
    config = {
        "frame_size": 2048,
        "hop_ratio": 4,
        "n_coeff": 40,
        "sr": 16000,
        "sample_duration": 60,
        "feature": "LTAS_welch_db",
    }

    data = pd.read_pickle(
        "/home/hugo/Thèse/identification/data/processed/dataset_cnsm.pkl"
    )
    data = data[(data.violin.isin(["A", "B", "C"]))]
    data = data[data.session.isin([1, 3])]
    data = data[data.extract == "gamme"]
    data.violin = data.violin.map({"A": "klimke", "B": "levaggi", "C": "stoppani"})

    df = identification.dataset.get_dataset(config, data)

    feature_matrix = np.stack(df["features"].values)
    n_features = feature_matrix.shape[1]
    f = np.linspace(0, config["sr"] // 2, n_features)

    df["phase"] = df.apply(lambda row: 2 if row["session"] == 3 else 1, axis=1)
    df["scope"] = df.apply(
        lambda row: "test" if row["player"] == "SMD" else "control", axis=1
    )
    # df["player"] = df["player"].apply(hash)

    ds = xr.Dataset(
        data_vars={
            "features": (["measurement", "frequency"], feature_matrix),
        },
        coords={
            "measurement": df.index,
            "frequency": f,
            "violin": (["measurement"], df["violin"]),
            "violinist": (["measurement"], df["player"]),
            "scope": (["measurement"], df["scope"]),
            "phase": (["measurement"], df["phase"]),
            "condition": (["measurement"], df["condition"]),
            # "extract": (["measurement"], df["extract"]),
            # "start_time": (["measurement"], df["start"]),
            # "end_time": (["measurement"], df["end"]),
            # "filepath": (["measurement"], df["file"]),
        },
    )
    return ds


def save_dataset(dataset: xr.Dataset, output_path: pathlib.Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    dataset.to_netcdf(output_path)
    print(f"Dataset saved to {output_path}")


def plot(dataset_path: pathlib.Path):
    if not dataset_path.exists():
        print(f"File not found: {dataset_path}")
        return

    # --- 1. Load and Process Data (Xarray) ---
    ds = xr.open_dataset(dataset_path)

    # Select frequency range
    features = ds["features"].sel(frequency=slice(200, 5000))

    # Normalize in linear scale (keep high performance math in xarray)
    features_lin = 10 ** (features / 20)

    # Set MultiIndex to separate violin/phase/violinist
    features_lin = features_lin.set_index(
        measurement=["violin", "phase", "violinist", "scope"]
    )

    # Normalize each measurement by its own mean
    norm_lin = features_lin.groupby("measurement").map(lambda x: x / x.mean())

    norm_lin = norm_lin.reset_index("measurement")

    # --- 2. Prepare DataFrames for Seaborn ---
    # Convert back to dB for plotting: 20*log10(x)
    # Note: Using Mean(dB) here instead of 20log(Mean(Lin)) for simplicity.
    # If strictly specific math is needed, pre-calculate in xarray as before.
    df_main = (20 * np.log10(norm_lin)).to_dataframe("amplitude")

    df_means = df_main.groupby(["violin", "violinist", "phase", "frequency", "scope"])[
        "amplitude"
    ].mean()

    # B. Unstack 'phase' to move it from rows to columns
    #    Result has columns: phase 1, phase 2
    df_pivoted = df_means.unstack("phase")

    # C. Calculate Difference (Phase 2 - Phase 1)
    diff_series = df_pivoted[2] - df_pivoted[1]

    # D. Reset index to make it plot-ready
    df_diff = diff_series.reset_index(name="difference")

    # --- 3. Plotting ---
    violins = df_main["violin"].unique()
    scopes = df_main["scope"].unique()

    # Use subplots to keep the custom layout (Grid + Diff row)
    fig, axs = plt.subplots(
        len(violins) + 1,
        len(scopes),
        sharex=True,
        sharey="row",
        figsize=(190 * mm, 190 / (4 / 3) * mm),
    )

    # A. Main Grid (Violin vs Violinist)
    for row, violin in enumerate(VIOLINS):
        for col, scope in enumerate(SCOPES):
            ax = axs[row, col]

            # Filter data for this cell
            subset = df_main[
                (df_main["violin"] == violin) & (df_main["scope"] == scope)
            ]

            # Seaborn Magic: Handles Mean AND Min/Max shading in one line
            sns.lineplot(
                data=subset,
                x="frequency",
                y="amplitude",
                hue="phase",
                errorbar=ci,
                estimator="mean",
                palette=[colors[1], colors[2]],
                ax=ax,
            )

            if col == 0:
                suffix = "(Test)" if violin == "klimke" else "(Control)"
                row_title = f"{violin.capitalize()} {suffix}"
                ax.set_ylabel(f"{row_title}\nAmplitude (dB)")
            if row == 0:
                ax.set_title("Control group" if col == 0 else "Test violinist")
            ax.grid(True, alpha=0.3)

    # B. Bottom Row: Difference Plot
    for col, scope in enumerate(SCOPES):
        ax = axs[-1, col]
        subset_diff = df_diff[df_diff["scope"] == scope]

        sns.lineplot(
            data=subset_diff,
            x="frequency",
            y="difference",
            hue="violin",
            errorbar=ci,
            estimator="mean",
            ax=ax,
        )
        # ax.get_legend().remove()
        ax.set_ylabel("Difference (dB)" if col == 0 else "")
        ax.set_xlabel("Frequency")
        ax.grid(True, alpha=0.3)

    # C. Global Styling
    for ax in axs.flat:
        if ax.get_legend():
            ax.get_legend().remove()
        ax.set_xscale("log")
        ax.set_xlim(200, 5000)
        ax.xaxis.set_major_formatter(mpl.ticker.ScalarFormatter())
        ax.set_xticks([200, 500, 1000, 5000])

    # Legends
    target_ax_top = axs[1, -1]
    handles_top, labels_top = target_ax_top.get_legend_handles_labels()
    target_ax_top.legend(
        handles_top[:2],
        labels_top[:2],
        title="Phase",
        loc="center left",
        bbox_to_anchor=(
            1.02,
            0.5,
        ),
        borderaxespad=0,
    )

    target_ax_bottom = axs[3, -1]
    handles_top, labels_top = target_ax_bottom.get_legend_handles_labels()
    target_ax_bottom.legend(
        handles_top[:3],
        map(str.capitalize, labels_top[:3]),
        title="Violin",
        loc="center left",
        bbox_to_anchor=(
            1.02,
            0.5,
        ),
        borderaxespad=0,
    )

    # s = fig.subplotpars
    # bb = [s.left, s.top + 0.04, s.right - s.left, 0.05]
    # target_ax_top = axs[0, 0]
    # handles_top, labels_top = target_ax_top.get_legend_handles_labels()
    # target_ax_top.legend(
    #     handles_top[:2],
    #     ["Phase 1", "Phase 2"],
    #     # title="Phase",
    #     loc="lower left",
    #     bbox_to_anchor=(0, 1.02, 2.185, 0.2),
    #     borderaxespad=0,
    #     ncol=2,
    #     mode="expand",
    #     # bbox_transform=fig.transFigure,
    #     fancybox=False,
    # )

    # target_ax_top = axs[3, 0]
    # handles_top, labels_top = target_ax_top.get_legend_handles_labels()
    # target_ax_top.legend(
    #     handles_top[:3],
    #     map(str.capitalize, labels_top[:3]),
    #     # title="Phase",
    #     loc="lower left",
    #     bbox_to_anchor=(0, 1.02, 2.185, 0.0),
    #     borderaxespad=0,
    #     ncol=3,
    #     mode="expand",
    #     # bbox_transform=fig.transFigure,
    #     fancybox=False,
    # )

    # Save
    plt.tight_layout()
    output_path = pathlib.Path("reports/figures/recordings.png")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path)
    print(f"Saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Process and plot violin recordings.")
    parser.add_argument("--process", action="store_true", help="Process raw .mat files")
    parser.add_argument("--plot", action="store_true", help="Generate plots")

    args = parser.parse_args()

    # If no args provided, run both
    if not args.process and not args.plot:
        args.process = True
        args.plot = True

    if args.process:
        ds = build_dataset()
        save_dataset(ds, PROCESSED_DATA_PATH)

    if args.plot:
        plot(PROCESSED_DATA_PATH)


if __name__ == "__main__":
    main()
