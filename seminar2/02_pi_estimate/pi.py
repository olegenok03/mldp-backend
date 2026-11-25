"""π через Monte Carlo — три подхода к параллелизму. См. README.md."""

import multiprocessing as mp
import random
from concurrent.futures import ThreadPoolExecutor

SEED = 42
N_WORKERS = mp.cpu_count()


def _hits_in_circle(n_points: int, seed: int) -> int:
    """helper: количество точек в единичном круге (top-level функция —
    чтобы pickle работал для Pool)."""
    random.seed(seed)
    in_circle_count = 0
    for _ in range(n_points):
        x, y = random.uniform(-1, 1), random.uniform(-1, 1)
        if x**2 + y**2 < 1.0:
            in_circle_count += 1
    return in_circle_count


def estimate_pi_serial(n_points: int) -> float:
    return 4 * _hits_in_circle(n_points, seed=SEED) / n_points


def estimate_pi_threading(n_points: int, workers: int = 4) -> float:
    points_per_worker = n_points // workers
    remainder = n_points % workers

    points_list = [
        points_per_worker + (1 if i < remainder else 0) for i in range(workers)
    ]
    seeds_list = [SEED + i for i in range(workers)]

    with ThreadPoolExecutor(max_workers=N_WORKERS) as pool:
        total_hits = sum(pool.map(_hits_in_circle, points_list, seeds_list))

    return 4 * total_hits / n_points


def estimate_pi_multiprocessing(n_points: int, workers: int = 4) -> float:
    points_per_worker = n_points // workers
    remainder = n_points % workers
    tasks = [
        (points_per_worker + (1 if i < remainder else 0), SEED + i)
        for i in range(workers)
    ]
    with mp.Pool(processes=N_WORKERS) as pool:
        hits_list = pool.starmap(_hits_in_circle, tasks)

    total_hits = sum(hits_list)
    return 4 * total_hits / n_points
