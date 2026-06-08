"""Build solution notebooks from the current exercise notebooks."""

import hashlib
from pathlib import Path
import subprocess

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell


ROOT = Path(__file__).parent
SOURCE = ROOT / "Nawrot_CNS_Course"


def load(name):
    if not SOURCE.is_dir():
        subprocess.run(
            ["git", "clone", "https://github.com/schmitfe/Nawrot_CNS_Course.git", str(SOURCE)],
            check=True,
        )
    return nbformat.read(SOURCE / name, as_version=4)


def save(nb, name):
    for index, cell in enumerate(nb.cells):
        identity = f"{index}\0{cell.cell_type}\0{cell.source}".encode()
        cell["id"] = hashlib.sha1(identity).hexdigest()[:12]
        if cell.cell_type == "code":
            cell.execution_count = None
            cell.outputs = []
    nbformat.write(nb, ROOT / name)


def solution_cell(code):
    return new_code_cell(code.strip() + "\n")


def note(text="# Solution"):
    return new_markdown_cell(text)


def insert_after(nb, cell_index, cells):
    nb.cells[cell_index + 1 : cell_index + 1] = cells


SETUP_REPLACEMENT = """
from pathlib import Path
import os
import subprocess
import sys

REPO_URL = "https://github.com/schmitfe/Nawrot_CNS_Course.git"
REPO_NAME = "Nawrot_CNS_Course"


def prepare_repo() -> Path:
    cwd = Path.cwd().resolve()
    if (cwd / "data").is_dir():
        return cwd

    clone_parent = Path("/content") if "google.colab" in sys.modules else cwd
    repo_root = clone_parent / REPO_NAME
    if not repo_root.exists():
        subprocess.run(["git", "clone", REPO_URL, str(repo_root)], check=True)
    os.chdir(repo_root)
    return repo_root.resolve()


REPO_ROOT = prepare_repo()
"""


def replace_setup(cell, extra):
    cell.source = SETUP_REPLACEMENT + extra.strip() + "\n"


def build_day1():
    nb = load("PythonProgramming_Day1.ipynb")
    nb.cells[1].source += " - Solutions"

    replacements = {
        28: """
mystring = "LovePython"
myfloat = 6.0
myint = 4

# testing code
if mystring == "LovePython":
    print("String: %s" % mystring)
if isinstance(myfloat, float) and myfloat == 6.0:
    print("Float: %f" % myfloat)
if isinstance(myint, int) and myint == 4:
    print("Integer: %d" % myint)
""",
    }
    for index, code in replacements.items():
        nb.cells[index].source = code.strip() + "\n"

    replace_setup(
        nb.cells[145],
        """
DATA_DIR = REPO_ROOT / "data" / "python_programming"
print(f"REPO_ROOT = {REPO_ROOT}")
print(f"DATA_DIR = {DATA_DIR}")
""",
    )

    additions = {
        48: "numbers = [1, 4, 6, 2, 7, 3, 9]\nprint(sum(numbers))",
        49: "print('smallest:', min(numbers))\nprint('largest:', max(numbers))",
        50: "a = list(range(10))\nprint(a)",
        83: "print(Movie.get('name'))",
        84: "Movie['year'] = 'April 1990'\nprint(Movie)",
        85: "Movie['genre'] = 'mystery/drama/horror'\nprint(Movie)",
        86: "print(Movie.pop('genre'))\nprint(Movie)",
        114: """
sample_list = [2, 3, 4, 5, 8, 2, 9]
even = 0
odd = 0
for number in sample_list:
    if number % 2 == 0:
        even += 1
    else:
        odd += 1
print('even:', even, 'odd:', odd)
""",
        115: """
fib = [0, 1]
while fib[-1] + fib[-2] <= 50:
    fib.append(fib[-1] + fib[-2])
print(fib)
""",
        130: """
def max_of_three(a, b, c):
    return max(a, b, c)

print(max_of_three(3, 8, 5))
""",
        131: """
def multiply(numbers):
    result = 1
    for number in numbers:
        result *= number
    return result

print(multiply([8, 2, 3, -1, 7]))
""",
        132: """
def unique_values(values):
    result = []
    for value in values:
        if value not in result:
            result.append(value)
    return result

print(unique_values([1, 1, 3, 3, 3, 3, 4, 4, 4, 5, 7, 7, 7]))
""",
        133: """
def is_prime(number):
    if number < 2:
        return False
    for divisor in range(2, int(number ** 0.5) + 1):
        if number % divisor == 0:
            return False
    return True

print(is_prime(29))
""",
        147: """
weather_path = DATA_DIR / "CologneWeather.csv"
with open(weather_path, encoding="utf-8") as file:
    weather_text = file.read()
print(weather_text)
""",
        148: """
data_lines = [line for line in weather_text.splitlines() if line.startswith("2019")]
temp = [float(line.split(";")[-1]) for line in data_lines]
print(temp)
""",
        149: "print('average temperature:', sum(temp) / len(temp))",
    }
    for index in sorted(additions, reverse=True):
        insert_after(nb, index, [note(), solution_cell(additions[index])])
    save(nb, "PythonProgramming_Day1_solutions.ipynb")


