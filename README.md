# Data Engineering using Apache Spark

Spark uses two key components – a distributed file storage system, and a cluster manager to manage workloads.

## Spark Cluster Managers
- local[n]
- YARN
- Kubernetes
- Mesos
- Standalone
### YARN
- YARN is an application-level scheduler.
- JVM-based cluster-manager of hadoop.
- aware of available resources and actively assigns tasks to those resources.
- YARN was purpose built to be a resource scheduler for Hadoop jobs.
- `How does YARN work?`
  - A YARN cluster consists of many hosts, some of which are `Master hosts`, while most are `Worker hosts`. 
  - A `ResourceManager` handles resources at the cluster level, while a `NodeManager` manages resources at the individual host level. They keep track of the vcores and memory at both cluster and local host level.
  - When an application like Spark runs on YARN, the ResourceManager and NodeManager assess the available resources on the cluster and allocate each container to a host. The key job of YARN is to manage resources and schedule tasks on a cluster.
- `Limitations:`
  - YARN falls short in aspects such as version and dependency control, isolating jobs from each other, and optimal resource allocation.
  - In order to run multiple workloads you need dedicated clusters for each workload type.
  - Because YARN falls short with job isolation, it requires setting up and tearing down the cluster for every new job that needs to be run. This incurs costs, is an error prone process, and wastes compute resources. 
### Mesos
- Mesos is an OS-level scheduler.
- It reports on available resources and expects the framework to choose whether to execute the job or not.
### Kubernetes
- decouples workloads from the infrastructure they are run on.
- outperforms YARN at processing speeds.
- `How does Spark-on-k8s work?`
  - submit Spark apps using spark-submit or using the spark-operator.
  - This request contains the full application configuration including the code and dependencies to run (packaged as a docker image or specified via URIs), the infrastructure parameters, (e.g. the memory, CPU, and storage volume specs to allocate to each Spark executor), and the Spark configuration.
  - Kubernetes takes this request and starts the Spark driver in a Kubernetes pod.
  - The Spark driver can then directly talk back to the Kubernetes master to request executor pods, scaling them up and down at runtime according to the load if dynamic allocation is enabled. 
  - Kubernetes takes care of the bin-packing of the pods onto Kubernetes nodes (the physical VMs), and will dynamically scale the various node pools to meet the requirements.
- `Benefits`:
  - Containerization: Build your dependencies once, run everywhere.
  - Dependency management: Package all dependencies along with Spark applications in containers. This avoids dependency issues that are common with Spark.
  - Multi-tenancy: Kubernetes’ Resource Quota, and Namespaces bring greater control over how applications consume and share system resources.
  - Swappable backed infrastructure means Spark applications are now portable across hybrid cloud setups.
  - Kubernetes Role and ClusterRole features allow you to set fine-grained permissions for resources and organize these permissions based on API groups.
  - Tag container images for version control which facilitates better auditing, and ability to rollback failed deployments.
  - The Kubernetes ecosystem is blooming with powerful open source add-ons for management & monitoring. Prometheus for time-series data, Fluentd for log aggregation, and Grafana for data visualization are a few of the notable examples.
  - GitOps allows you to manage infrastructure and application deployments declaratively. Flux and Argo are two leading GitOps tools that enable this.
  - When it comes to set up, you can use Helm charts to install, manage, and version control packages and their dependencies.
### local[n]
- n: number of threads
- n[1]: only one thread for Driver program
- n[3]: one thread for Driver and 2 threads for Executors
- local[*]: Run Spark locally with as many worker threads as logical cores on your machine.

## Spark Execution Model
### Spark execution methods
- Interactive clients
  - spark-shell
  - Notebook
- Submit job
  - spark-submit, Rest API
### Spark execution modes
- Client mode
  - spark-shell, Notebook
    - Driver runs in the client machine
    - Executors are started in the Spark Cluster
    - Logging off from client machine kills driver as well as executors
- Cluster mode
  - Driver & executors run in the Spark Cluster
  - Logging off from client machine does not impact the submitted job

## Spark Configurations
`Spark application configuration precedence`:
environment variable -> spark-defaults.conf -> spark-submit command line -> SparkConf

All available spark application properties:
https://spark.apache.org/docs/latest/configuration.html#application-properties

