import logging
from pathlib import Path
from typing import Optional

import pandas as pd

from utils.logger import get_logger

logger = get_logger('etl_job')


def create_sample_data() -> pd.DataFrame:
    """Create a sample dataset mimicking MahaRERA links payload."""
    df = pd.DataFrame([
        {'project': 'Project A', 'value': 100, 'region': 'Mumbai'},
        {'project': 'Project B', 'value': 150, 'region': 'Pune'},
        {'project': 'Project C', 'value': 120, 'region': 'Nagpur'},
    ])
    logger.info('Sample dataset created with %d rows', len(df))
    return df


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Add derived fields and clean data."""
    if df.empty:
        logger.warning('Transformation called with empty dataframe')
        return df

    df = df.copy()
    df['value_with_tax'] = (df['value'] * 1.18).round(2)
    df['region'] = df['region'].str.title()
    logger.info('Transformation applied (value_with_tax and region cleanup)')
    return df


def save_to_csv(df: pd.DataFrame, output_path: str) -> str:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding='utf-8')
    logger.info('Saved transformed data to %s', output_path)
    return str(path)


def run_etl(
    input_csv: Optional[str] = None,
    output_csv: str = 'data/output/etl_output.csv',
    from_sample: bool = False,
) -> str:
    try:
        if from_sample or input_csv is None:
            df = create_sample_data()
        else:
            path = Path(input_csv)
            if not path.exists():
                raise FileNotFoundError(f'Input file not found: {input_csv}')
            df = pd.read_csv(path)
            logger.info('Read input csv from %s: %d rows', input_csv, len(df))

        transformed = transform_data(df)
        output_path = save_to_csv(transformed, output_csv)
        logger.info('ETL pipeline completed successfully')
        return output_path
    except Exception as e:
        logger.exception('ETL pipeline failed: %s', e)
        raise


if __name__ == '__main__':
    run_etl(from_sample=True)