def build_day2():
    nb = load("PythonProgramming_Day2.ipynb")
    nb.cells[2].source = "# NumPy - Solutions"
    numpy_solutions = {
        16: "true_array = np.ones((3, 3), dtype=bool)\nprint(true_array)",
        17: "arr = np.arange(8)\nprint(arr[arr % 2 == 1])",
        18: "arr = np.arange(8)\nprint(arr.reshape(2, -1))",
        19: """
a = np.arange(10).reshape(2, -1)
b = np.repeat(1, 10).reshape(2, -1)
print(np.vstack((a, b)))
""",
        20: "a = np.arange(0, 15, 2)\nprint(a[(a >= 5) & (a <= 10)])",
        21: """
rng = np.random.default_rng(42)
a = rng.random(1000)
print('mean:', np.mean(a))
print('median:', np.median(a))
print('standard deviation:', np.std(a))
""",
    }
    for index in sorted(numpy_solutions, reverse=True):
        insert_after(nb, index, [note(), solution_cell(numpy_solutions[index])])

    final_index = next(
        i for i, cell in enumerate(nb.cells)
        if cell.cell_type == "markdown" and cell.source.startswith("1. Plot two or more")
    )
    plot_solution = """
rng = np.random.default_rng(42)
x = np.arange(200)
values = rng.uniform(0, 1000, size=x.size)
moving_average = np.convolve(values, np.ones(15) / 15, mode="valid")

fig, axes = plt.subplots(2, 2, figsize=(11, 8))

axes[0, 0].plot(x[values < 500], values[values < 500], "b.", label="< 500")
axes[0, 0].plot(x[values >= 500], values[values >= 500], "r.", label=">= 500")
axes[0, 0].legend()
axes[0, 0].set_title("Threshold colors")

axes[0, 1].plot(x, values, color="0.7")
axes[0, 1].plot(x[values > 800], values[values > 800], "k*", label="> 800")
axes[0, 1].legend()
axes[0, 1].set_title("Large values")

axes[1, 0].hist(values, bins=20)
axes[1, 0].set_title("Histogram")

axes[1, 1].plot(np.arange(len(moving_average)) + 7, moving_average)
axes[1, 1].set_title("15-sample moving average")

for ax in axes.flat:
    ax.set_xlabel("sample")
    ax.set_ylabel("value")
plt.tight_layout()
plt.show()
"""
    insert_after(nb, final_index, [note("## Solution"), solution_cell(plot_solution)])
    save(nb, "PythonProgramming_Day2_solutions.ipynb")


def build_day3():
    nb = load("Python_Programming_Day3.ipynb")
    nb.cells[1].source = "# Exercises - Solutions"
    replace_setup(
        nb.cells[3],
        """
DATA_DIR = REPO_ROOT / "data" / "python_programming"
print(f"REPO_ROOT = {REPO_ROOT}")
print(f"DATA_DIR = {DATA_DIR}")
""",
    )
    nb.cells[4].source = """
import matplotlib.pyplot as plt
import numpy as np

max_temp = np.array([5, 7, 11, 15, 19, 22, 24, 24, 20, 15, 10, 6])
min_temp = np.array([-1, -1, 2, 4, 8, 11, 13, 13, 10, 7, 3, 0])
months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]
mean_temp = (max_temp + min_temp) / 2

plt.figure(figsize=(10, 4))
plt.plot(months, mean_temp, "o-")
plt.ylabel("mean temperature (degrees C)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
""".strip() + "\n"
    nb.cells[7].source = """
from scipy.io import loadmat
from scipy.stats import mannwhitneyu, pearsonr, spearmanr

car_data = loadmat(DATA_DIR / "CarData.mat", squeeze_me=True)
print(car_data["Description"])
M = car_data["M"]
print("M dimensions:", M.ndim)

cylinders = M[:, 0]
fuel_economy = M[:, 3]
weight = M[:, 4]
print("cylinder values:", np.unique(cylinders[~np.isnan(cylinders)]))

idx_4 = np.where(cylinders <= 4)[0]
idx_6 = np.where(cylinders >= 6)[0]
print("<= 4 cylinders: mean weight =", np.nanmean(weight[idx_4]),
      "mean fuel economy (mpg) =", np.nanmean(fuel_economy[idx_4]))
print(">= 6 cylinders: mean weight =", np.nanmean(weight[idx_6]))
print("overlap:", np.intersect1d(idx_4, idx_6))

valid_groups = ~np.isnan(weight)
test = mannwhitneyu(
    weight[idx_4][valid_groups[idx_4]],
    weight[idx_6][valid_groups[idx_6]],
    alternative="two-sided",
)
print("weight difference:", test)

valid = ~np.isnan(weight) & ~np.isnan(fuel_economy)
print("Pearson:", pearsonr(weight[valid], fuel_economy[valid]))
print("Spearman:", spearmanr(weight[valid], fuel_economy[valid]))
""".strip() + "\n"
    save(nb, "Python_Programming_Day3_solutions.ipynb")


