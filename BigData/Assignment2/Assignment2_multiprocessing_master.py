#!/usr/bin/env python3

""""
author: Armin Dedic
St.number: 342615
Assignment 2: fastQ parser that calculates the average quality
score per base for all reads in a fastQ file.

THis is the master script, which creates a manager and connects to a server.
Clients from the client script will then connect to that server.
The clients will perform the calculations and the master will return the results.
"""

import multiprocessing as mp
from multiprocessing.managers import SyncManager
from multiprocessing.managers import BaseManager
import time
import sys
import os


def make_server_manager(port, authkey):
    """ Create a manager for the server, listening on the given port.
        Return a manager object with get_job_q and get_result_q methods.
    """
    job_q = mp.Queue()
    result_q = mp.Queue()

    class JobQueueManager(SyncManager):
        pass

    # This registers both the queues
    JobQueueManager.register('get_job_q', callable=lambda: job_q)
    JobQueueManager.register('get_result_q', callable=lambda: result_q)

    # Creates the manager to start the server
    manager = JobQueueManager(address=('', port), authkey=authkey)
    manager.start()
    time.sleep(2)
    print('Server started at port', port)
    return manager


def runserver():
    # Start a shared manager server and access its queues
    # Random port and key are provided
    manager = make_server_manager(3419, b'lol')
    shared_job_q = manager.get_job_q()
    shared_result_q = manager.get_result_q()

    # Creates job parts from the fastqfile for each client machine and stores it in the shared_job_q
    fastqfile_size = os.path.getsize(sys.argv[1])
    chunksize = 0
    fastq_fileparts = fastqfile_size / int(sys.argv[3])
    for i in range(0, fastqfile_size, int(fastq_fileparts)):
        shared_job_q.put((chunksize, chunksize + fastq_fileparts))
        chunksize += fastq_fileparts

    # counting after each client has finished its job
    numresults = 0
    resultdict = []
    while numresults < int(sys.argv[3]):
        outdict = shared_result_q.get()
        resultdict.append(outdict)
        numresults += 1

    # Sums all the results from the clients into one list and writes it to an output file
    final_results = [sum(item) / int(sys.argv[3]) for item in zip(*resultdict)]
    print(final_results)
    with open(sys.argv[4], 'w') as output_file:
        for items in final_results:
            output_file.write(str(items))
            output_file.write("\n")

    # Sleep a bit before shutting down the server, to let the clients know that its empty to shutdown.
    time.sleep(2)
    manager.shutdown()


if __name__ == "__main__":
    start = time.time()
    runserver()
    end = time.time()
    print("Processing time: ", end - start, "seconds")










