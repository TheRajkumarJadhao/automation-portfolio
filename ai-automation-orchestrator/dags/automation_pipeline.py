"""Airflow DAG for automation orchestration."""

import logging
import pendulum
import os
import subprocess
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ROBOT_SCRIPT = os.path.join(BASE_DIR, 'automation', 'robot', 'login_test.robot')
PLAYWRIGHT_SCRIPT = os.path.join(BASE_DIR, 'automation', 'playwright', 'scraper.py')
ETL_SCRIPT = os.path.join(BASE_DIR, 'automation', 'python', 'etl_job.py')

logger = logging.getLogger('automation_pipeline')
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': False,
    'email_on_retry': False,
}

def run_robot_task(**kwargs):
    logger.info('Starting Robot Framework task: %s', ROBOT_SCRIPT)
    if not os.path.exists(ROBOT_SCRIPT):
        raise FileNotFoundError(f'Robot file not found: {ROBOT_SCRIPT}')

    output_dir = os.path.join(BASE_DIR, 'logs', 'robot')
    os.makedirs(output_dir, exist_ok=True)

    command = ['robot', '--outputdir', output_dir, ROBOT_SCRIPT]
    result = subprocess.run(command, capture_output=True, text=True)

    logger.info('Robot stdout:\n%s', result.stdout)
    logger.info('Robot stderr:\n%s', result.stderr)

    if result.returncode != 0:
        logger.error('Robot task failed with return code %s', result.returncode)
        raise RuntimeError(f'Robot Framework execution failed (code={result.returncode})')

    logger.info('Robot Framework task completed successfully')

def run_playwright_task(**kwargs):
    logger.info('Starting Playwright task: %s', PLAYWRIGHT_SCRIPT)
    if not os.path.exists(PLAYWRIGHT_SCRIPT):
        raise FileNotFoundError(f'Playwright script not found: {PLAYWRIGHT_SCRIPT}')

    command = ['python', PLAYWRIGHT_SCRIPT]
    result = subprocess.run(command, capture_output=True, text=True)

    logger.info('Playwright stdout:\n%s', result.stdout)
    logger.info('Playwright stderr:\n%s', result.stderr)

    if result.returncode != 0:
        logger.error('Playwright task failed with return code %s', result.returncode)
        raise RuntimeError(f'Playwright script execution failed (code={result.returncode})')

    logger.info('Playwright task completed successfully')

def run_etl_task(**kwargs):
    logger.info('Starting ETL task: %s', ETL_SCRIPT)
    if not os.path.exists(ETL_SCRIPT):
        raise FileNotFoundError(f'ETL script not found: {ETL_SCRIPT}')

    command = ['python', ETL_SCRIPT]
    result = subprocess.run(command, capture_output=True, text=True)

    logger.info('ETL stdout:\n%s', result.stdout)
    logger.info('ETL stderr:\n%s', result.stderr)

    if result.returncode != 0:
        logger.error('ETL task failed with return code %s', result.returncode)
        raise RuntimeError(f'ETL script execution failed (code={result.returncode})')

    logger.info('ETL task completed successfully')

with DAG(
    dag_id='automation_pipeline',
    default_args=default_args,
    description='Orchestrate Robot, Playwright, and ETL tasks daily',
    schedule_interval='@daily',
    start_date=datetime(2026, 3, 31, tz="UTC"),
    catchup=False,
    max_active_runs=1,
    tags=['automation', 'orchestration'],
) as dag:

    robot_task = PythonOperator(
        task_id='run_robot_task',
        python_callable=run_robot_task,
    )

    playwright_task = PythonOperator(
        task_id='run_playwright_task',
        python_callable=run_playwright_task,
    )

    etl_task = PythonOperator(
        task_id='run_etl_task',
        python_callable=run_etl_task,
    )

    robot_task >> playwright_task >> etl_task