def build_day4():
    nb = load("PythonProgramming_Day4.ipynb")
    nb.cells[1].source += " - Solutions"
    fern_code = """
points = np.zeros((n_points, 2))
state = np.zeros(2)

for i in range(n_points):
    k = rng.choice(len(p), p=p)
    state = A[k] @ state + b[k]
    points[i] = state

plt.scatter(points[:, 0], points[:, 1], s=0.05, color="darkgreen")
plt.axis("off")
plt.show()
"""
    insert_after(nb, 9, [note("### Solution"), solution_cell(fern_code)])

    pattern_index = next(i for i, c in enumerate(nb.cells) if c.cell_type == "code" and "# Define your own patterns here." in c.source)
    nb.cells[pattern_index].source = """
pattern_1 = -np.ones((8, 8), dtype=int)
pattern_1[1:7, 1] = 1
pattern_1[1:7, 6] = 1
pattern_1[3:5, 1:7] = 1

pattern_2 = -np.ones((8, 8), dtype=int)
pattern_2[1:7, 1:3] = 1
pattern_2[1:3, 1:7] = 1
pattern_2[3:5, 1:6] = 1
pattern_2[5:7, 1:7] = 1

pattern_3 = -np.ones((8, 8), dtype=int)
pattern_3[1:7, 3:5] = 1
pattern_3[3:5, 1:7] = 1

patterns_2d = [pattern_1, pattern_2, pattern_3]

fig, axes = plt.subplots(1, 3, figsize=(9, 3))
for ax, pattern, title in zip(axes, patterns_2d, ["H", "S", "cross"]):
    show_pattern(pattern, ax=ax, title=title)
plt.tight_layout()
plt.show()
""".strip() + "\n"

    funcs_index = next(i for i, c in enumerate(nb.cells) if c.cell_type == "code" and "def train_hopfield" in c.source)
    nb.cells[funcs_index].source = """
def train_hopfield(patterns):
    n_units = patterns[0].size
    W = np.zeros((n_units, n_units), dtype=float)
    for pattern in patterns:
        p = pattern.reshape(-1)
        W += np.outer(p, p)
    W /= n_units
    np.fill_diagonal(W, 0)
    return W


def update_async(state, W, rng, n_steps):
    state = state.copy()
    for _ in range(n_steps):
        unit = rng.integers(state.size)
        support = W[unit] @ state
        if support != 0:
            state[unit] = np.sign(support)
    return state
""".strip() + "\n"

    workflow_index = next(i for i, c in enumerate(nb.cells) if c.cell_type == "code" and "# W = train_hopfield" in c.source)
    nb.cells[workflow_index].source = """
W = train_hopfield(patterns_2d)
original = patterns_2d[0]
noisy = corrupt_pattern(original, n_flips=10, rng=rng)
recovered = update_async(noisy.reshape(-1), W, rng=rng, n_steps=1000)
recovered = recovered.reshape(original.shape)

fig, axes = plt.subplots(1, 3, figsize=(9, 3))
show_pattern(original, ax=axes[0], title="original")
show_pattern(noisy, ax=axes[1], title="noisy")
show_pattern(recovered, ax=axes[2], title="recovered")
plt.tight_layout()
plt.show()
""".strip() + "\n"
    save(nb, "PythonProgramming_Day4_solutions.ipynb")


