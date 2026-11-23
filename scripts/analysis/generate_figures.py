
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Resolve repository paths
ROOT_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = ROOT_DIR / "experiments" / "multi_gateway" / "data"
OUTPUT_DIR = ROOT_DIR / "experiments" / "multi_gateway" / "graphs"

CSV_FILE = DATA_DIR / "benchmark_summary.csv"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

data = pd.read_csv(CSV_FILE)

configs = [
    "Direct_EdgeX",
    "Single_Kong_JWT",
    "HAProxy_Two_Kong_JWT"
]

labels = {
    "Direct_EdgeX": "Direct EdgeX",
    "Single_Kong_JWT": "Single Kong + JWT",
    "HAProxy_Two_Kong_JWT": "Two Kong + HAProxy + JWT"
}

data["Target_RPS"] = pd.to_numeric(data["Target_RPS"])
data = data.sort_values("Target_RPS")

plt.rcParams.update({
    "figure.figsize": (9, 5.5),
    "font.size": 10,
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "legend.fontsize": 9,
    "figure.dpi": 120
})

def make_plot(column, ylabel, title, filename, target_line=False):
    fig, ax = plt.subplots()

    for config in configs:
        subset = data[data["Configuration"] == config]

        ax.plot(
            subset["Target_RPS"],
            subset[column],
            marker="o",
            linewidth=2,
            markersize=5,
            label=labels[config]
        )

    if target_line:
        targets = sorted(data["Target_RPS"].unique())

        ax.plot(
            targets,
            targets,
            linestyle="--",
            color="gray",
            alpha=0.7,
            label="Target RPS"
        )

    ax.set_title(title)
    ax.set_xlabel("Target Request Rate (requests/second)")
    ax.set_ylabel(ylabel)
    ax.set_xticks(sorted(data["Target_RPS"].unique()))
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend()
    fig.tight_layout()

    fig.savefig(OUTPUT_DIR / filename, dpi=300, bbox_inches="tight")
    fig.savefig(
        OUTPUT_DIR / filename.replace(".png", ".svg"),
        bbox_inches="tight"
    )

    plt.close(fig)

    print(f"Created: {filename} and {filename.replace('.png', '.svg')}")

# Figure 1: Throughput comparison
make_plot(
    "Mean_Actual_RPS",
    "Mean Actual Throughput (requests/second)",
    "Throughput Comparison Across Configurations",
    "figure_1_throughput_comparison.png",
    target_line=True
)

# Figure 2: P95 latency comparison
make_plot(
    "Mean_P95_ms",
    "Mean P95 Latency (milliseconds)",
    "P95 Latency Comparison Across Configurations",
    "figure_2_p95_latency.png"
)

# Figure 3: Dropped iterations comparison
make_plot(
    "Mean_Dropped_Iterations",
    "Mean Dropped Iterations",
    "Dropped Iterations Across Configurations",
    "figure_3_dropped_iterations.png"
)

print("\nAll figures saved in:", OUTPUT_DIR)
