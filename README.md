# Big data #

* Name: Armin Dedić

### What is this repository for? ###
* This repository is for submitting assignments.

### Assignment 1 ###
The first assignment is about creating an fastqparser which calculates the average phredscore per base. This
is based up on a multiprocessing concept in which the user has to provide the number of processes. Each process
will then handle its own part of the file. This will produce results which will be merged together.

### Assignment 2 ###
This assignment continues on from the first assignment, but now it creates a master server manager and a client
manager. The master will connect to the server, for the clients to be able to connect to that server manager. 
The master manager will make sure that each client (now based up on different computer machines) processes a part
of the file. When all clients (machines) completes their jobs, the master will then return the final results.

### Assignment 3 ###
For the third assignment, the perigrine cluster from the RUG university is used. The script of the first
assignment is used without changes. A perigrine.sh bash script is created which executes the Python script by calling 
the script from it. Given the amount of memory and cpu per task, it will perform basically the same as the 
first assignment but now on a cluster.

### Assignment 4 ###
Unfortunately, I did not manage to complete this assignment, but I still can provide my view and approach. 
The fourth assignment will continue with the script of the second assignment. This time, it is based up on 
a peer to peer concept. So it is
necessary to find out where you are and where everybody else is. This can be done by doing a broadcast message.
To be able to communicate with the other nodes (machines), sockets are used. And then the same function
of calculation applies to produce those results.

## Assignment 5 ##
This assignment will be a small documentation on the comparison of the previous assignments. To provide
my own opinion and give the feedback. Also to give a summary of what Spark is and how it would be implemented
this case. 

## Usage ##
* Python3 <PYTHON SCRIPT> <FASTQ FILE> -n <number of processes> <output file name> 