def build_neural_data():
    nb = load("Neural_Data_Analysis.ipynb")
    nb.cells[1].source += " - Solutions"
    replace_setup(
        nb.cells[5],
        """
DATA_DIR = REPO_ROOT / "data" / "neural_data_analysis"
A1_PATH = DATA_DIR / "A1_data_set_040528_boucsein_nostruct.mat"
SPONTANEOUS_PATH = DATA_DIR / "spontaneous_recording_nostruct.mat"
RELIABILITY_PATH = DATA_DIR / "synaptic_response_variability_nostruct.mat"
print(f"REPO_ROOT = {REPO_ROOT}")
print(f"DATA_DIR = {DATA_DIR}")
""",
    )
    imports = """
from scipy.io import loadmat
import matplotlib.pyplot as plt
import numpy as np


def event_cutouts(signal, event_idx, before, after):
    valid = event_idx[(event_idx >= before) & (event_idx + after < len(signal))]
    return np.array([signal[i - before:i + after] for i in valid])
"""
    insert_after(nb, 5, [solution_cell(imports)])

    part1 = """
a1 = loadmat(A1_PATH, squeeze_me=True)
V = a1["V"].ravel()
dt = float(a1["SampleIntervalSeconds"])
t = np.arange(V.size) * dt
print(f"complete duration: {t[-1]:.2f} s")

plt.figure()
plt.plot(t[t < 2], V[t < 2])
plt.ylim(-75, 20)
plt.xlabel("time (s)")
plt.ylabel("membrane potential (mV)")
plt.title("Figure 1: intracellular voltage")
plt.show()

threshold = -40
spike_idx = np.where((V[1:] >= threshold) & (V[:-1] < threshold))[0] + 1
spike_times = spike_idx * dt
print("spikes:", len(spike_idx), "mean firing rate (Hz):", len(spike_idx) / t[-1])

before = after = round(0.010 / dt)
spikes = event_cutouts(V, spike_idx, before, after)
spike_t = (np.arange(spikes.shape[1]) - before) * dt * 1000
spike_mean = spikes.mean(axis=0)
spike_std = spikes.std(axis=0)
plt.figure()
plt.plot(spike_t, spike_mean, color="red")
plt.fill_between(spike_t, spike_mean - spike_std, spike_mean + spike_std, alpha=0.3)
plt.xlabel("time from threshold crossing (ms)")
plt.ylabel("membrane potential (mV)")
plt.title("Figure 2: average action potential")
plt.show()

non_spike_mask = np.ones(V.size, dtype=bool)
for i in spike_idx:
    non_spike_mask[max(0, i - before):min(V.size, i + after)] = False
non_spike_V = V[non_spike_mask]
print("non-spiking mean:", non_spike_V.mean(), "variance:", non_spike_V.var())
plt.figure()
plt.hist(non_spike_V, bins=np.arange(-75, -20, 0.5))
plt.xlabel("membrane potential (mV)")
plt.ylabel("samples")
plt.title("Figure 3: membrane-potential distribution")
plt.show()

long_before = round(0.5 / dt)
long_spikes = event_cutouts(V, spike_idx, long_before, after)
long_t = (np.arange(long_spikes.shape[1]) - long_before) * dt * 1000
plt.figure()
plt.plot(long_t, long_spikes.mean(axis=0), color="red")
plt.fill_between(
    long_t,
    long_spikes.mean(axis=0) - long_spikes.std(axis=0),
    long_spikes.mean(axis=0) + long_spikes.std(axis=0),
    alpha=0.3,
)
plt.xlabel("time from threshold crossing (ms)")
plt.ylabel("membrane potential (mV)")
plt.title("Figure 4: variability before spike onset")
plt.show()
"""
    insert_after(nb, 13, [note("### Solution: Part I"), solution_cell(part1)])

    part2 = """
spontaneous = loadmat(SPONTANEOUS_PATH, squeeze_me=True)
I = spontaneous["I"].ravel()
FI = spontaneous["FI"].ravel()
dt_I = float(spontaneous["TimeResolutionS"])
t_I = np.arange(I.size) * dt_I

threshold_psc = -8
onset_idx = np.where((FI[1:] < threshold_psc) & (FI[:-1] >= threshold_psc))[0] + 1
print("detected PSCs:", len(onset_idx))

window = t_I < 1
plt.figure()
plt.plot(t_I[window], I[window], label="raw")
plt.plot(t_I[window], FI[window], label="filtered")
plt.axhline(threshold_psc, color="red", label="threshold")
plt.xlabel("time (s)")
plt.ylabel("current (pA)")
plt.legend()
plt.show()

psc_before = round(0.020 / dt_I)
psc_after = round(0.080 / dt_I)
PSCs = event_cutouts(I, onset_idx, psc_before, psc_after)
psc_t = (np.arange(PSCs.shape[1]) - psc_before) * dt_I * 1000
mean_psc = PSCs.mean(axis=0)
std_psc = PSCs.std(axis=0)
peak_amplitudes = -PSCs.min(axis=1)
print("average PSC peak amplitude (pA):", -mean_psc.min())

fig, axes = plt.subplots(1, 3, figsize=(14, 4))
axes[0].plot(psc_t, PSCs.T, alpha=0.15)
axes[0].plot(psc_t, mean_psc, color="black", linewidth=2)
axes[1].plot(psc_t, mean_psc, color="black")
axes[1].fill_between(psc_t, mean_psc - std_psc, mean_psc + std_psc, alpha=0.3)
axes[2].hist(peak_amplitudes[peak_amplitudes > 0], bins=25)
axes[2].set_xscale("log")
for ax in axes[:2]:
    ax.set_xlabel("time from onset (ms)")
    ax.set_ylabel("current (pA)")
axes[2].set_xlabel("PSC peak amplitude (pA, log scale)")
axes[2].set_ylabel("count")
plt.tight_layout()
plt.show()
"""
    insert_after(nb, 21 + 2, [note("### Solution: Part II"), solution_cell(part2)])

    # Find the final task by text because earlier insertions shifted indices.
    final_task = next(i for i, c in enumerate(nb.cells) if c.cell_type == "markdown" and c.source.startswith("3.4 Temporal precision"))
    part3 = """
reliability = loadmat(RELIABILITY_PATH, squeeze_me=True)
current = reliability["I"].ravel()
shutter = reliability["Z"].ravel()
dt_current = float(reliability["I_TimeResolutionS"])
dt_shutter = float(reliability["Z_TimeResolutionS"])

opening_idx = np.where((shutter[1:] < 0) & (shutter[:-1] >= 0))[0] + 1
opening_times = opening_idx * dt_shutter
opening_times = opening_times.reshape(14, 3).T
print("shutter openings:", opening_times.size)

n_response = round(0.100 / dt_current)
responses = np.empty((3, 14, n_response))
for site in range(3):
    for trial in range(14):
        start = round(opening_times[site, trial] / dt_current)
        responses[site, trial] = current[start:start + n_response]

response_t = np.arange(n_response) * dt_current * 1000
peak = responses.max(axis=2)
peak_mean = peak.mean(axis=1)
peak_std = peak.std(axis=1)
cv = peak_std / peak_mean

fig, axes = plt.subplots(1, 3, figsize=(14, 4), sharex=True, sharey=True)
for site, ax in enumerate(axes):
    ax.plot(response_t, responses[site].T, alpha=0.7)
    ax.set_title(f"site {site + 1}: mean={peak_mean[site]:.1f}, CV={cv[site]:.2f}")
    ax.set_xlabel("time after stimulation (ms)")
axes[0].set_ylabel("current (pA)")
plt.tight_layout()
plt.show()

onset_threshold = 40
onset_times = np.full((3, 14), np.nan)
for site in range(3):
    for trial in range(14):
        trace = responses[site, trial]
        crossings = np.where((trace[1:] >= onset_threshold) & (trace[:-1] < onset_threshold))[0] + 1
        if crossings.size:
            onset_times[site, trial] = crossings[0] * dt_current * 1000
print("onset-time standard deviations (ms):", np.nanstd(onset_times, axis=1))
"""
    insert_after(nb, final_task, [note("### Solution: Part III"), solution_cell(part3)])
    save(nb, "Neural_Data_Analysis_solutions.ipynb")


