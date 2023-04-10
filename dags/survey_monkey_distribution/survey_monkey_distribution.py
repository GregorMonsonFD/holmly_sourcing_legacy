from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.models import Variable
from airflow.utils.dates import days_ago
from scripts.python.survey_monkey_distribute_daily import survey_monkey_distribute_daily
import datetime, os, yaml

args = {
    'owner': 'Gregor Monson',
    'start_date': days_ago(1),
    'yesterday': days_ago(2), # make start date in the past
}

LOCAL_PATH = os.path.dirname(__file__)

dag = DAG(
        dag_id='survey_monkey_distribution',
        default_args=args,
        schedule_interval='0 6 * * *',
        template_searchpath=['/home/eggzo/airflow/scripts/sql/report_content'],# make this workflow happen every day
    )

with dag:
    report_generation_task_sensor = ExternalTaskSensor(
        task_id='report_generation_task_sensor',
        poke_interval=60,
        timeout=600,
        soft_fail=False,
        retries=2,
        external_task_id='common_end_report_generation',
        external_dag_id='report_generate_daily',
        execution_delta=datetime.timedelta(hours=6),
        dag=dag
    )

    survey_monkey_distribute_daily = PythonOperator(
        task_id='survey_monkey_distribute_daily',
        provide_context=True,
        python_callable=survey_monkey_distribute_daily,
        op_kwargs={'api_key': Variable.get('survey_monkey_api_key'), 'server' : Variable.get('survey_monkey_server')},
        execution_timeout=datetime.timedelta(hours=1),
        retries=1,
    )

    report_generation_task_sensor >> survey_monkey_distribute_daily

