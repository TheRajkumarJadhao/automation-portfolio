#!/bin/bash
# Initialize the Airflow database
airflow db init

# Create the default admin user
airflow users create \
  --username admin \
  --firstname raj \
  --lastname jadhao \
  --role Admin \
  --email jadhav.raj321@gmail.com \
  --password admin
