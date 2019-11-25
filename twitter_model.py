from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from variables import *



default_args = {
    'owner': 'Airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 11, 25),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG('twitter_model', default_args=default_args, schedule_interval=timedelta(days=1))

build_sentiment_model_job_command = """
cd {{params.git_base_path}}/twitter-sentiment
sbt "runMain com.mateuszjancy.sentiment.twitter.tweets.job.BuildSentimentModelJob --master {{params.master}} --train_data_path {{params.train_data_path}} --model_path {{params.model_path}}"
"""

build_sentiment_model_job = BashOperator(
    task_id='build_sentiment_model_job',
    bash_command=build_sentiment_model_job_command,
    params={'git_base_path': git_base_path, 'master': master, 'new_data_path': new_data_path, 'model_path': model_path, 'train_data_path': train_data_path},
    dag=dag)
