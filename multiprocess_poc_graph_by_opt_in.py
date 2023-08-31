import multiprocessing as mp
import os
import platform

import time
from dataclasses import dataclass


def run(v):
    sum(i * i for i in range(v.value))
    return v.id


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


def determine_what_to_run(values, has_run):
    will_run = []
    for val in values:
        if val.id in has_run:
            continue
        if val.depends_on is not None and val.depends_on not in has_run:
            continue
        will_run.append(val)
    return will_run


def main(values):
    total_items = len(values)
    has_run = []

    with mp.Pool(processes=determine_workers()) as pool:
        while len(has_run) < total_items:
            
            will_run = determine_what_to_run(values, has_run)
            print(f"Running for {len(will_run)}")
            results = pool.map(run, will_run)
            has_run.extend(results)                
                
    print(f"Done for: {len(has_run)} / {total_items}")
    print(f"{has_run=}")

@dataclass
class Number:
    id: int
    value: int

    @property
    def depends_on(self):
        if bool(self.id % 2) and self.id < 10:
            return self.id + 4 
        else:
            return None

if __name__ == "__main__":
    # This approach loops over the graph items (will be pipelines), 
    # all the ones that CAN run are added to the map.
    # Once they are all done, the graph is reexamined to make a new list of what can run
    # This list is then passed back into the map until all items are complete
    # Testing on a contrived graph this was mildly faster than the retry option,
    # it also has the added bonus of simpler orchestration and the process not 
    # needing to know about the logic of what can/cant run
    values = [Number(id=v, value=(5_000_000 + v)) for v in range(1, 50)]
    start = time.time()
    main(values)
    end = time.time()
    print(end - start)