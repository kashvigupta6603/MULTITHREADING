import numpy as np
import time
import threading
import matplotlib.pyplot as plt
import os

# SETTINGS (small for fast execution)
SIZE = 300
NUM_MATRICES = 20

# Generate matrices
matrices = [np.random.rand(SIZE, SIZE) for _ in range(NUM_MATRICES)]
constant_matrix = np.random.rand(SIZE, SIZE)

# Worker function
def multiply_range(start, end, results):
    for i in range(start, end):
        results[i] = np.dot(matrices[i], constant_matrix)

def run_threads(num_threads):
    threads = []
    results = [None] * NUM_MATRICES
    chunk = NUM_MATRICES // num_threads

    start_time = time.time()

    for i in range(num_threads):
        start = i * chunk
        end = NUM_MATRICES if i == num_threads - 1 else (i + 1) * chunk
        t = threading.Thread(target=multiply_range, args=(start, end, results))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return (time.time() - start_time) / 60  # in minutes

# Detect cores
cores = os.cpu_count()
max_threads = cores * 2

thread_list = []
time_list = []

print(f"CPU Cores: {cores}")

for t in range(1, max_threads + 1):
    print(f"Running with {t} threads...")
    time_taken = run_threads(t)
    thread_list.append(t)
    time_list.append(time_taken)
    print(f"Time: {time_taken:.4f} min")

# Save results
with open("results.txt", "w") as f:
    for t, tm in zip(thread_list, time_list):
        f.write(f"T={t}, Time={tm:.4f} min\n")

# Plot graph
plt.plot(thread_list, time_list, marker='o')
plt.xlabel("Threads")
plt.ylabel("Time (minutes)")
plt.title("Thread vs Time")
plt.grid()

plt.savefig("graph.png")
plt.show()