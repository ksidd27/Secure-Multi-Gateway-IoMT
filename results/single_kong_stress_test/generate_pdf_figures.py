import json
import re
from pathlib import Path

import matplotlib.pyplot as plt

DATA_DIR = Path(__file__).resolve().parent
files = []

for path in DATA_DIR.glob("capacity_summary_*rps.json"):
    match = re.fullmatch(r"capacity_summary_(\d+)rps\.json", path.name)
    if match:
        files.append((int(match.group(1)), path))

files.sort(key=lambda item: item[0])

rates, actual, avg_latency, p95_latency, dropped = [], [], [], [], []

for target, path in files:
    with path.open(encoding="utf-8") as f:
        data = json.load(f)

    metrics = data["metrics"]
    rates.append(target)
    actual.append(metrics["http_reqs"]["rate"])
    duration = metrics["http_req_duration"]
    avg_latency.append(duration["avg"])
    p95_latency.append(duration["p(95)"])
    dropped.append(metrics.get("dropped_iterations", {}).get("count", 0))

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
ax.plot(rates, actual, marker="o", linewidth=1.8, label="Actual throughput")
ax.plot(rates, rates, linestyle="--", linewidth=1.2, label="Target throughput")
ax.set_xlabel("Target arrival rate (requests/second)")
ax.set_ylabel("Throughput (requests/second)")
ax.set_title("Single-Kong Throughput")
ax.grid(True, linestyle=":", alpha=0.6)
ax.legend()
fig.savefig(DATA_DIR / "figure_1_single_kong_throughput.pdf")
plt.close(fig)

# Figure 2: Response latency
fig, ax = plt.subplots()
ax.plot(rates, avg_latency, marker="o", linewidth=1.8, label="Mean latency")
ax.plot(rates, p95_latency, marker="s", linewidth=1.8, label="95th-percentile latency")
ax.set_xlabel("Target arrival rate (requests/second)")
ax.set_ylabel("Response latency (ms)")
ax.set_title("Single-Kong Response Latency")
ax.grid(True, linestyle=":", alpha=0.6)
ax.legend()
fig.savefig(DATA_DIR / "figure_2_single_kong_latency.pdf")
plt.close(fig)

# Figure 3: Dropped iterations
fig, ax = plt.subplots()
ax.bar([str(r) for r in rates], dropped, width=0.65)
ax.set_xlabel("Target arrival rate (requests/second)")
ax.set_ylabel("Dropped iterations")
ax.set_title("Single-Kong Dropped Iterations")
ax.grid(True, axis="y", linestyle=":", alpha=0.6)
fig.savefig(DATA_DIR / "figure_3_single_kong_dropped_iterations.pdf")
plt.close(fig)

print(f"Processed {len(files)} primary test files.")
print("Generated:")
print("figure_1_single_kong_throughput.pdf")
print("figure_2_single_kong_latency.pdf")
print("figure_3_single_kong_dropped_iterations.pdf")
