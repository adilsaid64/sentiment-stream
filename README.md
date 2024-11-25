# sentiment-stream
An end-to-end real-time data streaming pipeline that leverages Kafka and Spark Streaming to analyze social media sentiment trends. 

Project still in progress...

![alt text](images/architecture.png)

## Architecture

1. **Data Sources**:
   - Twitter and Reddit are the data sources. But more can be added. 

2. **Stream Data Ingestion**:
   - **Apache Kafka** is used to handle incoming data streams. Each source gets sent to its respective topic  (`twitter-topic` and `reddit-topic`).
   - **Apache ZooKeeper** manages Kafka brokers.

3. **Stream Processing**:
   - **Apache Spark** processes the streaming data using Spark Structured Streaming.
   - Processed data is stored in:
     - **Object Storage** for long-term persistence.
     - **Redis** for short-term persistence.


4. **Real-Time Dashboard**:
   - **Redis** serves as a short-term cache for fast data retrieval.
   - **Flask** handles backend operations for the dashboard.
   - Frontend is in **HTML**, **CSS**, and **JavaScript**.

5. **End Users**:
   - Users access the dashboard via a web interface served by **Nginx**.


## To Run
   - Ensure Docker is installed and running.
   - Run `docker-compose up --build` file.