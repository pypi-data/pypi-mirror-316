from pathlib import Path
import pandas as pd
import polars as pl
from concurrent.futures import ThreadPoolExecutor
import trino
import os
from rich import print
from rich.progress import (
    BarColumn,
    Progress,
    TextColumn,
    SpinnerColumn
)
from datetime import datetime


class DataPipeLine:
    def __init__(
            self,
            query: str,
            count_rows: bool = False,
    ):
        self.query = f"SELECT COUNT(*) FROM ({query})" if count_rows else query
        self.count_rows = count_rows
        self.status = '[bright_blue]🤖 JDBC[/bright_blue]'

    def debug_query(self):
        print(self.query)

    def _records_to_df(self, records, columns: list, save_path: Path):
        # records to df
        try:
            df = pl.DataFrame(records, orient='row', schema=columns)
        except (pl.exceptions.ComputeError, TypeError) as e:
            print(f'{self.status} Errors on Polars, switch to Pandas: {e}')
            df = pd.DataFrame(records, columns=columns)

        # write
        if save_path:
            save_path.parent.mkdir(parents=True, exist_ok=True)
            if isinstance(df, pl.DataFrame):
                df.write_parquet(save_path)
            else:
                df.to_parquet(save_path, index=False, compression='zstd')

        # message
        message = f"Data shape ({df.shape[0]:,.0f}, {df.shape[1]})"
        return message, df

    def _connection(self):
        username, password = os.environ['PRESTO_USER'], os.environ['PRESTO_PASSWORD']
        conn = trino.dbapi.connect(
            host='presto-secure.data-infra.shopee.io',
            port=443,
            user=username,
            catalog='hive',
            http_scheme='https',
            source=f'(50)-(vnbi-dev)-({username})-(jdbc)-({username})-(SG)',
            auth=trino.auth.BasicAuthentication(username, password)
        )
        return conn

    def _progress(self):
        query_progress = Progress(
            TextColumn("{task.description}"),
            SpinnerColumn("simpleDots"),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            BarColumn(),
            transient=True
        )

        fetch_progress = Progress(
            TextColumn("{task.description}"),
            SpinnerColumn("simpleDots"),
            transient=True
        )

        return query_progress, fetch_progress

    def run_presto_to_df(
            self,
            save_path: Path = None,
            file_name: str = '',
    ):
        # connection
        conn = self._connection()
        cur = conn.cursor()

        # verbose
        query_progress, fetch_progress = self._progress()
        thread = ThreadPoolExecutor(1)

        # run
        async_result = thread.submit(cur.execute, self.query)
        task_id_query = query_progress.add_task("[cyan]Presto to Local", total=100)
        time_ = f'[orange1]{datetime.now().strftime('%H:%M:%S')}[/]'
        print(f"{time_} {self.status} [bold green]QUERY[/]: file name [{file_name}], Count rows: [{self.count_rows}]")
        # query
        memory = 0
        with query_progress:
            while not async_result.done():
                try:
                    memory = cur.stats.get('peakMemoryBytes', 0) * 10 ** -9
                    perc = 0
                    stt = cur.stats.get('state', 'Not Ready')
                    if stt == "RUNNING":
                        perc = round((cur.stats.get('completedSplits', 1e-3) * 100.0) / (cur.stats.get('totalSplits', 0)), 2)
                    status = f"{stt} - Memory {memory:,.0f}GB"
                    query_progress.update(task_id_query, description=status, advance=perc)
                except ZeroDivisionError as e:
                    continue

        time_ = f'[orange1]{datetime.now().strftime('%H:%M:%S')}[/]'
        print(f"{time_} {self.status} [bold green]FETCHING...[/] ")
        try:
            # fetch
            records = cur.fetchall()
            # result
            columns = [i[0] for i in cur.description]
            text, df = self._records_to_df(records, columns, save_path)
            # update status
            time_ = f'[orange1]{datetime.now().strftime('%H:%M:%S')}[/]'
            print(f"{time_} {self.status} [bold green]DONE:[/] Memory {memory:,.0f}GB, {text}")
            return df
        except AssertionError as e:
            print(e)

    def _run_presto(
            self,
            save_path: Path = None,
            file_name: str = '',
    ):
        # connection
        conn = self._connection()
        cur = conn.cursor()

        # run
        time_ = f'[orange1]{datetime.now().strftime('%H:%M:%S')}[/]'
        print(f"{time_} {self.status} [bold green]QUERY[/]: file name [{file_name}], Count rows: [{self.count_rows}]")
        cur.execute(self.query)

        time_ = f'[orange1]{datetime.now().strftime('%H:%M:%S')}[/]'
        print(f"{time_} {self.status} [bold green]FETCHING...[/] ")
        try:
            # fetch
            records = cur.fetchall()
            # result
            columns = [i[0] for i in cur.description]
            text, df = self._records_to_df(records, columns, save_path)
            # update status
            time_ = f'[orange1]{datetime.now().strftime('%H:%M:%S')}[/]'
            print(f"{time_} {self.status} [bold green]DONE:[/] {text}")
            return df
        except AssertionError as e:
            print(e)


# def spawn(query: str, path: Path, file_name: str):
#     file_path = path / f'data_daily/{file_name}.ftr'
#
#     if not file_path.exists():
#         df = DataPipeLine(query)._run_presto(save_path=path)
#
#
# yesterday = (pd.to_datetime('today') - pd.Timedelta(1, unit='D')).date().isoformat()
# dates = pd.date_range(start='2022-08-01', end='2023-02-28', freq='10D')
# # dates = pd.date_range(start='2022-08-01', end=yesterday, freq='10D')
# shift = (dates + pd.Timedelta(9, unit='D')).date.tolist()
# dates = dates.date.tolist()
# run = list(zip(dates, shift))
#
# # spawn(run)
# # run = pd.date_range(start='2023-0-01', end=yesterday).date.tolist()
# with ThreadPoolExecutor(4) as executor:
#     executor.map(spawn, run)


# def pipe_thread(query):
#     DataPipeLine(query)._run_presto()