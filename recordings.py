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

import identification.dataset

from config import mm, colors, ci, VIOLIN_MAP

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
    # --- 1. Load Data (Xarray) ---
    ds = xr.open_dataset(dataset_path)
    features = ds["features"].sel(frequency=slice(200, 5000))

    features_lin = 10 ** (features / 20)

    # --- 1.2 Normalize each measurement by its own mean ---
    norm_lin = features_lin / features_lin.mean(dim="frequency")
    norm_db = 20 * np.log10(norm_lin)

    # --- 1.3 Compute phase 2 - phase 1
    # Grouping condition
    multi_indexed = norm_db.set_index(
        measurement=["violin", "violinist", "scope", "phase"]
    )
    # Handling duplicates (multiple takes -> mean)
    averaged_takes = multi_indexed.groupby("measurement").mean()
    # Pivoting baby
    unstacked = averaged_takes.unstack("measurement")
    # Compute difference
    diff_db = unstacked.sel(phase=2) - unstacked.sel(phase=1)

    # --- 2. Prepare Dataframes for Seaborn ---
    df = norm_db.to_dataframe("amplitude").reset_index()
    df_diff = diff_db.to_dataframe("difference").reset_index()

    # --- 3. Plotting ---
    fig, axes = plt.subplots(
        nrows=len(VIOLINS) + 1,
        ncols=len(SCOPES),
        sharex=True,
        sharey="row",
    )

    # A. Main Grid (Violin vs Violinist)
    for row, violin in enumerate(VIOLINS):
        for col, scope in enumerate(SCOPES):
            ax = axes[row, col]

            sns.lineplot(
                data=df[(df["violin"] == violin) & (df["scope"] == scope)],
                x="frequency",
                y="amplitude",
                hue="phase",
                errorbar=ci,
                estimator="mean",
                palette=[colors[1], colors[2]],
                ax=ax,
                err_kws={"linewidth": 0},
            )

            if col == 0:
                ax.set_ylabel(f"{VIOLIN_MAP[violin]}\nAmplitude (dB)")
            if row == 0:
                ax.set_title("Control group" if col == 0 else "Test violinist")
            ax.grid(True, alpha=0.3)

    # --- 3.2 Row 4 : Differences ---
    for col, scope in enumerate(SCOPES):
        ax = axes[-1, col]

        sns.lineplot(
            data=df_diff[df_diff["scope"] == scope],
            x="frequency",
            y="difference",
            hue="violin",
            errorbar=ci,
            estimator="mean",
            ax=ax,
            err_kws={"linewidth": 0},
        )
        ax.set_xlabel("Frequency")
        ax.set_ylabel("Difference (dB)" if col == 0 else "")
        ax.grid(True, alpha=0.3)

    # Global Styling
    for ax in axes.flat:
        if ax.get_legend():
            ax.get_legend().remove()
        ax.set_xscale("log")
        ax.set_xlim([200, 5000])
        ax.grid(True, which="both", alpha=0.3)
        ax.xaxis.set_ticks([200, 500, 1000, 5000])
        ax.get_xaxis().set_major_formatter(mpl.ticker.ScalarFormatter())

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

    if args.process:
        ds = build_dataset()
        save_dataset(ds, PROCESSED_DATA_PATH)

    if args.plot:
        plot(PROCESSED_DATA_PATH)


if __name__ == "__main__":
    main()
