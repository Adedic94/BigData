#!/usr/bin/env python3

""""
author: Armin Dedic
St.number: 342615
Assignment 1: fastQ parser that calculates the average quality
score per base for all reads in a fastQ file.
"""

import sys
import multiprocessing as mp
import time
import os


def fastq_parser(fastqfile, fastqparts, queue, end_part):
    """
    this method reads the fastQ file and calculates the average quality score per base based on the concept
    of multiprocessing. By dividing the file in parts, using the seek function to jump into those parts. Using the
    tell() function to known the current position of the file. Each process (of the amount of process provided) will
    handle its own part. At the end those parts results will merge together to produce one output result.
    """
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
        queue.put(results)


if __name__ == "__main__":
    start = time.time()
    fastq_file_size = os.path.getsize(sys.argv[1])
    fastq_file_parts = fastq_file_size / int(sys.argv[3])
    fastq_process_part = 0
    queue = mp.Queue()
    jobs = []

    # Setup a list of processes provided by the number of the third argument in the cmdline. It calls the function
    # and provides the arguments needed to produce the results.
    for i in range(int(sys.argv[3])):
        new_process = mp.Process(target=fastq_parser, args=((sys.argv[1]), fastq_process_part,  queue,
                                                            fastq_process_part + fastq_file_parts))
        fastq_process_part += fastq_file_parts
        new_process.start()
        jobs.append(new_process)

    # Joins all the processes
    for items in jobs:
        items.join()

    # gets the process results from the queue
    queue_result = [queue.get() for num in range(queue.qsize())]
    final_results = [sum(item) / int(sys.argv[3]) for item in zip(*queue_result)]
    print(final_results)
    print(len(final_results))

    # Writes the output to a new file
    with open(sys.argv[4], 'w') as output_file:
        for items in final_results:
            output_file.write(str(items))
            output_file.write('\n')
    end = time.time()
    print("processing time: ", end - start, "seconds")

