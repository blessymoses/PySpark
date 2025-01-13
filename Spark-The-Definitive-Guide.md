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
    - filter() and contains() represent narrow transformations because
they can operate on a single partition and produce the resulting output partition
without any exchange of data.
  - `Wide transformation`: A wide dependency style transformation will have input partitions contributing to many output partitions. This is referred to as a `shuffle` whereby Spark will exchange partitions across the cluster.
    - When we perform a shuffle, Spark writes the results to disk.
    - groupBy() or orderBy() instruct Spark to perform wide transformations,
where data from other partitions is read in, combined, and written to disk.
    - The Spark SQL shuffle is a mechanism for redistributing or re-partitioning data so that the data is grouped differently across partitions
    - Spark shuffle is a very expensive operation as it moves the data between executors or even between worker nodes in a cluster so try to avoid it when possible. When you have a performance issue on Spark jobs, you should look at the Spark transformations that involve shuffling.
    - DataFrame operations that trigger shufflings are join(), and all aggregate functions.
## Lazy Evaluation
- Lazy evaulation means that Spark will wait until the very last moment to execute the graph of computation instructions. 
- In Spark, instead of modifying the data immediately when you express
some operation, you build up a `plan` of transformations that you would like to apply to your source data. 
- By waiting until the last minute to execute the code, Spark compiles this plan from your raw DataFrame transformations to a streamlined `physical plan` that will run as efficiently as possible across the cluster.
- `predicate pushdown`:
  - If we build a large Spark job but specify a filter at the end that only requires us to fetch one row from our source data, the most efficient way to execute this is to access the single record that we need. 
  - Spark will actually optimize this for us by pushing the filter down
  - Use the EXPLAIN command to see the query plan
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
## DataFrames and SQL
- `With Spark SQL, you can register any DataFrame as a table or view (a temporary table) and query it using pure SQL`. 
- There is no performance difference between writing SQL queries or writing DataFrame code, they both “compile” to the same underlying plan that we specify in DataFrame code.
- You can make any DataFrame into a table or view with one simple method call:
df.`createOrReplaceTempView`("flight_data_2015_view")
- The `execution plan is a directed acyclic graph (DAG) of transformations`,
each resulting in a new immutable DataFrame, on which we call an action to generate a result.
```python
myRange = spark.range(1000).toDF("number")

divisibleBy2 = myRange.where("number % 2 = 0")

divisibleBy2.count()

flight_data_2015 = spark.read.option("inferSchema", "true").option("header", "true").csv("data/flight-data/csv/2015-summary.csv")

flight_data_2015.sort("count").explain() # call explain on any DataFrame object to see the DataFrame’s lineage (or how Spark will execute this query)

flight_data_2015.sort("count").take(2)

# By default, when we perform a shuffle, Spark outputs 200 shuffle partitions.
# to reduce the number of the output partitions from the shuffle:
spark.conf.set("spark.sql.shuffle.partitions", "5")

flight_data_2015.createOrReplaceTempView("flight_data_2015_view")

sqlWay = spark.sql("""
SELECT DEST_COUNTRY_NAME, count(1)
FROM flight_data_2015_view
GROUP BY DEST_COUNTRY_NAME
""")

dataFrameWay = flight_data_2015.groupBy("DEST_COUNTRY_NAME").count()

spark.sql("SELECT max(count) from flight_data_2015_view").take(1)

from pyspark.sql.functions import max
flight_data_2015.select(max("count")).take(1)

maxSql = spark.sql("""
SELECT DEST_COUNTRY_NAME, sum(count) as destination_total
FROM flight_data_2015_view
GROUP BY DEST_COUNTRY_NAME
ORDER BY sum(count) DESC
LIMIT 5
""")

from pyspark.sql.functions import desc
flight_data_2015\
.groupBy("DEST_COUNTRY_NAME")\
.sum("count")\
.withColumnRenamed("sum(count)", "destination_total")\
.sort(desc("destination_total"))\
.limit(5)\
.show()
```
# Structured API Overview
- The Structured APIs are a tool for manipulating all sorts of data, from unstructured log files to semi-structured CSV files and highly structured Parquet files. 
- These APIs refer to three core types of distributed collection APIs:
  - Datasets
  - DataFrames
  - SQL tables and views
