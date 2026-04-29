import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from pathlib import Path

# ── Configuration ────────────────────────────────────────────────────────────
# Set BASE_DIR to the folder containing your "Run 1", "Run 2", … subfolders.
# Using pathlib.Path avoids any forward-slash / backslash mismatch on Windows.
BASE_DIR = Path("C:/Users/rpoli/Documents/College/Evolutionary Robotics (CS 3060)/Final Project/Final Report")
OUTPUT_MAX = Path("max_fitness.png")
OUTPUT_AVG = Path("average_fitness.png")

COLOR_A = "#E63946"     # Red for all A runs
COLOR_B = "#457B9D"     # Blue for all B runs
ALPHA   = 0.80          # Line transparency
# ─────────────────────────────────────────────────────────────────────────────


def get_generation_count(folder_name: str) -> int:
    """Extract the numeric generation count from a name like '150 Generations'."""
    match = re.search(r"(\d+)", folder_name)
    return int(match.group(1)) if match else -1


def find_best_generation_folder(run_path: Path):
    """Return the sub-folder with the highest generation count."""
    gen_folders = [f for f in run_path.iterdir() if f.is_dir()]
    if not gen_folders:
        return None
    return max(gen_folders, key=lambda f: get_generation_count(f.name))


def load_csv(path: Path):
    """Load a CSV, trying tab-separated first then comma-separated."""
    for sep in ("\t", ",", ";"):
        try:
            df = pd.read_csv(path, sep=sep, engine="python")
            if df.shape[1] > 1:
                return df
        except Exception:
            continue
    print(f"  ⚠  Could not read: {path}")
    return None


def collect_data(base_dir: Path):
    """Walk base_dir and collect DataFrames for every run."""
    run_dirs = sorted(
        [d for d in base_dir.iterdir()
         if d.is_dir() and re.match(r"run\s*\d+", d.name, re.IGNORECASE)],
        key=lambda d: int(re.search(r"\d+", d.name).group())
    )

    if not run_dirs:
        raise FileNotFoundError(
            f"No 'Run N' folders found in: {base_dir.resolve()}"
        )

    runs_a, runs_b = [], []

    for run_dir in run_dirs:
        gen_folder = find_best_generation_folder(run_dir)
        if gen_folder is None:
            print(f"  ⚠  No generation sub-folders in {run_dir.name}, skipping.")
            continue

        print(f"  {run_dir.name} -> {gen_folder.name}")

        for suffix, storage in [("A", runs_a), ("B", runs_b)]:
            csv_path = gen_folder / f"fitness_data_{suffix}.csv"
            if not csv_path.exists():
                print(f"    ⚠  Missing: {csv_path.name}")
                continue
            df = load_csv(csv_path)
            if df is not None:
                df["run"] = run_dir.name
                storage.append(df)

    return runs_a, runs_b


def infer_column(df: pd.DataFrame, kind: str) -> str:
    """Flexibly find Generation / Max / Average fitness column."""
    cols_lower = [c.lower() for c in df.columns]
    if kind == "gen":
        candidates = [c for c in cols_lower if "gen" in c]
    elif kind == "max":
        candidates = [c for c in cols_lower if "max" in c and "fitness" in c]
    else:  # avg
        candidates = [c for c in cols_lower
                      if any(kw in c for kw in ("average", "avg", "mean"))
                      and "fitness" in c]
    if not candidates:
        raise KeyError(f"Cannot find '{kind}' column in: {list(df.columns)}")
    return df.columns[cols_lower.index(candidates[0])]


def plot_metric(runs_a, runs_b, metric: str, output_path: Path):
    """Plot one metric ('max' or 'avg') for all A and B runs."""
    fig, ax = plt.subplots(figsize=(11, 6))

    for runs, color in [(runs_a, COLOR_A), (runs_b, COLOR_B)]:
        for df in runs:
            gen_col = infer_column(df, "gen")
            fit_col = infer_column(df, metric)

            # Ensure both columns are numeric — drop any non-numeric rows
            x = pd.to_numeric(df[gen_col], errors="coerce")
            y = pd.to_numeric(df[fit_col], errors="coerce")
            mask = x.notna() & y.notna()

            ax.plot(x[mask], y[mask], color=color, alpha=ALPHA, linewidth=1.6)

    # Legend — one entry per group
    legend_handles = [
        mlines.Line2D([], [], color=COLOR_A, linewidth=2.5, label="Version A"),
        mlines.Line2D([], [], color=COLOR_B, linewidth=2.5, label="Version B"),
    ]
    ax.legend(handles=legend_handles, fontsize=12, framealpha=0.9)

    title_word = "Max" if metric == "max" else "Average"
    ax.set_title(f"{title_word} Fitness Across All Runs", fontsize=15, pad=12)
    ax.set_xlabel("Generation", fontsize=12)
    ax.set_ylabel(f"{title_word} Fitness", fontsize=12)

    # Limit tick density so labels never collide
    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True, nbins=10))
    ax.yaxis.set_major_locator(plt.MaxNLocator(nbins=8))
    ax.tick_params(axis="both", labelsize=10)
    ax.yaxis.set_major_formatter(plt.FormatStrFormatter("%.4f"))

    ax.grid(True, linestyle="--", alpha=0.35)
    ax.set_facecolor("#f9f9f9")
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"  Saved: {output_path.resolve()}")
    plt.close(fig)


def main():
    print(f"\nScanning: {BASE_DIR.resolve()}\n")
    runs_a, runs_b = collect_data(BASE_DIR)

    if not runs_a and not runs_b:
        print("No data loaded — check that BASE_DIR points to the correct folder.")
        return

    print(f"\nLoaded {len(runs_a)} Group A run(s) and {len(runs_b)} Group B run(s).\n")

    print("Plotting max fitness ...")
    plot_metric(runs_a, runs_b, "max", OUTPUT_MAX)

    print("Plotting average fitness ...")
    plot_metric(runs_a, runs_b, "avg", OUTPUT_AVG)

    print("\nDone!")


if __name__ == "__main__":
    main()