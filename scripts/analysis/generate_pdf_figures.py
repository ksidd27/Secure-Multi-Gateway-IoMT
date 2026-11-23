
import csv
from pathlib import Path

# Resolve repository paths
ROOT_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = ROOT_DIR / "experiments" / "single_gateway" / "data"
OUTPUT_DIR = ROOT_DIR / "experiments" / "single_gateway" / "graphs"

CSV_FILE = DATA_DIR / "capacity_graph_data.csv"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Read capacity test results
rates = []
actual = []
avg_latency = []
p95_latency = []
dropped = []

with CSV_FILE.open(newline="", encoding="utf-8-sig") as f:
    for row in csv.DictReader(f):
        rates.append(float(row["Target_RPS"]))
        actual.append(float(row["Actual_RPS"]))
        avg_latency.append(float(row["Avg_ms"]))
        p95_latency.append(float(row["P95_ms"]))
        dropped.append(float(row["Dropped"]))

import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "font.size": 10,
    "axes.labelsize": 11,
    "axes.titlesize": 12,
    "legend.fontsize": 9,
    "figure.figsize": (6.5, 4),
    "savefig.bbox": "tight"
})

# Figure 1: Throughput
fig, ax = plt.subplots()
ax.plot(rates, actual, marker="o", linewidth=1.8,
        label="Actual throughput")
ax.plot(rates, rates, linestyle="--", linewidth=1.2,
        label="Target throughput")
ax.set_xlabel("Target arrival rate (requests/second)")
ax.set_ylabel("Throughput (requests/second)")
ax.set_title("Single-Kong Throughput")
ax.grid(True, linestyle=":", alpha=0.6)
ax.legend()
fig.savefig(OUTPUT_DIR / "figure_1_single_kong_throughput.pdf")
plt.close(fig)

# Figure 2: Response latency
fig, ax = plt.subplots()
ax.plot(rates, avg_latency, marker="o", linewidth=1.8,
        label="Mean latency")
ax.plot(rates, p95_latency, marker="s", linewidth=1.8,
        label="95th-percentile latency")
ax.set_xlabel("Target arrival rate (requests/second)")
ax.set_ylabel("Response latency (ms)")
ax.set_title("Single-Kong Response Latency")
ax.grid(True, linestyle=":", alpha=0.6)
ax.legend()
fig.savefig(OUTPUT_DIR / "figure_2_single_kong_latency.pdf")
plt.close(fig)

# Figure 3: Dropped iterations
fig, ax = plt.subplots()
ax.bar([str(int(r)) for r in rates], dropped, width=0.65)
ax.set_xlabel("Target arrival rate (requests/second)")
ax.set_ylabel("Dropped iterations")
ax.set_title("Single-Kong Dropped Iterations")
ax.grid(True, axis="y", linestyle=":", alpha=0.6)
fig.savefig(OUTPUT_DIR / "figure_3_single_kong_dropped_iterations.pdf")
plt.close(fig)

print(f"Processed {len(rates)} capacity test records.")
print(f"Figures saved in: {OUTPUT_DIR}")
