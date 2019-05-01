Authors:
Jake Johnson
Dawson Canby
Prashant Thakur

To Compile and run program:

1. Run ./create-link.sh, this will create the links for kafka and zookeeper
2. Run ./run_cluster zookeeper/ start | stop
3. Run ./run_cluster kafka/ start | stop
4. Run gradle build and them ./submit-job.sh, this will start the spark job
5. (Optional) For a graphic visualization of the data run graph.py

NOTE:
    You must have kafka and zookeeper set up on your machine in order to run this program.
