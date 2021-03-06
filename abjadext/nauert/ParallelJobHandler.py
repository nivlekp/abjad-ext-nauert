import multiprocessing
import pickle

from .JobHandler import JobHandler
from .ParallelJobHandlerWorker import ParallelJobHandlerWorker


class ParallelJobHandler(JobHandler):
    """
    Parallel job-handler.

    Processes ``QuantizationJob`` instances in parallel, based on the number of
    CPUs available.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __call__(self, jobs):
        """
        Calls parallel job handler.
        """
        finished_jobs = []
        job_queue = multiprocessing.JoinableQueue()
        result_queue = multiprocessing.Queue()
        workers = [
            ParallelJobHandlerWorker(job_queue, result_queue)
            for i in range(multiprocessing.cpu_count() * 2)
        ]
        for worker in workers:
            worker.start()
        for job in jobs:
            job_queue.put(pickle.dumps(job, protocol=0))
        for i in range(len(jobs)):
            finished_jobs.append(pickle.loads(result_queue.get()))
        for worker in workers:
            job_queue.put(None)
        job_queue.join()
        result_queue.close()
        job_queue.close()
        for worker in workers:
            worker.join()
        return finished_jobs
