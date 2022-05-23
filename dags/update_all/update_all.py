from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash_operator import BashOperator

args = {
    'owner': 'Gregor Monson',
    'start_date': days_ago(0),
    'yesterday': days_ago(1), # make start date in the past
}

dag = DAG(
        dag_id='update_all_scripts',
        default_args=args,
        schedule_interval=None, # make this workflow happen every day
    )

with dag:
    bash_task = BashOperator(
        task_id='run_make_file',
        bash_command='cd /home/eggzo/airflow/; make update;'
    )