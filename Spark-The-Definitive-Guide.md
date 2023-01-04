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
## Partitions
- To allow every executor to perform work in parallel, Spark breaks up the data into chunks called `partitions`. 
- A partition is a collection of rows that sit on one physical machine in your cluster. 
- A DataFrame’s partitions represent how the data is physically distributed across the cluster of machines during execution. 
- If you have one partition, Spark will have a parallelism of only one,
even if you have thousands of executors. 
- If you have many partitions but only one executor, Spark will still have a parallelism of only one because there is only one computation resource.
## Transformations
- In Spark, the `core data structures are immutable`, meaning they cannot be changed after they’re created.
- To “change” a DataFrame, you need to instruct Spark how you would like to
modify it to do what you want. These instructions are called transformations.
- Spark will not act on transformations until we call an action.
- Two types of transformations:
  - `Narrow transformations`: Transformations consisting of narrow dependencies are those for which each input partition will contribute to only one output partition.
    - With narrow transformations, Spark will automatically perform an operation called `pipelining`, meaning that if we specify multiple filters on DataFrames, they’ll all be performed in-memory.
  - `Wide transformation`: A wide dependency style transformation will have input partitions contributing to many output partitions. This is referred to as a `shuffle` whereby Spark will exchange partitions across the cluster.
    - When we perform a shuffle, Spark writes the results to disk.
## Lazy Evaluation
- Lazy evaulation means that Spark will wait until the very last moment to execute the graph of computation instructions. 
- In Spark, instead of modifying the data immediately when you express
some operation, you build up a `plan` of transformations that you would like to apply to your source data. 
- By waiting until the last minute to execute the code, Spark compiles this plan from your raw DataFrame transformations to a streamlined `physical plan` that will run as efficiently as possible across the cluster.
- `predicate pushdown`:
  - If we build a large Spark job but specify a filter at the end that only requires us to fetch one row from our source data, the most efficient way to execute this is to access the single record that we need. 
  - Spark will actually optimize this for us by pushing the filter down
automatically.
## Actions
- Transformations allow us to build up our logical transformation plan. 
- To trigger the computation, we run an action. 
- An `action` instructs Spark to compute a result from a series of transformations.
- There are three kinds of actions:
  - Actions to view data in the console
  - Actions to collect data to native objects in the respective language
  - Actions to write to output data sources
## Spark UI
- You can monitor the progress of a job through the Spark web UI. 
- The Spark UI is available on `port 4040 of the driver node`.
- If you are running in local mode, this will be http://localhost:4040.
- The Spark UI displays information on the state of your Spark jobs, its environment, and cluster state.
- `A Spark job represents a set of transformations triggered by an individual action, and you can monitor that job from the Spark UI`.
```python
myRange = spark.range(1000).toDF("number")

divisibleBy2 = myRange.where("number % 2 = 0")

divisibleBy2.count()

flight_data_2015 = spark.read.option("inferSchema", "true").option("header", "true").csv("data/flight-data/csv/2015-summary.csv")

flight_data_2015.sort("count").explain() # call explain on any DataFrame object to see the DataFrame’s lineage (or how Spark will execute this query)

```
p31