- `spark.master`: specifies the Spark Cluster Manager
- `spark.yarn.app.container.log.dir`: set this if you need a reference to the proper location to put log files in the YARN so that YARN can properly display and aggregate them
  - This variable is used by YARN log aggregator to find the application log files
  - log4j file appender will create log files in this directory
- `spark.driver.extraJavaOptions`: A string of extra JVM options to pass to the driver.

## Using Log4J with PySpark
1. Create a Log4J configuration file
2. Configure Spark JVM to pickup the Log4J configuration file
3. Create a Python class to get Spark Log4J instance and use it
### Log4J components
1. Logger: set of APIs that are going to be used
2. Configurations: are loaded at the runtime
3. Appender: output destinations like console or log files

## Spark Session
- SparkSession is a singleton object.
- Each spark application can have only one active SparkSession.
### Configuring Spark Session:
1. Environment variables
2. SPARK_HOME/conf/spark-defaults.conf
3. spark-submit command line options
4. SparkConf Object

## Installing Apache Spark
- install jdk 8 or 11
```sh
# install java
$ apt-get install default-jdk

# find java_home in ubuntu
$ update-alternatives --list java

# set JAVA_HOME
$ export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64
```
- `To install spark`:
```sh
$ wget https://dlcdn.apache.org/spark/spark-3.3.0/spark-3.3.0-bin-hadoop2.tgz

$ tar xf spark-3.3.0-bin-hadoop2.tgz

$ export SPARK_HOME=/home/codingfairy/sparkdist/spark-3.3.0-bin-hadoop2

$ export PATH=$PATH:$SPARK_HOME/bin

# $ export PYSPARK_PYTHON=python3

# start a spark shell, :q to exit
$ spark-shell

# start a pyspark shell, ctrl+d to exit
$ pyspark
```
- `To use the PySpark which is included in the spark distribution`:
  - Ensure that `SPARK_HOME` is set.
  - Update PYTHONPATH environment variable such that it can find the PySpark and Py4J under `SPARK_HOME/python/lib`.
```sh
$ export PYTHONPATH=$(ZIPS=("$SPARK_HOME"/python/lib/*.zip); IFS=:; echo "${ZIPS[*]}"):$PYTHONPATH
```
- `bashrc`:
```sh
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export SPARK_HOME=/home/codingfairy/sparkdist/spark-3.3.0-bin-hadoop2
export PATH=$PATH:$SPARK_HOME/bin
export PYTHONPATH=$(ZIPS=("$SPARK_HOME"/python/lib/*.zip); IFS=:; echo "${ZIPS[*]}"):$PYTHONPATH
```

## HDFS
- Data is stored in block size of 128MB and each block is replicated 3 times(configurable).
- Atleast 2 data nodes are needed for replication.

### Installing Hadoop - Single Node Hadoop Deployment
- Download Hadoop from https://hadoop.apache.org/releases.html
```sh
 wget https://dlcdn.apache.org/hadoop/common/hadoop-3.3.4/hadoop-3.3.4.tar.gz

tar xzf hadoop-3.3.4.tar.gz
```
- A Hadoop environment is configured by editing a set of configuration files:

  - bashrc
  - hadoop-env.sh
    - The hadoop-env.sh file serves as a master file to configure YARN, HDFS, MapReduce, and Hadoop-related project settings.
    - When setting up a single node Hadoop cluster, you need to define which Java implementation is to be utilized.
  - core-site.xml
    - The core-site.xml file defines HDFS and Hadoop core properties.
    - To set up Hadoop in a pseudo-distributed mode, you need to specify the URL for your NameNode, and the temporary directory Hadoop uses for the map and reduce process.
  - hdfs-site.xml
    - The properties in the hdfs-site.xml file govern the location for storing node metadata, fsimage file, and edit log file. Configure the file by defining the NameNode and DataNode storage directories.
    - Additionally, the default dfs.replication value of 3 needs to be changed to 1 to match the single node setup.
  - mapred-site-xml
    - define MapReduce values
    - change the default MapReduce framework name value to yarn
  - yarn-site.xml
    - The yarn-site.xml file is used to define settings relevant to YARN. It contains configurations for the Node Manager, Resource Manager, Containers, and Application Master.
