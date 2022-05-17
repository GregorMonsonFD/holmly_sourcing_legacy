from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.sftp.operators.sftp import SFTPOperator
from airflow.utils.dates import days_ago
from scripts.rightmove_scrape import get_for_sale_properties
import datetime

#https://www.youtube.com/watch?v=IsWfoXY_Duk

args = {
    'owner': 'Gregor Monson',
    'start_date': days_ago(0), # make start date in the past
    'yesterday': days_ago(1),
    'borough_code': '5E475'
}

dag = DAG(
    dag_id='rightmove-edinburgh',
    default_args=args,
    schedule_interval='0 0 * * *', # make this workflow happen every day
)

with dag:
    rightmove_edinburgh_to_csv = PythonOperator(
        task_id='rightmove_edinburgh_to_csv',
        provide_context=True,
        python_callable=get_for_sale_properties,
        execution_timeout=datetime.timedelta(seconds=300),
        op_kwargs={'borough': '{{ borough_code }}'},
        retries=2,
    )

    ftp_upload_edinburgh_to_db = SFTPOperator(
        task_id="sftp_pi_to_warehouse",
        ssh_conn_id="ssh_default",
        local_filepath="/home/eggzo/tmp_data/sales_data_{{ borough_code }}_{{ start_date }}.csv",
        remote_filepath="/var/lib/mysql-files/sales_data_{{ borough_code }}_{{ start_date }}.csv",
        operation="put",
        create_intermediate_dirs=True,
        dag=dag
    )

    rightmove_edinburgh_to_csv >> ftp_upload_edinburgh_to_db