from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.sftp.operators.sftp import SFTPOperator
from airflow.operators.mysql_operator import MySqlOperator
from airflow.utils.dates import days_ago
from scripts.rightmove_scrape import get_for_sale_properties
import datetime

args = {
    'owner': 'Gregor Monson',
    'start_date': days_ago(0),
    'yesterday': days_ago(1), # make start date in the past
    'borough_code': '{{ var.value.edinburgh_id }}'
}

dag = DAG(
    dag_id='rightmove-edinburgh',
    default_args=args,
    schedule_interval='0 0 * * *', # make this workflow happen every day
)

with dag:
    make_staging_table = (
""" 
DROP TABLE IF EXISTS landing.edinburgh{{ ds_nodash }}; 
CREATE TABLE landing.edinburgh{{ ds_nodash }}
(
ID bigint not null, 
address varchar(128) not null, 
number_of_beds smallint null, 
links varchar(256) not null, 
description varchar(128) not null, 
price varchar(64) not null 
);
"""
)

    import_csv = (
"""
LOAD DATA INFILE '/var/lib/mysql-files/sales_data_{{ var.value.edinburgh_id }}_{{ ds }}.csv' 
INTO TABLE landing.edinburgh{{ ds_nodash }} 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS; 
"""
)

    make_staging_table = make_staging_table.replace("\n", "")
    import_csv = import_csv.replace("\n", "")

    rightmove_edinburgh_to_csv = PythonOperator(
        task_id='rightmove_edinburgh_to_csv',
        provide_context=True,
        python_callable=get_for_sale_properties,
        execution_timeout=datetime.timedelta(seconds=300),
        op_kwargs={'borough': '{{ var.value.edinburgh_id }}'},
        retries=2,
        dag=dag,
    )

    ftp_upload_edinburgh_to_db = SFTPOperator(
        task_id="sftp_pi_to_warehouse",
        ssh_conn_id="sftp_default",
        local_filepath="/home/eggzo/airflow/tmp_data/sales_data_{{ var.value.edinburgh_id }}_{{ ds }}.csv",
        remote_filepath="/var/lib/mysql-files/sales_data_{{ var.value.edinburgh_id }}_{{ ds }}.csv",
        operation="put",
        create_intermediate_dirs=True,
        retries=3,
        dag=dag
    )

    create_staging_table = MySqlOperator(
        sql=make_staging_table,
        task_id="create_staging_table_edinburgh",
        mysql_conn_id="mysql_warehouse",
        retries=3,
        dag=dag
    )

    import_csv = MySqlOperator(
        sql=import_csv,
        task_id="import_csv_edinburgh",
        mysql_conn_id="mysql_warehouse",
        retries=3,
        dag=dag
    )

    rightmove_edinburgh_to_csv >> ftp_upload_edinburgh_to_db >> create_staging_table
    create_staging_table >> import_csv