def build_trial_variability():
    nb = load("Trial_by_trial_variability.ipynb")
    nb.cells[2].source += " - Solutions"
    replace_setup(
        nb.cells[7],
        """
import matplotlib.pyplot as plt
import numpy as np
import scipy.io as spio
import scipy.signal

DATA_DIR = REPO_ROOT / "data" / "motor_cortex"
SPARSE_DATA_DIR = DATA_DIR / "data_sparse_FromLinux"
SELECTED_C1_DIR = DATA_DIR / "SelectedDataC1"
SELECTED_C3_DIR = DATA_DIR / "SelectedDataC3"
""",
    )
    part1 = """
def load_sparse_format(path):
    return spio.loadmat(path, squeeze_me=True, struct_as_record=False)["SparseFormat"]


def centered_counts(spike_data, window_bins):
    kernel = np.ones((window_bins, 1))
    return scipy.signal.convolve(spike_data, kernel, mode="same")


def fano_factor(counts):
    mean = counts.mean(axis=1)
    variance = counts.var(axis=1)
    return np.divide(variance, mean, out=np.full_like(mean, np.nan), where=mean > 0)


example = load_sparse_format(SELECTED_C1_TS_FILES[0])
spike_data = example.Data[0].toarray()
dt_ms = float(example.TimeResolutionMS)
time_ms = np.arange(spike_data.shape[0]) * dt_ms + example.CutIntervalMS[0]
window_bins = round(400 / dt_ms)
example_ff = fano_factor(centered_counts(spike_data, window_bins))
print("binary spike-train resolution (ms):", dt_ms)

unit_ff = []
for path in SELECTED_C1_TS_FILES:
    sparse = load_sparse_format(path)
    direction_ff = []
    for direction_data in sparse.Data:
        spike_data = direction_data.toarray()[:time_ms.size]
        counts = centered_counts(spike_data, window_bins)
        direction_ff.append(fano_factor(counts))
    unit_ff.append(np.nanmean(direction_ff, axis=0))
grand_ff = np.nanmean(unit_ff, axis=0)

fig, axes = plt.subplots(2, 1, figsize=(9, 7), sharex=True)
axes[0].plot(time_ms, example_ff)
axes[0].set_title("one unit, one direction")
axes[1].plot(time_ms, grand_ff)
axes[1].set_title("mean across C1 units and directions")
for ax in axes:
    ax.set_ylabel("Fano factor")
axes[1].set_xlabel("time relative to TS (ms)")
plt.tight_layout()
plt.show()
"""
    nb.cells[17].source = part1.strip() + "\n"

    part2 = """
def cv2_for_trials(spike_data):
    values = []
    for trial in range(spike_data.shape[1]):
        spike_times = np.flatnonzero(spike_data[:, trial])
        isi = np.diff(spike_times)
        if isi.size >= 2:
            values.extend(2 * np.abs(np.diff(isi)) / (isi[:-1] + isi[1:]))
    return np.mean(values) if values else np.nan


ff_values = []
cv2_squared_values = []
window_start_ms, window_end_ms = 0, 750

for path in SELECTED_C1_TS_FILES:
    sparse = load_sparse_format(path)
    start = round((window_start_ms - sparse.CutIntervalMS[0]) / sparse.TimeResolutionMS)
    end = round((window_end_ms - sparse.CutIntervalMS[0]) / sparse.TimeResolutionMS)
    for direction_data in sparse.Data:
        window_data = direction_data.toarray()[start:end]
        counts = window_data.sum(axis=0)
        ff_values.append(counts.var() / counts.mean() if counts.mean() > 0 else np.nan)
        cv2_squared_values.append(cv2_for_trials(window_data) ** 2)

ff_values = np.asarray(ff_values)
cv2_squared_values = np.asarray(cv2_squared_values)
valid = np.isfinite(ff_values) & np.isfinite(cv2_squared_values)
limit = 1.05 * max(ff_values[valid].max(), cv2_squared_values[valid].max())

fig, axes = plt.subplots(1, 3, figsize=(14, 4))
axes[0].scatter(cv2_squared_values[valid], ff_values[valid])
axes[0].plot([0, limit], [0, limit], "r--", label="renewal expectation")
axes[0].set(xlim=(0, limit), ylim=(0, limit), aspect="equal",
            xlabel="$CV2^2$", ylabel="Fano factor")
axes[0].legend()
axes[1].hist(ff_values[valid], bins=12)
axes[1].set_xlabel("Fano factor")
axes[2].hist(cv2_squared_values[valid], bins=12)
axes[2].set_xlabel("$CV2^2$")
plt.tight_layout()
plt.show()

print("mean FF:", np.nanmean(ff_values))
print("mean CV2 squared:", np.nanmean(cv2_squared_values))
"""
    nb.cells[24].source = part2.strip() + "\n"
    save(nb, "Trial_by_trial_variability_solutions.ipynb")


def main():
    build_day1()
    build_day2()
    build_day3()
    build_day4()
    build_neural_data()
    build_trial_variability()


if __name__ == "__main__":
    main()
