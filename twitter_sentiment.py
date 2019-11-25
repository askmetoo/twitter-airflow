from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from variables import *

default_args = {
    'owner': 'Airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 10, 27),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG('twitter_sentiment', default_args=default_args, schedule_interval=timedelta(days=1))

twitter_dumper_command = """
cd {{params.git_base_path}}/twitter-dumper
sbt "runMain com.mateuszjancy.dumper.twitter.tweets.Boot --api_key {{params.api_key}} --api_secret_key {{params.api_secret_key}} --date {{ds}} --path {{params.path}}"
"""

calculate_sentiment_job_command = """
cd {{params.git_base_path}}/twitter-sentiment
sbt "runMain com.mateuszjancy.sentiment.twitter.tweets.job.CalculateSentimentJob --master {{params.master}} --new_data_path {{params.new_data_path}} --model_path {{params.model_path}} --prediction_data_path {{params.prediction_data_path}}"
"""

tweet_datamart_job_command = """
cd {{params.git_base_path}}/twitter-sentiment
sbt "runMain com.mateuszjancy.sentiment.twitter.tweets.job.TweetDataMartJob --master {{params.master}} --prediction_data_path {{params.prediction_data_path}} --datamart_data_path {{params.datamart_data_path}}"
"""

twitter_dumper = BashOperator(
    task_id='twitter_dumper',
    bash_command=twitter_dumper_command,
    params={'git_base_path': git_base_path, 'api_key': api_key, 'api_secret_key': api_secret_key, 'path': path},
    dag=dag)

calculate_sentiment_job = BashOperator(
    task_id='calculate_sentiment_job',
    bash_command=calculate_sentiment_job_command,
    params={'git_base_path': git_base_path, 'master': master, 'new_data_path': new_data_path, 'model_path': model_path, 'prediction_data_path': prediction_data_path},
    dag=dag)

tweet_datamart_job = BashOperator(
    task_id='tweet_datamart_job',
    bash_command=tweet_datamart_job_command,
    params={'git_base_path': git_base_path, 'master': master, 'datamart_data_path': datamart_data_path, 'prediction_data_path': prediction_data_path},
    dag=dag)

calculate_sentiment_job.set_upstream(twitter_dumper)
tweet_datamart_job.set_upstream(calculate_sentiment_job)
