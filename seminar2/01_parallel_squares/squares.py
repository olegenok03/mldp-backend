"""3 варианта посчитать квадраты. См. README.md."""

import multiprocessing as mp
import threading
import time
from queue import Queue

N_WORKERS = mp.cpu_count()


def very_slow_function(x: int) -> int:
    """Возвращает x**2 с задержкой 0.1s — НЕ менять."""
    time.sleep(0.1)
    return x**2


def calc_squares_simple(bound: int) -> list[int]:
    return [very_slow_function(i) for i in range(bound)]


def calc_squares_multithreading(bound: int) -> list[int]:
    q: Queue[tuple[int, int]] = Queue()

    def thread_worker(part_id: int, bound: int, n_workers: int) -> None:
        for k in range(part_id, bound, n_workers):
            q.put((k, very_slow_function(k)))

    threads = [
        threading.Thread(target=thread_worker, args=(i, bound, N_WORKERS))
        for i in range(N_WORKERS)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    res = [0] * bound
    while not q.empty():
        idx, value = q.get()
        res[idx] = value
    return res


def process_worker(part_id: int, bound: int, n_workers: int) -> list[tuple[int, int]]:
    chunk = []
    for k in range(part_id, bound, n_workers):
        chunk.append((k, very_slow_function(k)))
    return chunk


def calc_squares_multiprocessing(bound: int) -> list[int]:
    tasks = [(i, bound, N_WORKERS) for i in range(N_WORKERS)]
    with mp.Pool(processes=N_WORKERS) as pool:
        chunks = pool.starmap(process_worker, tasks)
    res = [0] * bound
    for chunk in chunks:
        for idx, val in chunk:
            res[idx] = val
    return res
