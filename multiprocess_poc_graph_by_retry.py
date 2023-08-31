import multiprocessing as mp
import os
import platform

import time
from dataclasses import dataclass

def run(v):

    if v.depends_on and v.depends_on not in run.has_run:
        run.rerun.put(v)
        return None
    else:
        run.has_run.append(v.id)
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
    

def run_init(rerun: mp.Queue, has_run: mp.Queue):
    run.rerun = rerun
    run.has_run = has_run

def main(values):
    total_items = len(values)
    complete = []
    rerun = mp.Queue()
    workers = determine_workers()

    with mp.Manager() as manager:

        has_run = manager.list()
        with mp.Pool(processes=workers, initializer=run_init, initargs=[rerun, has_run]) as pool:
            while len(complete) < total_items:
                results = pool.map(run, values)
                # Remove Nones from completed
                complete.extend([r for r in results if r])
                if rerun.empty():
                    break
                else:
                    values = []
                    while not rerun.empty():
                        values.append(rerun.get())
                    print(f"Retrying for: {len(values)}, {values=}")


    print(f"Done for: {len(complete)} / {total_items}")
    print(f"{complete=}")

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
    # This approach passes the state of completions around the different processes
    # It might run risk of race conditions because it passes around two variables
    # has_run and re_run, these are a mp.queue and a mp.list and combined keep track of what
    # to run. When an item is considered invalid for running it returns the process at once
    # Returned processes are then rerun once the others have completed. It was slightly slower
    # across tests than an opt in approach, but really may depend on the graph. The fact that
    # This one has mich more complexity seems like more of a deal breaker realistically
    values = [Number(id=v, value=(5_000_000 + v)) for v in range(1, 50)]
    start = time.time()
    main(values)
    end = time.time()
    print(end - start)