@echo off

for /F "tokens=*" %%A in (.env) do set %%A

REM Submit the Spark job to the spark-master container
docker exec sentiment-stream-spark-master-1 spark-submit --master spark://spark-master:7077 --deploy-mode client --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.4,com.redislabs:spark-redis_2.12:3.1.0 --conf spark.hadoop.fs.s3a.endpoint=http://minio:9000 --conf spark.hadoop.fs.s3a.access.key=%MINIO_ACCESS_KEY% --conf spark.hadoop.fs.s3a.secret.key=%MINIO_SECRET_KEY% --conf spark.hadoop.fs.s3a.path.style.access=true --conf spark.executor.cores=1 --conf spark.executor.instances=1 --total-executor-cores=1 /opt/bitnami/spark/jobs/reddit_job.py