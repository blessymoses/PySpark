# Spark
Apache Spark is a unified engine designed for large-scale distributed data processing, on premises in data centers or in the cloud.
## Distributed Execution
- a Spark application consists of a driver program that is responsible for orchestrating parallel operations on the Spark cluster. 
- The driver accesses the distributed components in the cluster — the Spark executors and cluster manager — through a SparkSession.
## Cheat sheet for Spark deployment modes
| Mode | Spark driver | Spark executor | Cluster manager |
| --- | --- | --- | --- |
| Local | Runs on a single JVM, like a laptop or single node | Runs on the same JVM as the driver | Runs on the same host |
| Standalone | Can run on any node in the cluster | Each node in the cluster will launch its own executor JVM | Can be allocated arbitrarily to any host in the cluster |
| YARN (client) | Runs on a client, not part of the cluster | YARN’s NodeManager’s container | YARN’s Resource Manager works with YARN’s Application Master to allocate the containers on NodeManagers for executors |
| YARN (client) | Runs with the YARN Application Master | Same as YARN client mode | Same as YARN client mode |
| Kubernetes | Runs in a Kubernetes pod | Each worker runs within its own pod | Kubernetes Master |