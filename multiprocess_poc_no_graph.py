import multiprocessing as mp
import os
import platform

import time
from dataclasses import dataclass

def run(v):
    return sum(i * i for i in range(v.value))
    

def determine_workers():
    workers_env = os.getenv("WORKERS", None)
    if workers_env is None:
        return mp.cpu_count()
    
    if workers_env.isdigit():
        workers = int(workers_env)
    else:
        raise ValueError(f"Invalid value for env variable WORKERS: {workers_env}")
    
    if workers > mp.cpu_count():
        raise ValueError(f"Requested workers higher than available CPUs: {workers} vs {mp.cpu_count()}")

    if platform.system() == "Windows" and workers > 61:
        raise ValueError(f"Windows only supports up to 61 workers, requested: {workers}")

    return workers
    

def main(values):
    workers = determine_workers()

    with mp.Pool(processes=workers) as pool:  
        results = pool.map(run, values)
            
    print(f"{values=}")

@dataclass
class Number:
    id: int
    value: int


if __name__ == "__main__":
    values = [Number(id=v, value=(5_000_000 + v)) for v in range(1, 50)]
    start = time.time()
    main(values)
    end = time.time()
    print(end - start)