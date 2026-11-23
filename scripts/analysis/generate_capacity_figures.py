
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Resolve repository paths
ROOT_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = ROOT_DIR / "experiments" / "single_gateway" / "data"
OUTPUT_DIR = ROOT_DIR / "experiments" / "single_gateway" / "graphs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Read existing CSV data
capacity = pd.read_csv(DATA_DIR / "capacity_graph_data.csv")
resources = pd.read_csv(DATA_DIR / "resource_utilization_summary.csv")

capacity = capacity.sort_values("Target_RPS")

plt.rcParams.update({
    "figure.figsize": (9, 5.5),
    "font.size": 10,
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "legend.fontsize": 9,
    "figure.dpi": 120
})

def save_plot(fig, filename):
    fig.tight_layout()

    fig.savefig(OUTPUT_DIR / filename, dpi=300, bbox_inches="tight")
    fig.savefig(
        OUTPUT_DIR / filename.replace(".png", ".svg"),
        bbox_inches="tight"
    )

    plt.close(fig)
    print("Created:", filename)

# Figure 1: Throughput
fig, ax = plt.subplots()
ax.plot(
    capacity["Target_RPS"],
    capacity["Actual_RPS"],
    marker="o",
    linewidth=2,
    label="Actual throughput"
)
ax.plot(
    capacity["Target_RPS"],
    capacity["Target_RPS"],
    linestyle="--",
    label="Target throughput"
)
ax.set(
    title="Single-Kong Throughput vs. Target Load",
    xlabel="Target Request Rate (requests/second)",
    ylabel="Actual Throughput (requests/second)"
)
ax.grid(True, linestyle=":", alpha=0.6)
ax.legend()
save_plot(fig, "figure_4_single_kong_throughput.png")

# Figure 2: Latency
fig, ax = plt.subplots()
ax.plot(
    capacity["Target_RPS"],
    capacity["Avg_ms"],
    marker="o",
    label="Average latency"
)
ax.plot(
    capacity["Target_RPS"],
    capacity["P95_ms"],
    marker="s",
    label="P95 latency"
)
ax.set(
    title="Single-Kong Latency vs. Target Load",
    xlabel="Target Request Rate (requests/second)",
    ylabel="Latency (milliseconds)"
)
ax.grid(True, linestyle=":", alpha=0.6)
ax.legend()
save_plot(fig, "figure_5_single_kong_latency.png")

# Figure 3: Dropped iterations
fig, ax = plt.subplots()
ax.plot(
    capacity["Target_RPS"],
    capacity["Dropped"],
    marker="o",
    linewidth=2
)
ax.set(
    title="Single-Kong Dropped Iterations vs. Target Load",
    xlabel="Target Request Rate (requests/second)",
    ylabel="Dropped Iterations"
)
ax.grid(True, linestyle=":", alpha=0.6)
save_plot(fig, "figure_6_single_kong_dropped_iterations.png")

# Figure 4: CPU utilization
fig, ax = plt.subplots()

for container in ["kong", "edgex-core-data", "kong-db"]:
    subset = resources[
        resources["Container"] == container
    ].sort_values("Target_RPS")

    ax.plot(
        subset["Target_RPS"],
        subset["CPU_Avg_pct"],
        marker="o",
        linewidth=2,
        label=container
    )

ax.set(
    title="Average CPU Utilization Across Load Levels",
    xlabel="Target Request Rate (requests/second)",
    ylabel="Average CPU Utilization (%)"
)
ax.grid(True, linestyle=":", alpha=0.6)
ax.legend()
save_plot(fig, "figure_7_single_kong_cpu_utilization.png")
# Figure 5: Memory utilization
fig, ax = plt.subplots()

for container in ["kong", "edgex-core-data", "kong-db"]:
    subset = resources[
        resources["Container"] == container
    ].sort_values("Target_RPS")

    ax.plot(
        subset["Target_RPS"],
        subset["Memory_Avg_MiB"],
        marker="o",
        linewidth=2,
        label=container
    )

ax.set(
    title="Average Memory Utilization Across Load Levels",
    xlabel="Target Request Rate (requests/second)",
    ylabel="Average Memory (MiB)"
)
ax.grid(True, linestyle=":", alpha=0.6)
ax.legend()
save_plot(fig, "figure_8_single_kong_memory_utilization.png")

print("\nAll five figures saved in:")
print(OUTPUT_DIR)