## Schemas
- A schema defines the column names and types of a DataFrame. 
- You can define schemas manually or read a schema from a data source (often called `schema on read`).
## Structured Spark Types
- Internally, Spark uses an engine called `Catalyst` that maintains its own type information through the planning and processing of work.
- Spark types map directly to the different language APIs that Spark maintains and there exists a lookup table for each of these in Scala, Java, Python, SQL, and R.
- Even if we use Spark’s Structured APIs from Python or R, the majority of our manipulations will operate strictly on Spark types, not Python types.
## DataFrames Versus Datasets
- “untyped” DataFrames and the “typed” Datasets.
- Spark maintains the DataFrame's types completely and only checks whether those types line up to those specified in the schema at `runtime`.
- Datasets, on the other hand, check whether types conform to
the specification at `compile time`. 
- Datasets are only available to Java Virtual Machine (JVM)–based languages (Scala and Java) and we specify types with case classes or Java beans.
- The `“Row” type` is Spark’s internal representation of its optimized
in-memory format for computation. This format makes for highly specialized and efficient computation because rather than using JVM types, which can cause high garbage-collection and object instantiation costs, Spark can operate on its own internal format without incurring any of those costs. 
- To Spark (in Python or R), there is no such thing as a Dataset: everything is a
DataFrame and therefore we always operate on that optimized format.
- `when you’re using DataFrames, you’re taking advantage of Spark’s
optimized internal format`. This format applies the same efficiency gains to all of Spark’s language APIs.
## Columns
Columns represent a simple type like an integer or string, a complex type like an array or map, or a null value.
## Rows
- A row is nothing more than a record of data. Each record in a DataFrame must be of type Row
- We can create these rows manually from
SQL, from Resilient Distributed Datasets (RDDs), from data sources, or manually from scratch.
## Python type reference
| Data type | Value type in Python | API |
| --- | --- | --- |
| ByteType | int or long. numbers are within the range of –128 to 127. | ByteType() |
| ShortType | int or long. numbers are within the range of –32768 to 32767. | ShortType() |
| IntegerType | int or long. Python has a lenient definition of “integer.”. Numbers that are too large will be rejected by Spark SQL if you use the IntegerType(). It’s best practice to use LongType. | IntegerType() |
| LongType | long. numbers are within the range of –9223372036854775808 to 9223372036854775807. Otherwise, convert data to decimal.Decimal and use DecimalType. | LongType() |
| FloatType | float. Numbers will be converted to 4-byte single-precision floating-point numbers at runtime. | FloatType() |
| DoubleType | float | DoubleType() |
| DecimalType | decimal.Decimal | DecimalType() |
| StringType | string | StringType() |
| BinaryType | float | BinaryType() |
| BooleanType | bool | BooleanType() |
| TimestampType | datetime.datetime | TimestampType() |
| DateType | datetime.date | DateType() |
| ArrayType | list, tuple, or array | ArrayType(elementType, [containsNull]). Note: The default value of containsNull is True.() |
| MapType | dict | MapType(keyType, valueType, [valueContainsNull]). Note: The default value of valueContainsNull is True. |
| StructType | list or tuple | StructType(fields). Note: fields is a list of StructFields. Also, fields with the same name are not allowed. |
| StructField | The value type in Python of the data type of this field (for example, Int for a StructField with the data type IntegerType) | StructField(name, dataType, [nullable]) Note: The default value of nullable is True. |
## Structured API Execution
Execution steps of a single structured API query from user code to executed
code:
1. Write DataFrame/Dataset/SQL Code.
2. If valid code, Spark converts this to a `Logical Plan`.
3. Spark transforms this Logical Plan to a `Physical Plan`, checking for optimizations along the way.
4. Spark then executes this Physical Plan (RDD manipulations) on the cluster.
- To execute code, we must write code. This code is then submitted to Spark either through the console or via a submitted job. This code then passes through the `Catalyst Optimizer, which decides how the code should be executed and lays out a plan for doing so` before, finally, the code is run and the result is returned to the user.
### Logical Planning
User code --> Unresolved logical plan --> (Analysis) Catalog --> Resolved logical plan --> (Logical optimization) --> Optimized logical plan
- The first phase of execution is meant to take user code and convert it into a logical plan.
- This plan is unresolved because although your code might be valid, the tables or columns that it refers to might or might not exist. 
- Spark uses the `catalog`, a repository of all table and DataFrame information,to resolve columns and tables in the analyzer. 
- The analyzer might reject the unresolved logical plan if the required table or column name does not exist in the catalog. 
- If the analyzer can resolve it, the result is passed through the `Catalyst Optimizer`, `a collection of rules that attempt to optimize the logical plan by pushing down predicates or selections`.
- Packages can extend the Catalyst to include their own rules for domain-specific optimizations.
### Physical Planning
- After successfully creating an optimized logical plan, Spark then begins the physical planning process. 
- The physical plan, often called a `Spark plan, specifies how the logical plan will execute on the cluster by generating different physical execution strategies and comparing them through a cost model`.
### Execution
- Upon selecting a physical plan, Spark runs all of this code over RDDs, the lower-level programming interface of Spark.
- Spark performs further optimizations at runtime, generating native Java bytecode that can remove entire tasks or stages during execution. 
- Finally the result is returned to the user.
```python
df = spark.range(500).toDF("number")
df.select(df["number"]+10)

spark.range(2).collect()

from pyspark.sql.types import *
 b = ByteType()

strings = spark.read.text("README.md")
filtered = strings.filter(strings.value.contains("Spark"))
filtered.count()
```
# Review
- Spark is a distributed programming model in which the user specifies `transformations`. 
- Multiple transformations build up a `directed acyclic graph` of instructions. 
- An action begins the process of executing that graph of instructions, as a single job, by breaking it down into stages and tasks to execute across the cluster. 
- The logical structures that we manipulate with transformations and actions
are DataFrames and Datasets. 
- To create a new DataFrame or Dataset, you call a `transformation`. 
- To start computation or convert to native language types, you call an `action`.

- Data engineering concepts
  - High scalability: to scale HDFS horizontally when the data increase, add more data nodes
  - High Availability: this is handled using replication factor; default is 3
  - High latency: the system takes longer to respond; like MapReduce Batch jobs
  - Low latency: near real-time response from the system; HBase is meant for quick searching. when you fire a query, you get the results immediately
