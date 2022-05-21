from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.sftp.operators.sftp import SFTPOperator
from airflow.operators.mysql_operator import MySqlOperator
from airflow.utils.dates import days_ago
from scripts.python.rightmove_scrape import get_for_sale_properties
import datetime

args = {
    'owner': 'Gregor Monson',
    'location': 'Edinburgh',
    'start_date': days_ago(0),
    'yesterday': days_ago(1), # make start date in the past
    'borough_code': '{{ var.value.edinburgh_id }}'
}


def mysql_group(name, **kwargs):
    return MySqlOperator(
        task_id='sql_{}'.format(name[:-4]),
        sql=name,
        mysql_conn_id="mysql_warehouse",
        retries=3,
        dag=dag)

dag = DAG(
    dag_id='rightmove-edinburgh',
    default_args=args,
    schedule_interval='0 0 * * *', # make this workflow happen every day
    template_searchpath=['/home/eggzo/airflow/scripts/sql/edi'],
)

with dag:
    SQL_files = (
    [
        'csv_to_landing_area_edi.sql',
        'create_tables_edi.sql',
        'insert_ids_edi.sql',
        'price_conversion_edi.sql',
        'updating_static_fields.sql',
        'address_extraction_edi.sql'
    ]
    )

    rightmove_edinburgh_to_csv = PythonOperator(
        task_id='rightmove_edinburgh_to_csv',
        provide_context=True,
        python_callable=get_for_sale_properties,
        execution_timeout=datetime.timedelta(seconds=300),
        op_kwargs={'borough': '{{ var.value.edinburgh_id }}'},
        retries=2,
        dag=dag,
    )

    sftp_upload_edinburgh_to_db = SFTPOperator(
        task_id="sftp_pi_to_warehouse",
        ssh_conn_id="sftp_default",
        local_filepath="/home/eggzo/airflow/tmp_data/sales_data_{{ var.value.edinburgh_id }}_{{ ds }}.csv",
        remote_filepath="/var/lib/mysql-files/sales_data_{{ var.value.edinburgh_id }}_{{ ds }}.csv",
        operation="put",
        create_intermediate_dirs=True,
        retries=3,
        dag=dag
    )

    rightmove_edinburgh_to_csv >> sftp_upload_edinburgh_to_db

    sftp_upload_edinburgh_to_db >> mysql_group(SQL_files[0]) >> mysql_group(SQL_files[1]) >> mysql_group(SQL_files[2])

    for i in range(3, 6):
        mysql_group(SQL_files[2]) >> mysql_group(SQL_files[i])