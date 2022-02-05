# Data Engineering using Apache Spark

Spark uses two key components – a distributed file storage system, and a cluster manager to manage workloads.

## Spark Cluster Manager

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