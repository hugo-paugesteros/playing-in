import argparse
import pathlib
import warnings
from typing import Optional, Tuple

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import scipy.io
import xarray as xr

from config import mm, colors

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

            file_paths = list(source_dir.glob(f"*.mat"))

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
                            "filename": file_path.name,
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
    if not dataset_path.exists():
        print(f"File not found: {dataset_path}")
        return

    dataset = xr.open_dataset(dataset_path)

    # Calculate dB
    dataset["H_db"] = 20 * np.log10(np.abs(dataset["H"]))

    # Calculate Mean (RMS)
    mean = (dataset["H"] ** 2).groupby(["violin", "phase"]).mean(dim="measurement") ** (
        1 / 2
    )
    mean_db = 20 * np.log10(mean)

    # Difference
    diff_db = mean_db.sel(phase=1) - mean_db.sel(phase=2)

    violins = mean_db.violin.values
    n_violins = len(violins)

    fig, axs = plt.subplots(
        nrows=n_violins + 1,
        ncols=1,
        sharex=True,
        figsize=(140 * mm, 200 * mm),
    )

    if n_violins == 0:
        return

    for i, violin in enumerate(violins):
        ax = axs[i]
        title_suffix = "(Test)" if violin == "Klimke" else "(Control)"
        ax.set_title(f"{violin.capitalize()} {title_suffix}")

        for phase in PHASES:
            # Select mean data
            m = mean_db.sel(violin=violin, phase=phase)

            # Select individual data for range
            subset = dataset.where(
                (dataset.violin == violin) & (dataset.phase == phase),
                drop=True,
            )
            ind_db = subset["H_db"]

            # Plot Mean
            ax.plot(
                m.frequency,
                m,
                label=f"Phase {phase}",
                c=colors[phase],
            )

            # Plot Variability (Min/Max range)
            ax.fill_between(
                m.frequency,
                ind_db.min(dim="measurement"),
                ind_db.max(dim="measurement"),
                alpha=0.2,
                color=colors[phase],
            )

        ax.legend(fontsize="small", loc="upper left", mode="expand", ncol=4)

    # Plot Difference
    for violin in violins:
        axs[-1].plot(
            diff_db.frequency,
            diff_db.sel(violin=violin),
            label=violin,
            c=colors[violin],
        )

    # Styling
    for ax in axs:
        ax.set_xscale("log")
        ax.set_xlim([180, 5000])
        ax.set_ylim([-45, 0])
        ax.grid(True, which="both", alpha=0.3)
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Amplitude (dB)")
        ax.xaxis.set_ticks([200, 500, 1000, 5000])
        ax.get_xaxis().set_major_formatter(mpl.ticker.ScalarFormatter())

    axs[-1].set_title("Differences between phase 1 and phase 2")
    axs[-1].set_ylim([-20, 25])
    axs[-1].legend(fontsize="small", loc="upper left", mode="expand", ncol=3)

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
