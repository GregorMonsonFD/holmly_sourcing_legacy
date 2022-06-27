from airflow.models import DAG
from airflow.contrib.operators.ssh_operator import SSHOperator
from airflow.operators.python_operator import PythonOperator
from airflow.providers.sftp.operators.sftp import SFTPOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.mysql_operator import MySqlOperator
from airflow.utils.dates import days_ago
from scripts.python.rightmove_scrape import get_for_sale_properties
import datetime, os, yaml

args = {
    'owner': 'Gregor Monson',
    'start_date': days_ago(0),
    'yesterday': days_ago(1), # make start date in the past
}

LOCAL_PATH = os.path.dirname(__file__)

dag = DAG(
        dag_id='find_listing_area',
        default_args=args,
        schedule_interval='0 0 * * *',
        template_searchpath=['/home/eggzo/airflow/scripts/sql/floorplan'],# make this workflow happen every day
    )

with dag: