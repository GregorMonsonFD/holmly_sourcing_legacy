from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from scripts.rightmove_scrape import get_for_sale_properties
import datetime

#https://www.youtube.com/watch?v=IsWfoXY_Duk

args = {
    'owner': 'Gregor Monson',
    'start_date': days_ago(1) # make start date in the past
}

dag = DAG(
    dag_id='rightmove-scrape-edinburgh',
    default_args=args,
    schedule_interval='0 0 * * *', # make this workflow happen every day
)

with dag:
    rightmove_edinburgh_to_csv = PythonOperator(
        task_id='rightmove_edinburgh_to_csv',
        provide_context=True,
        python_callable=get_for_sale_properties,
        execution_timeout=datetime.timedelta(seconds=300),
        op_kwargs={'borough': '5E475'},
        retries=2,
    )