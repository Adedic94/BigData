#!/usr/bin/env python3

""""
author: Armin Dedic
St.number: 342615
Assignment 2: fastQ parser that calculates the average quality
score per base for all reads in a fastQ file.

This is the clients script which contains the calculation part. It creates a manager and clients.
The clients connects to the server manager which together work on the job of calculating phred scores (assignment1).
Each client does its own part to run on different machines. When all work is completed, the results will be returned
from the master script, and can even be visualized from an output file.
"""

import sys
import multiprocessing as mp
from multiprocessing.managers import BaseManager
from multiprocessing.managers import SyncManager
import time
import os


def fastq_parser(fastqfile, shared_job_q,  shared_result_q):
    """
    this method reads the fastQ file and calculates the average quality score per base based on the concept
    of multiprocessing. By dividing the file in parts, using the seek function to jump into those parts. Using the
    tell() function to known the current position of the file. Each process (of the amount of process provided) will
    handle its own part. At the end those parts results will merge together to produce one output result.
    """

    fastqparts, end_part = shared_job_q.get()
    data = open(fastqfile)
    scores = []
    count = 0
    data.seek(fastqparts)
    read = False
    counter = 1
    end = False

    while True:
        line = data.readline()
        if line.startswith("@DE"):
            if len(line) > 60:
                data.readline()
            read = True

        if read:
            if (counter % 4) == 0:
                count += 1
                for index, char in enumerate(line.encode("ascii")):
                    if len(scores) == index:
                        scores.append(0)
                    scores[index] += char - 33
            counter += 1

        if data.tell() >= end_part:
            end = True
            break

        if not line:
            break
    results = [item / count for item in scores]
    if end:
        shared_result_q.put(results)


def run_client():
    # master machine, random port and key provided
    manager = make_client_manager('bin150', 3419, b'lol')
    job_q = manager.get_job_q()
    result_q = manager.get_result_q()
    worker(job_q, result_q, sys.argv[1])


def make_client_manager(ip, port, authkey):
    """ Create a manager for the clients to connect to a server on the
        given address and exposes the get_job_q and get_result_q methods for
        accessing the shared queues from the server.
        Return a manager object.
    """
    class ServerQueueManager(SyncManager):
        pass

    # This registers both the queues
    ServerQueueManager.register('get_job_q')
    ServerQueueManager.register('get_result_q')

    # Creates a manager to connect to the server of the master
    manager = ServerQueueManager(address=(ip, port), authkey=authkey)
    manager.connect()

    print('Client connected to', ip, port)
    return manager


def worker(shared_job_q, shared_result_q, file):
    # Creates processes for each client, starts it and joins it.
    jobs = []
    new_process = mp.Process(target=fastq_parser, args=(file, shared_job_q, shared_result_q))
    new_process.start()
    jobs.append(new_process)

    for i in jobs:
        i.join()


if __name__ == "__main__":
    start = time.time()
    run_client()
    end = time.time()
    print("processing time: ", end - start, "seconds")



