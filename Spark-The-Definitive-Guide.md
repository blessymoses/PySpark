# Spark’s Basic Architecture
- Framework that is managing and coordinating the execution of tasks on data across a cluster of computers.
- The cluster of machines that Spark will use to execute tasks is managed by a cluster manager like Spark’s standalone cluster manager, YARN, or Mesos. We then submit Spark Applications to these cluster managers, which will grant resources to our application so that we can complete our work.
## Spark Applications
- Spark Applications consist of a `driver` process and a set of `executor` processes.
- The driver process runs your main() function, sits on a node in the cluster, and is responsible for three things:
  - maintaining information about the Spark Application; 
  - responding to a user’s program or input;
  - analyzing, distributing, and scheduling work across the executors
- The executors are responsible for actually carrying out the work that the driver assigns them. This means that each executor is responsible for only two things: 
  - executing code assigned to it by the driver, and 
  - reporting the state of the computation on that executor back to the driver node.
- `local mode`
  - In local mode, the driver and executors run (as threads) on your individual computer instead of a cluster.
- Spark employs a cluster manager that keeps track of the resources available.
- The driver process is responsible for executing the driver program’s commands across the executors to complete a given task.
## Spark’s Language APIs
- Spark presents some core “concepts” in every language; these
concepts are then translated into Spark code that runs on the cluster of machines.
- Each language API maintains the same core concepts. There is a `SparkSession object available to the user, which is the entrance point to running Spark code`.
- When using Spark from Python or R, you don’t write explicit JVM instructions; instead, you write Python and R code that Spark translates into code that it then can run on the executor JVMs.
## The SparkSession
- You control your Spark Application through a driver process called the SparkSession. 
- The SparkSession instance is the way Spark executes user-defined manipulations across the cluster. 
- There is a one-to-one correspondence between a SparkSession and a Spark Application.

```python
myRange = spark.range(1000).toDF("number")
```

p24