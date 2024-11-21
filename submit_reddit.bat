@echo off
REM Submit the Spark job to the spark-master container
docker exec sentiment-stream-spark-master-1 spark-submit --master spark://spark-master:7077 --deploy-mode client --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0 /opt/bitnami/spark/jobs/reddit_job.py
