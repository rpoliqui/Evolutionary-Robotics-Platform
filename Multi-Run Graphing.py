import re
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np
from pathlib import Path

# ── Configuration ────────────────────────────────────────────────────────────
BASE_DIR = Path("C:/Users/rpoli/Documents/College/Evolutionary Robotics (CS 3060)/Final Project/Final Report")
OUTPUT_MAX_INDIVIDUAL  = Path("max_fitness_individual.png")
OUTPUT_AVG_INDIVIDUAL  = Path("avg_fitness_individual.png")
OUTPUT_MAX_AGGREGATE   = Path("max_fitness_aggregate.png")
OUTPUT_AVG_AGGREGATE   = Path("avg_fitness_aggregate.png")

COLOR_A = "#E63946"     # Red for all A runs
COLOR_B = "#457B9D"     # Blue for all B runs
ALPHA_INDIVIDUAL = 1.0 # Transparency for individual run lines
ALPHA_AGGREGATE  = 1.0  # Aggregate line is fully opaque
# ─────────────────────────────────────────────────────────────────────────────


def get_generation_count(folder_name: str) -> int:
    match = re.search(r"(\d+)", folder_name)
    return int(match.group(1)) if match else -1


def find_best_generation_folder(run_path: Path):
    gen_folders = [f for f in run_path.iterdir() if f.is_dir()]
    if not gen_folders:
        return None
    return max(gen_folders, key=lambda f: get_generation_count(f.name))


def load_csv(path: Path):
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
    run_dirs = sorted(
        [d for d in base_dir.iterdir()
         if d.is_dir() and re.match(r"run\s*\d+", d.name, re.IGNORECASE)],
        key=lambda d: int(re.search(r"\d+", d.name).group())
    )
    if not run_dirs:
        raise FileNotFoundError(f"No 'Run N' folders found in: {base_dir.resolve()}")

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
    cols_lower = [c.lower() for c in df.columns]
    if kind == "gen":
        candidates = [c for c in cols_lower if "gen" in c]
    elif kind == "max":
        candidates = [c for c in cols_lower if "max" in c and "fitness" in c]
    else:
        candidates = [c for c in cols_lower
                      if any(kw in c for kw in ("average", "avg", "mean"))
                      and "fitness" in c]
    if not candidates:
        raise KeyError(f"Cannot find '{kind}' column in: {list(df.columns)}")
    return df.columns[cols_lower.index(candidates[0])]


def build_aggregate(runs: list, metric: str):
    """
    Interpolate every run onto a common integer generation index,
    then return (mean, std) across all runs at each generation.
    Returns (None, None) if runs is empty.
    """
    if not runs:
        return None, None

    series_list = []
    for df in runs:
        gen_col = infer_column(df, "gen")
        fit_col = infer_column(df, metric)
        x = pd.to_numeric(df[gen_col], errors="coerce")
        y = pd.to_numeric(df[fit_col], errors="coerce")
        mask = x.notna() & y.notna()
        s = pd.Series(y[mask].values, index=x[mask].values.astype(int))
        s = s[~s.index.duplicated(keep="last")].sort_index()
        series_list.append(s)

    all_gens = sorted(set().union(*[set(s.index) for s in series_list]))
    aligned = pd.DataFrame(index=all_gens)
    for i, s in enumerate(series_list):
        aligned[i] = s
    aligned = aligned.interpolate(method="index", limit_direction="both")

    return aligned.mean(axis=1), aligned.std(axis=1)


def apply_axis_formatting(ax):
    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True, nbins=10))
    ax.yaxis.set_major_locator(plt.MaxNLocator(nbins=8))
    ax.tick_params(axis="both", labelsize=10)
    ax.yaxis.set_major_formatter(plt.FormatStrFormatter("%.4f"))
    ax.grid(True, linestyle="--", alpha=0.35)
    ax.set_facecolor("#f9f9f9")


def plot_individual(runs_a, runs_b, metric: str, output_path: Path):
    """One line per run, A and B coloured separately."""
    title_word = "Max" if metric == "max" else "Average"
    fig, ax = plt.subplots(figsize=(10, 6))

    for runs, color in [(runs_a, COLOR_A), (runs_b, COLOR_B)]:
        for df in runs:
            gen_col = infer_column(df, "gen")
            fit_col = infer_column(df, metric)
            x = pd.to_numeric(df[gen_col], errors="coerce")
            y = pd.to_numeric(df[fit_col], errors="coerce")
            mask = x.notna() & y.notna()
            ax.plot(x[mask], y[mask], color=color, alpha=ALPHA_INDIVIDUAL, linewidth=1.5)

    legend_handles = [
        mlines.Line2D([], [], color=COLOR_A, linewidth=2.5, label="Group A"),
        mlines.Line2D([], [], color=COLOR_B, linewidth=2.5, label="Group B"),
    ]
    ax.legend(handles=legend_handles, fontsize=12, framealpha=0.9)
    ax.set_title(f"{title_word} Fitness — Individual Runs", fontsize=14)
    ax.set_xlabel("Generation", fontsize=12)
    ax.set_ylabel(f"{title_word} Fitness", fontsize=12)
    apply_axis_formatting(ax)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"  Saved: {output_path.resolve()}")
    plt.close(fig)


def plot_aggregate(runs_a, runs_b, metric: str, output_path: Path):
    """One mean line per group with shaded +/- 1 std error band."""
    title_word = "Max" if metric == "max" else "Average"
    fig, ax = plt.subplots(figsize=(10, 6))

    mean_a, std_a = build_aggregate(runs_a, metric)
    mean_b, std_b = build_aggregate(runs_b, metric)

    if mean_a is not None:
        ax.plot(mean_a.index, mean_a.values, color=COLOR_A, linewidth=2.5, label="Group A (mean)")
        ax.fill_between(mean_a.index, mean_a - std_a, mean_a + std_a,
                        color=COLOR_A, alpha=0.2, label="Group A (±1 std)")
    if mean_b is not None:
        ax.plot(mean_b.index, mean_b.values, color=COLOR_B, linewidth=2.5, label="Group B (mean)")
        ax.fill_between(mean_b.index, mean_b - std_b, mean_b + std_b,
                        color=COLOR_B, alpha=0.2, label="Group B (±1 std)")

    ax.legend(fontsize=12, framealpha=0.9)
    ax.set_title(f"{title_word} Fitness — Aggregated Mean ± Std", fontsize=14)
    ax.set_xlabel("Generation", fontsize=12)
    ax.set_ylabel(f"{title_word} Fitness", fontsize=12)
    apply_axis_formatting(ax)
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

    print("Plotting max fitness (individual) ...")
    plot_individual(runs_a, runs_b, "max", OUTPUT_MAX_INDIVIDUAL)

    print("Plotting average fitness (individual) ...")
    plot_individual(runs_a, runs_b, "avg", OUTPUT_AVG_INDIVIDUAL)

    print("Plotting max fitness (aggregate) ...")
    plot_aggregate(runs_a, runs_b, "max", OUTPUT_MAX_AGGREGATE)

    print("Plotting average fitness (aggregate) ...")
    plot_aggregate(runs_a, runs_b, "avg", OUTPUT_AVG_AGGREGATE)

    print("\nDone!")


if __name__ == "__main__":
    main()