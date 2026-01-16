import argparse
import pathlib
import warnings
from typing import Optional, Tuple

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import scipy.io
import xarray as xr
import seaborn as sns
import pandas as pd

from config import colors, ci, linear_mean, VIOLIN_MAP

# Constants
RAW_DATA_DIR = pathlib.Path("data/raw/")
PROCESSED_DATA_PATH = pathlib.Path("data/processed/admittances.nc")
SR = 51200
N_FFT = 32768
CALIBRATION_X = 1 / (20.41 / 1000)  # mv/N
CALIBRATION_Y = 125 / 1000  # mm/S / V

PHASES = [1, 2]
VIOLINS = ["klimke", "levaggi", "stoppani"]


def process_file(filepath: pathlib.Path) -> Optional[Tuple[np.ndarray, np.ndarray]]:
    """
    Load and process a single .mat file.

    Args:
        filepath: Path to the .mat file.

    Returns:
        Tuple of (frequency_vector, magnitude_response) or None if validation fails.
    """
    try:
        mat = scipy.io.loadmat(filepath)
    except Exception as e:
        warnings.warn(f"Error loading {filepath}: {e}")
        return None

    if "freq" not in mat or "npts" not in mat:
        warnings.warn(f"Missing keys in {filepath}")
        return None

    sr = mat["freq"][0, 0]
    n_fft = mat["npts"][0, 0]

    if n_fft != N_FFT or sr != SR:
        warnings.warn(f"Invalid SR or N_FFT in {filepath}: sr={sr}, n_fft={n_fft}")
        return None

    X_raw = mat["yspec"][:, 1]
    Y_raw = mat["yspec"][:, 0]

    X_cal = X_raw * CALIBRATION_X
    Y_cal = Y_raw * CALIBRATION_Y

    f = np.linspace(0, sr // 2, n_fft // 2 + 1).astype(np.float32)

    # Calculate Admittance (Mobility) H = Y/X (Velocity / Force)
    H_linear = np.abs(Y_cal / X_cal).astype(np.float32)

    return f, H_linear


def build_dataset() -> xr.Dataset:
    """
    Iterate over raw files and build an xarray Dataset.
    """
    datasets = []

    for phase in PHASES:
        for violin in VIOLINS:
            source_dir = RAW_DATA_DIR / f"phase_{phase}" / violin / "admittances"

            if not source_dir.exists():
                warnings.warn(f"Directory not found: {source_dir}")
                continue

            file_paths = sorted(list(source_dir.glob(f"*.mat")))

            if not file_paths:
                warnings.warn(f"No files found for {violin} in session {phase}")
                continue

            for i, file_path in enumerate(file_paths):
                result = process_file(file_path)
                if result:
                    f, H = result
                    ds = xr.Dataset(
                        data_vars={
                            "H": (["frequency"], H),
                        },
                        coords={
                            "frequency": f,
                            "violin": violin,
                            "phase": phase,
                            "measurement_id": i + 1,
                        },
                    ).expand_dims("measurement")

                    datasets.append(ds)

    if not datasets:
        raise ValueError("No data found or processed.")

    combined = xr.concat(datasets, dim="measurement")
    return combined


def save_dataset(dataset: xr.Dataset, output_path: pathlib.Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    dataset.to_netcdf(output_path)
    print(f"Dataset saved to {output_path}")


def plot_admittances(dataset_path: pathlib.Path):
    # --- 1. Load data ---
    ds = xr.open_dataset(dataset_path)
    ds = ds.sel(frequency=slice(180, 5000))

    ds["H_db"] = 20 * np.log10(np.abs(ds["H"]))

    # --- 2. Prepare data for plotting ---
    df = ds["H_db"].to_dataframe("amplitude")
    df_diff = pd.merge(
        df[df["phase"] == 2],
        df[df["phase"] == 1],
        on=["violin", "frequency"],
        suffixes=("_p2", "_p1"),
    )
    df_diff["difference"] = df_diff["amplitude_p2"] - df_diff["amplitude_p1"]

    # --- 3. Plotting ---
    fig, axes = plt.subplots(
        nrows=len(VIOLINS) + 1,
        ncols=1,
        sharex=True,
    )

    # --- 3.1 Rows 1, 2, 3 ---
    for i, violin in enumerate(VIOLINS):
        ax = axes[i]

        sns.lineplot(
            data=df[(df["violin"] == violin)],
            x="frequency",
            y="amplitude",
            hue="phase",
            # errorbar=ci,
            errorbar=("pi", 100),
            estimator=linear_mean,
            palette=[colors[1], colors[2]],
            ax=ax,
            err_kws={"linewidth": 0},
        )

        # Tweak axis
        ax.set_ylabel(f"{VIOLIN_MAP[violin]}\nAmplitude (dB)")
        ax.get_legend().remove()
        ax.sharey(axes[0])

    # --- 3.2 Row 4 : Differences ---
    sns.lineplot(
        data=df_diff,
        x="frequency",
        y="difference",
        hue="violin",
        errorbar=ci,
        estimator="mean",
        ax=axes[-1],
        err_kws={"linewidth": 0},
    )
    axes[-1].set_ylim([-20, 25])
    axes[-1].set_xlabel("Frequency (Hz)")
    axes[-1].set_ylabel("Diff (P2 - P1) (dB)")

    # Styling
    for ax in axes:
        ax.set_xscale("log")
        ax.set_xlim([180, 5000])
        ax.grid(True, which="both", alpha=0.3)
        ax.xaxis.set_ticks([200, 500, 1000, 5000])
        ax.get_xaxis().set_major_formatter(mpl.ticker.ScalarFormatter())

    # --- 3.4 Legends ---
    target_ax = axes[1]
    handles_top, labels_top = target_ax.get_legend_handles_labels()
    target_ax.legend(
        handles_top[:2],
        labels_top[:2],
        title="Phase",
        loc="center left",
        bbox_to_anchor=(1.02, 0.5),
        borderaxespad=0,
    )

    target_ax = axes[-1]
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
    output_png = pathlib.Path("reports/figures/admittances.png")
    output_svg = pathlib.Path("reports/figures/admittances.svg")
    output_png.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_png)
    plt.savefig(output_svg)
    print(f"Figures saved to {output_png} and {output_svg}")


def main():
    parser = argparse.ArgumentParser(description="Process and plot violin admittances.")
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
        plot_admittances(PROCESSED_DATA_PATH)


if __name__ == "__main__":
    main()
