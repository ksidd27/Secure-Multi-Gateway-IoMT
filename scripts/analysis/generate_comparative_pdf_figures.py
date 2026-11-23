
import csv
from pathlib import Path
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np

# Resolve repository paths
ROOT_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = ROOT_DIR / "experiments" / "multi_gateway" / "data"
OUTPUT_DIR = ROOT_DIR / "experiments" / "multi_gateway" / "graphs"

CSV_FILE = DATA_DIR / "benchmark_summary.csv"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

data = defaultdict(list)

# Read benchmark summary
with CSV_FILE.open(newline="", encoding="utf-8-sig") as f:
    for row in csv.DictReader(f):
        config = row["Configuration"]
        data[config].append({
            "target": int(row["Target_RPS"]),
            "throughput": float(row["Mean_Actual_RPS"]),
            "p95": float(row["Mean_P95_ms"]),
            "dropped": float(row["Mean_Dropped_Iterations"]),
            "runs": int(row["Runs"])
        })

configs = [
    ("Direct_EdgeX", "Direct EdgeX", "o", "-"),
    ("Single_Kong_JWT", "Single Kong + JWT", "s", "--"),
    ("HAProxy_Two_Kong_JWT", "HAProxy + Two Kong + JWT", "^", "-.")
]

targets = sorted({r["target"] for rows in data.values() for r in rows})

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "font.size": 10,
    "axes.labelsize": 11,
    "axes.titlesize": 12,
    "legend.fontsize": 8.5,
    "figure.figsize": (6.5, 4),
    "savefig.bbox": "tight"
})

note = "Values are means across the reported runs (1 or 2 runs per configuration)."

# Figure 4: Throughput comparison
fig, ax = plt.subplots()

for key, label, marker, linestyle in configs:
    rows = sorted(data[key], key=lambda x: x["target"])
    ax.plot(
        [r["target"] for r in rows],
        [r["throughput"] for r in rows],
        marker=marker,
        linestyle=linestyle,
        linewidth=1.7,
        markersize=5,
        label=label
    )

ax.set_xlabel("Target arrival rate (requests/second)")
ax.set_ylabel("Mean actual throughput (requests/second)")
ax.set_title("Throughput Comparison Across Configurations")
ax.set_xticks(targets)
ax.grid(True, linestyle=":", alpha=0.6)
ax.legend()
fig.subplots_adjust(bottom=0.18)
fig.text(0.5, 0.035, note, ha="center", fontsize=8)
fig.savefig(OUTPUT_DIR / "figure_4_comparative_throughput.pdf")
plt.close(fig)

# Figure 5: P95 latency comparison
fig, ax = plt.subplots()

for key, label, marker, linestyle in configs:
    rows = sorted(data[key], key=lambda x: x["target"])
    ax.plot(
        [r["target"] for r in rows],
        [r["p95"] for r in rows],
        marker=marker,
        linestyle=linestyle,
        linewidth=1.7,
        markersize=5,
        label=label
    )

ax.set_xlabel("Target arrival rate (requests/second)")
ax.set_ylabel("Mean run-level P95 latency (ms)")
ax.set_title("P95 Latency Comparison Across Configurations")
ax.set_xticks(targets)
ax.grid(True, linestyle=":", alpha=0.6)
ax.legend()
fig.subplots_adjust(bottom=0.18)
fig.text(0.5, 0.035, note, ha="center", fontsize=8)
fig.savefig(OUTPUT_DIR / "figure_5_comparative_p95_latency.pdf")
plt.close(fig)

# Figure 6: Dropped iterations comparison
fig, ax = plt.subplots()

x = np.arange(len(targets))
width = 0.24

for i, (key, label, marker, linestyle) in enumerate(configs):
    rows = {r["target"]: r for r in data[key]}
    values = [rows[t]["dropped"] for t in targets]

    ax.bar(
        x + (i - 1) * width,
        values,
        width,
        label=label
    )

ax.set_xlabel("Target arrival rate (requests/second)")
ax.set_ylabel("Mean dropped iterations")
ax.set_title("Dropped Iterations Across Configurations")
ax.set_xticks(x)
ax.set_xticklabels([str(t) for t in targets])
ax.grid(True, axis="y", linestyle=":", alpha=0.6)
ax.legend()
fig.subplots_adjust(bottom=0.18)
fig.text(0.5, 0.035, note, ha="center", fontsize=8)
fig.savefig(OUTPUT_DIR / "figure_6_comparative_dropped_iterations.pdf")
plt.close(fig)

print("Processed all three configurations.")
print("Generated:")
print("figure_4_comparative_throughput.pdf")
print("figure_5_comparative_p95_latency.pdf")
print("figure_6_comparative_dropped_iterations.pdf")
print(f"Output directory: {OUTPUT_DIR}")