- To configure Hadoop Environment Variables in bashrc:

 `bashrc`:
```sh
# Hadoop configuration
export HADOOP_HOME=/home/codingfairy/sparkdist/hadoop-3.3.4
export HADOOP_INSTALL=$HADOOP_HOME
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_COMMON_HOME=$HADOOP_HOME
export HADOOP_HDFS_HOME=$HADOOP_HOME
export YARN_HOME=$HADOOP_HOME
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
export PATH=$PATH:$HADOOP_HOME/sbin:$HADOOP_HOME/bin
export HADOOP_OPTS="-Djava.library.path=$HADOOP_HOME/lib/nativ"
```
`hadoop-env.sh`:
- Open $HADOOP_HOME/etc/hadoop/hadoop-env.sh and set $JAVA_HOME
```sh
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
```
`core-site.xml`:
- $HADOOP_HOME/etc/hadoop/core-site.xml
```xml
<configuration>
<property>
  <name>hadoop.tmp.dir</name>
  <value>/home/hdoop/tmpdata</value>
</property>
<property>
  <name>fs.defaultFS</name>
  <value>hdfs://127.0.0.1:9000</value>
</property>
<property>
  <name>hadoop.proxyuser.hadoop.groups</name>
  <value>*</value>
</property>
<property>
  <name>hadoop.proxyuser.hadoop.hosts</name>
  <value>*</value>
</property>
</configuration>
```
`hdfs-site.xml`:
- $HADOOP_HOME/etc/hadoop/hdfs-site.xml
```xml
<configuration>
<property>
  <name>dfs.namenode.name.dir</name>
  <value>/home/codingfairy/hdoop/dfsdata/namenode</value>
</property>
<property>
  <name>dfs.datanode.data.dir</name>
  <value>/home/codingfairy/hdoop/dfsdata/datanode</value>
</property>
<property>
  <name>dfs.replication</name>
  <value>1</value>
</property>
</configuration>
```
`mapred-site.xml`:
- $HADOOP_HOME/etc/hadoop/mapred-site.xml
```xml
<configuration> 
<property> 
  <name>mapreduce.framework.name</name> 
  <value>yarn</value> 
</property> 
</configuration>
```
`yarn-site.xml`:
- $HADOOP_HOME/etc/hadoop/yarn-site.xml
```xml
<configuration>
<property>
  <name>yarn.nodemanager.aux-services</name>
  <value>mapreduce_shuffle</value>
</property>
<property>
  <name>yarn.nodemanager.aux-services.mapreduce.shuffle.class</name>
  <value>org.apache.hadoop.mapred.ShuffleHandler</value>
</property>
<property>
  <name>yarn.resourcemanager.hostname</name>
  <value>127.0.0.1</value>
</property>
<property>
  <name>yarn.acl.enable</name>
  <value>0</value>
</property>
<property>
  <name>yarn.nodemanager.env-whitelist</name>   
  <value>JAVA_HOME,HADOOP_COMMON_HOME,HADOOP_HDFS_HOME,HADOOP_CONF_DIR,CLASSPATH_PERPEND_DISTCACHE,HADOOP_YARN_HOME,HADOOP_MAPRED_HOME</value>
</property>
</configuration>
```
- Format HDFS NameNode
```sh
hdfs namenode -format
```
- Start Hadoop Cluster

cd $HADOOP_HOME/sbin

To start the NameNode and DataNode:
```sh
./start-dfs.sh
```
Once the namenode, datanodes, and secondary namenode are up and running, start the YARN resource and nodemanagers:
```sh
./start-yarn.sh
```
To check if all the daemons are active and running as Java processes:
```sh
jps

4560 NameNode
5123 ResourceManager
5587 Jps
4700 DataNode
5247 NodeManager
```
To access Hadoop UI from browser: http://localhost:9870

To access YARN Resource Manager: http://localhost:8088

### Mapreduce
- `MapReduce` is a way of sending computational tasks to a distributed file system.
- A MapReduce job usually splits the input dataset into independent chunks which are processed by the `map tasks` in a completely parallel manner. The framework sorts the outputs of the maps, which are then input to the `reduce tasks`. Typically both the input and the output of the job are stored in a file system.

