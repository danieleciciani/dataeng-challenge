# dataeng-challenge
Truefilm Data Engineering Challenge

This guide contains instructions on the steps/setup/prerequisite to execute the pipelines, and explanations relating the choices made.
In particular:

* Tools & Languages
* Solution Overview
* Pipeline execution
* Explainations
* Unit Test
 
### **1. Tools & Languages**

* Python 3.7
* Spark 3.3.1
* Docker (docker-compose)
* Airflow 2.5


### **2. Solution Overview**
The solution consist on the use python and Spark (pyspark) to develop two airflow pipelines, one end2end that download data, process it, calculate the  hight profit movies and one that apply unit testing on the code.
All the infrastracture is managed by docker-compose, that deploy a non productive airflow deployment plus a target postgres container as target of the high profit pipeline. Moreover, a customized airflow image with Spark is build and used during the container provisioning.


### **3. Pipelines execution**
#### Pre Requisites:
* Docker: need to be installed and running on the machine: Get docker for mac/unix/windows here: https://docs.docker.com/get-docker/
* Docker volumes: create this two volumes once docker is installed:
	- `docker volume create --name truelayer_postgres-db-volume`
  	- `docker volume create --name truelayer_postgres-db-volume-etl`
* Assigned 16 GB of memory and 4 cpu to Docker: From `Docker > Preferences > Resources > Advanced`. More info here: https://docs.docker.com/desktop/settings/windows/
* Git: need to be installed to clone this project: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

#### Steps:
* Clone the repo: `git clone https://github.com/danieleciciani/dataeng-challenge.git`
* cd into dataeng-challenge/
* create the following folders with: `mkdir -p ./logs ./plugins ./output ./data`
* Upload the `movies_metadata.csv` into the ./data folder
* Execute this command to your host user id used to mount the local folder data, dags, output, logs: `echo -e "AIRFLOW_UID=$(id -u)" > .env`
* Execute the build of the customized airflow image with Spark: `docker build . -f Dockerfile --pull --tag airflow-spark-image:0.0.1`
* Once the build is complete, execute the airflow init `docker compose up airflow-init`
* Then, spin up all the containers `docker compose up -d`
* Create the local spark and postgress connection in airflow. Executing
  - `docker exec dataeng-challenge-airflow-webserver-1 airflow connections add --conn-type 'postgres' --conn-host 'postgres_etl' --conn-schema 'truefilm_db' --conn-login 'truefilm' --conn-password "truefilm" --conn-port "5432" 'conn_postgres'`
  - `docker exec dataeng-challenge-airflow-webserver-1 airflow connections add --conn-type 'Spark' --conn-host 'local[*]' 'spark_local'`
* Navigate to Airflow UI at http://localhost:8080, login with `airflow/airflow` and use the interface to execute the two pipeline, clicking in the red section highlited on the screenshot:
  -  truefile_pipeline_orchestrator (main pipeline)
  -  truefile_unit_tests (unit testing)
<img width="1765" alt="image" src="https://user-images.githubusercontent.com/28576091/210083584-b9a34711-1957-4d24-a40b-8788366096da.png">
* Monitor the execution of the pipelines from the UI:
<img width="1758" alt="image" src="https://user-images.githubusercontent.com/28576091/210085257-adb50b72-956a-44b2-9b9f-95887ca152d7.png">


#### Troubleshooting:
If for some reason at the airflow start up the two dags are not visible in the UI, execute the following command in one shell:
* `docker exec dataeng-challenge-airflow-scheduler-1 airflow dags reserialize`

If still not visible, be sure that the project path is inside a parent folder that Docker trust to allow the volume mount. Verify it from `Docker > Preferences > Resources > File sharing`. If not, add it and restart Docker.



### **4. Explainations**
#### Tools
* **Python**: python is a powerful language for data analysis tasks that leverage a great libraries like pandas & numpy. It was used for his simplicity, the native compatibility with Airflow, and for the presence of Spark APIs.
* **Spark**: Spark is one of the main data processing framewok for distributing computation. The reason to choose Spark with pySpark to perform the main data preprocessing part, is to design and develop a system natively ready to scale over much more data and machines to provide better performance. It's important to note that in this specific deployment (local), the difference to use spark vs pure python is it's pretty irrelevant, but in enterprise scenarios with much more data, spark is definitely to be preferred. If Scala was used instead of python to leverage Spark, could have been considered to deploy a spark cluster and distributed the application on it istead of make it run locally https://www.agilelab.it/blog/apache-spark-3-0-development-cluster-single-machine-using-docker; indeed actually, pySpark standalone (no yarn, k8s or mesor) don't support a "cluster" deploy mode unlike Scala.
* **Airflow**: Airflow is a simple and powerfull orchestrator written in python. It's was used to orchestrate the various pipeline, monitor the workflow execution and provide to the end user a nice UI to view logs, execution status and trigger new run.
* **Docker**: Tool used by developers to create, deploy and manged container application. It's was a great choise in order to provide a reproducible, isolated and light enviroment that can be executed on multiple OS.

#### Design/Algorithmic Decisions
- Since the complexty due to Kaggle credentials/login to download the imbd data, the pipeline expect 'movies_metadata.csv' to be already present in the data folder, while the wiki data is download by the pipeline.
- To Execute Spark from Airflow, it's has been decide to choose the SparkSubmitOperator. The reason to use it, was to provide to the user a better management of Spark job in Airflow especially for the deployment. Infact, with SparkSubmitOperator it's possible to easy leverage the classic spark-submit options and easly managed the required resources in term of cpu & memory for the job. A drowback of use this spark operator istead of execute spark from classic functions with the PythonOperator, it's due to not being able to take advantage of Airflow's xcom.
- The parsing of XML files has been performed with a databricks connector present here https://github.com/databricks/spark-xml that which simplified  tremendously the parsing of the xml wiki dataset.
- After the calculating of the ratio between budget and revenue columns, since we require only top 1000 rows, its ideal to join only those 1000 rows from IMDB dataset with the wiki info.


### **5. Unit Test**
* pytest python package has been used for unit testing
* Check on columns and data have been performed to verify if any inconsistent or wrong data have been processed.
* Perfemed test to verify the presence in the final output, of some of the most high profit movies as reported online on https://www.imdb.com
