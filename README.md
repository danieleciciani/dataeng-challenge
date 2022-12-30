# dataeng-challenge
Truefilm Data Engineering Challenge

This guide contains instructions on the steps/tools setup/prerequisite to execute the project, and an explanation relating to the choices made.
In particular:

* Tools & Languages
* Solution details
* Pipeline execution
* Explainations
* Unit Test
 
### **1. Tools & Languages**

* Python 3.7
* Spark 3.3.1
* Docker (docker-compose)
* Airflow 2.5


### **2. Solution details**
The solution consist on the use python and Spark (pyspark) to develop two airflow pipelines, one end2end that download data, process it, calculate the  hight profit movies and one that apply unit testing on the code.
All the infrastracture is managed by docker-compose, that deploy a non productive airflow deployment plus a target postgres container as target of the high profit pipeline. Moreover, a customized airflow image with Spark is build and used during the container provisioning.


### **3. Pipelines execution**
#### Pre Requisites:
* Docker: need to be installed and running on the machine: Get docker for mac/unix/windows here: https://docs.docker.com/get-docker/
* Docker volumes: create this two volumes once docker is installed:
 - `docker volume create --name truelayer_postgres-db-volume`
 - `docker volume create --name truelayer_postgres-db-volume-etl`
* Memory assigned 16 GB of memory and 4 cpu to Docker: From `Docker > Preferences > Resources > Advanced`. More info here: https://docs.docker.com/desktop/settings/windows/
* Git: need to be installed to clone this project: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

#### Steps:


### **4. Explainations**



### **5. Unit Test**




