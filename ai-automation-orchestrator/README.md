# AI Automation Orchestrator

## Project overview
A production-grade automation orchestration platform that combines Apache Airflow, Playwright, Robot Framework, and Python ETL to run daily end-to-end workflows targeting `https://maharera.maharashtra.gov.in/`.

This repo includes modular scripts and an Airflow DAG to orchestrate web automation and data processing with reusable components and reliable logging.

## Architecture (text diagram)
```
            +-------------------+
            |   Airflow DAG     |
            | automation_pipeline|
            +---------+---------+
                      |
         +------------+-------------+
         |            |             |
+--------v--------+ +--v-----------+ +---------v-------+
| Robot Framework | | Playwright   | | Python ETL      |
| login_test.robot| | scraper.py   | | etl_job.py      |
+-----------------+ +--------------+ +-----------------+
         |                                            |
         +-----------------+  +-----------------------+
                           |  |
                       +---v--v---+
                       |   data   |
                       |  outputs |---> logs/orchestrator.log
                       +----------+
```

## Tech stack
- Apache Airflow 2.10.2
- Playwright 1.46.0
- Robot Framework 6.0.1 + SeleniumLibrary
- Python 3.12+
- Docker Compose
- Pandas
- PyYAML

## Features
- daily scheduled orchestration (robot, playwright, etl)
- robust retry logic via Airflow
- centralized logging to console and rotating file
- modular code structure (utils, automation, dags)
- environment-configurable via `config/config.yaml`
- Docker-ready for portable deployment

## Setup instructions
1. Clone repository
   ```bash
git clone <repo> ; cd ai-automation-orchestrator
```
2. Install dependencies
   ```bash
python -m venv .venv;
.\.venv\Scriptsctivate
pip install -r requirements.txt
python -m playwright install
```
3. Update `config/config.yaml` as needed.
4. Ensure a functional Chrome/Chromium and chromedriver; or rely on Docker.

## Docker Compose setup
```bash
docker compose up -d
```

## How to run Airflow
### Using Docker Compose
- start Airflow
  ```bash
docker compose up -d
```
- check status
  ```bash
docker compose ps
docker compose logs -f airflow
```
- navigate to `http://localhost:8080`
- verify DAG `automation_pipeline` exists and trigger manually if required.

### Local mode (option)
```bash
airflow db init
airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com
airflow webserver --port 8080
airflow scheduler
```

## Running components manually
- Robot test
  ```bash
python -m robot --outputdir logs/robot_results automation/robot/login_test.robot
```
- Playwright scraper
  ```bash
python automation/playwright/scraper.py
```
- ETL job
  ```bash
python automation/python/etl_job.py
```
- all-in-one script
  ```bash
./run_all.ps1
```

## Example use cases
1. Scheduled status check and data capture of MahaRERA site for compliance.
2. Automated nightly refresh of web links and ETL pipeline for reporting.
3. RPA-driven UI validation via Robot Framework as part of broken-build detection.

## Screenshots
Add after first successful run:
- Airflow DAG view (automation_pipeline)
- task instance logs in Airflow
- `data/output/etl_output.csv` preview
- `logs/orchestrator.log` snippet

## Notes
- Adjust retries in `config/config.yaml`.
- For production, set `environment.mode: prod` and configure Airflow backend/fernet keys.
- Use `docker compose down` to stop the stack.
