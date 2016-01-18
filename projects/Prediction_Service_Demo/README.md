# Prediction Model Demo
Inspired by Ja Dianes's recommendation engine. 

Decouple the data pipeline with the model. While since the ALS model caculate with all of its data, the model and data is not literally separated as initially planned. Also, sending the spark context to both Pipeline() and PredictionEngine() needs future attention as the application and cluster expand.

(In future)

Add connection to database to make it truly 'online'.

Add some front-end interfaces.

## How to set up

1. ```$ git clone  https://github.com/kevinshenyang07/notes-and-projects/tree/gh-pages/projects/Prediction_Model_Demo```
2. Modify the pipeline.py according to the data you have.
3. Download the pre-built spark at [http://spark.apache.org/downloads.html](http://spark.apache.org/downloads.html) and unzip it to, for example, ```~/spark-1.5.1-bin-hadoop2.6```.
4. To start a standalone cluster, go to the spark folder and start the master node of spark, for example ```$ sbin/start-master.sh```.
5. In the web browser, enter ```http://localhost:8080``` and find its URL formatted as ```spark://localhost:7077```
6. Start the workers with command ``` $ sbin/start-slaves.sh $MASTER_URL```, $MASTER_URL shoule be the URL you found.
7. Start the demo with start_server.sh, remember to configure the cores and RAM you allocate to the executors.
8. You might find 'cherry.error' in the log, the reason is still a mystery, but it works just fine.
