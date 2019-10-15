#!/bin/bash
#SBATCH --time 2:00:00
#SBATCH --nodes=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=4000

module load protobuf-python/3.4.0-foss-2016a-Python-3.5.2

python3 Assignment1_multiprocessing_calculating_averagePhredscore.py ../rnaseq.fastq -n 4 output.csv
