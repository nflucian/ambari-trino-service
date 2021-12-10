# Ambari Service for Trino
Ambari service for easily installing and managing Trino on HDP clusters.
Trino is a distributed SQL query engine designed to query large data sets distributed over one or more heterogeneous data sources.

- Requirements:
  - Linux operating system
    -  64-bit required
    -  newer release preferred, especially when running on containers
    -  adequate ulimits for the user that runs the Trino process. These limits may depend on the specific Linux distribution you are using. The number of open file descriptors needed for a particular Trino instance scales as roughly the number of machines in the cluster, times some factor depending on the workload. We recommend the following limits, which can typically be set in /etc/security/limits.conf:
    ```
    trino soft nofile 131072
    trino hard nofile 131072
    ```
  - Java runtime environment
    - Trino requires a 64-bit version of Java 11, with a minimum required version of 11.0.11.
  - Python
    - version 2.6.x, 2.7.x, or 3.x