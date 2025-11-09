import os
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

try:
    import seaborn as sns
except Exception:
    sns = None


def _get_sample_dataset():
    """Return a DataFrame similar to seaborn's `tips` dataset.

    If seaborn is available, try to load `tips`. Otherwise create a simple synthetic dataset.
    """
    if sns is not None:
        try:
            df = sns.load_dataset("tips")
            return df
        except Exception:
            pass

    # Fallback synthetic dataset (small)
    rng = np.random.default_rng(0)
    n = 200
    total_bill = np.round(rng.normal(20, 8, n).clip(3), 2)
    tip = np.round(total_bill * (rng.normal(0.15, 0.05, n).clip(0.05, 0.4)), 2)
    smoker = rng.choice(["Yes", "No"], size=n, p=[0.3, 0.7])
    day = rng.choice(["Thur", "Fri", "Sat", "Sun"], size=n)
    time = rng.choice(["Lunch", "Dinner"], size=n, p=[0.25, 0.75])
    size = rng.integers(1, 6, size=n)
    df = pd.DataFrame({
        "total_bill": total_bill,
        "tip": tip,
        "smoker": smoker,
        "day": day,
        "time": time,
        "size": size,
    })
    return df


def _ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def generate_visuals(output_dir="outputs"):
    """Generate several visualizations and save them as PNG files.

    Args:
        output_dir (str): Directory where PNGs will be written. Created if missing.

    Returns:
        List[str]: list of written file paths.
    """
    _ensure_dir(output_dir)
    df = _get_sample_dataset()
    files = []

    # Scatter: total_bill vs tip, color by smoker (if available)
    plt.figure(figsize=(7, 5))
    colors = df["smoker"].map({"Yes": "tab:red", "No": "tab:blue"}) if "smoker" in df.columns else "tab:blue"
    plt.scatter(df["total_bill"], df["tip"], c=colors, alpha=0.7, edgecolor="k", linewidth=0.2)
    plt.xlabel("Total bill")
    plt.ylabel("Tip")
    plt.title("Total bill vs Tip")
    scatter_path = os.path.join(output_dir, "scatter_total_vs_tip.png")
    plt.tight_layout()
    plt.savefig(scatter_path, dpi=150)
    plt.close()
    files.append(scatter_path)

    # Histogram of total_bill
    plt.figure(figsize=(6, 4))
    plt.hist(df["total_bill"], bins=20, color="tab:green", edgecolor="k", alpha=0.8)
    plt.title("Distribution of total bill")
    plt.xlabel("Total bill")
    plt.ylabel("Count")
    hist_path = os.path.join(output_dir, "hist_total_bill.png")
    plt.tight_layout()
    plt.savefig(hist_path, dpi=150)
    plt.close()
    files.append(hist_path)

    # Bar: aggregated total bill by day
    if "day" in df.columns:
        agg = df.groupby("day")["total_bill"].sum().reindex(["Thur", "Fri", "Sat", "Sun"]).fillna(0)
        plt.figure(figsize=(6, 4))
        agg.plot(kind="bar", color="tab:orange", edgecolor="k")
        plt.title("Total bill by day (sum)")
        plt.xlabel("Day")
        plt.ylabel("Total bill")
        bar_path = os.path.join(output_dir, "bar_total_by_day.png")
        plt.tight_layout()
        plt.savefig(bar_path, dpi=150)
        plt.close()
        files.append(bar_path)

    # Heatmap of numeric correlations
    numeric = df.select_dtypes(include=[np.number])
    if numeric.shape[1] >= 2:
        corr = numeric.corr()
        plt.figure(figsize=(5, 4))
        plt.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
        plt.colorbar()
        ticks = range(len(corr.columns))
        plt.xticks(ticks, corr.columns, rotation=45, ha="right")
        plt.yticks(ticks, corr.columns)
        plt.title("Feature correlation (numeric)")
        heatmap_path = os.path.join(output_dir, "heatmap_corr.png")
        plt.tight_layout()
        plt.savefig(heatmap_path, dpi=150)
        plt.close()
        files.append(heatmap_path)

    # Pairplot if seaborn exists
    if sns is not None:
        try:
            numeric_cols = numeric.columns.tolist()
            if len(numeric_cols) >= 2:
                g = sns.pairplot(df[numeric_cols].sample(min(100, len(df))), diag_kind="kde")
                pair_path = os.path.join(output_dir, "pairplot.png")
                g.fig.suptitle("Pairplot (sample)", y=1.02)
                g.fig.tight_layout()
                g.fig.savefig(pair_path, dpi=150)
                plt.close(g.fig)
                files.append(pair_path)
        except Exception:
            # non-fatal
            pass

    return files


if __name__ == "__main__":
    out = "outputs"
    written = generate_visuals(out)
    print(f"Wrote {len(written)} files to '{out}'")
