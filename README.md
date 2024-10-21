# MySQL Replication Spike

## Overview

This project demonstrates setting up MySQL replication using Docker Compose. The setup includes a master MySQL server and a slave MySQL server that replicates data from the master. Additionally, a data generator service is included to insert random data into the master and verify that it is replicated to the slave.

### Goals

- Understand how to configure MySQL replication using Docker containers.
- Implement a data generator that interacts with the master database.
- Ensure data consistency between the master and slave databases.

## Architecture

The project is structured into three main services:

1. **Master Service**: 
   - Runs the master MySQL server.
   - Configured with environment variables to set the root password, database name, user, and password.
   - Initializes with a configuration file and an SQL script to create the initial database structure.

1. **Slave Service**: 
   - Runs the slave MySQL server.
   - Connects to the master for replication.
   - Configured to wait for the master to be healthy before starting.

1. **Data Generator Service**: 
   - A Python service that inserts random data into the master database.
   - Checks for data replication in the slave database.

## Setup Instructions

### Prerequisites

- Docker and Docker Compose must be installed on your machine.

## Build and Start the Services

1. Navigate to the directory containing the docker-compose.yml file.
1. Run the following command to build and start the services:

```bash
docker-compose up --build
```
3. The services will be started, and you can monitor the logs to see the replication in action.

## Accessing the MySQL Databases

* You can connect to the master database using the following command:

```bash
mysql -h localhost -u bugs -p -D bugs
```

* To connect to the slave database, use:

```bash
mysql -h localhost -P 3307 -u bugs -p -D bugs
```

## Testing Data Replication

1. The data generator service will run indefinitely, inserting data into the master database.
1. You can check the logs of the slave service to verify that the data is replicated correctly.

```bash
data-generator  | Inserting data into master...
data-generator  | Master has 1 rows in random_data.
data-generator  | Waiting for replication...
data-generator  | Connecting to slave...
data-generator  | Slave has 1 rows in random_data.
data-generator  | Data replicated successfully.
```

## Stopping the Services

To stop the services, use:

```bash
docker-compose down
```

## Project Structure

```
.
├── docker-compose.yml        # Main configuration for Docker Compose
├── data-gen                  # Directory containing the data generator service
│   ├── Dockerfile            # Dockerfile for the data generator
│   └── data_gen.py           # Python script for generating and checking data
├── master                    # Directory for master MySQL configuration
│   ├── my.cnf                # MySQL configuration file
│   └── master-init.sql       # SQL script for initializing the master database
└── slave                     # Directory for slave MySQL configuration
    ├── my.cnf                # MySQL configuration file
    └── slave-init.sh         # Script for initializing the slave database
```

### Configuration Files Explained 

**my.cnf**

The my.cnf files for both master and slave contain MySQL configuration settings that enable replication. Key settings may include:

* `server-id`: A unique identifier for each server in the replication setup.  
* `log_bin`: Enables binary logging, which is necessary for replication.
* `bind-address`: Specifies the IP address on which MySQL listens for connections (set to `0.0.0.0` to accept connections from any host).


#### Example Configuration for my.cnf (Master)

```ini
[mysqld]
server-id=1
log-bin=mysql-bin
binlog_do_db=bugs 
bind-address=0.0.0.0
```

#### Example Configuration for my.cnf (Slave)

```ini
[mysqld]
server-id=2
relay-log=relay-log
log_bin=mysql-bin
binlog_do_db=bugs 
replicate-do-db=bugs
bind-address=0.0.0.0
```

**master-init.sql**

`master-init.sql`: This SQL script is executed when the master MySQL server is initialized. It can contain commands setup `bugs` user and set permissions to enable replication.

```sql
CREATE USER IF NOT EXISTS 'bugs'@'%' IDENTIFIED BY 'bugs';
GRANT REPLICATION SLAVE, REPLICATION CLIENT, SUPER ON *.* TO 'bugs'@'%';
FLUSH PRIVILEGES;
```

**slave-init.sh**

`slave-init.sh`: This shell script is executed when the slave MySQL server is initialized. It is responsible for configuring the slave to connect to the master, setting up replication, and starting the slave process. It typically uses the `CHANGE MASTER TO` command to specify the master server and the log file and position from which to start replication.

```bash
#!/bin/bash

# Wait for the master to be ready
until mysql -h"$MASTER_HOST" -P"$MASTER_PORT" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" -e "SHOW MASTER STATUS\G"; do
  echo "Waiting for master to be ready..."
  sleep 5
done

# Set up replication
MASTER_LOG_FILE=$(mysql -h"$MASTER_HOST" -P"$MASTER_PORT" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" -e "SHOW MASTER STATUS\G" | grep File | awk '{print $2}')
MASTER_LOG_POS=$(mysql -h"$MASTER_HOST" -P"$MASTER_PORT" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" -e "SHOW MASTER STATUS\G" | grep Position | awk '{print $2}')

mysql -uroot -p"$MYSQL_ROOT_PASSWORD" -e "CHANGE MASTER TO MASTER_HOST='$MASTER_HOST', MASTER_USER='$MYSQL_USER', MASTER_PASSWORD='$MYSQL_PASSWORD', MASTER_LOG_FILE='$MASTER_LOG_FILE', MASTER_LOG_POS=$MASTER_LOG_POS; START SLAVE;"
```

## References

* [mysql-replica-server](https://github.com/Siddhant-K-code/mysql-replica-server)
* [Setting the Replication Source Configuration](https://dev.mysql.com/doc/mysql-replication-excerpt/8.0/en/replication-howto-masterbaseconfig.html)

## Conclusion

This spike serves as a foundational step in understanding MySQL replication using Docker. It provides an opportunity to explore database consistency, replication mechanisms, and automated data generation.