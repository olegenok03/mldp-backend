"""3 варианта посчитать квадраты. См. README.md."""

import time
from multiprocessing import Pool
from queue import Queue
from threading import Thread

N_WORKERS = 12


def very_slow_function(x: int) -> int:
    """Возвращает x**2 с задержкой 0.1s — НЕ менять."""
    time.sleep(0.1)
    return x**2


def calc_squares_simple(bound: int) -> list[int]:
    return [very_slow_function(i) for i in range(bound)]


def calc_squares_multithreading(bound: int) -> list[int]:
    q: Queue[tuple[int, int]] = Queue()

    def thread_worker(part_id: int, bound: int, n_workers: int):
        for k in range(part_id, bound, n_workers):
            q.put((k, very_slow_function(k)))

    threads = [
        Thread(target=thread_worker, args=(i, bound, N_WORKERS))
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


def calc_squares_multiprocessing(bound: int) -> list[int]:
    Pool().starmap()
