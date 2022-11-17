from typing import Optional, List
import requests
import aiohttp
import asyncio
import pandas as pd
import base62
import io
import pathlib
from src.utils.settings import Settings


class API:

    header_key = {"api-key": Settings.api_key}
    session = requests.Session()
    session.headers.update(header_key)

    @classmethod
    async def fetch_available_results(
        cls, session: aiohttp.ClientSession, study_path: str
    ) -> Optional[List[str]]:
        identifier = base62.encodebytes(study_path.encode("utf-8"))
        url = f"{Settings.result_api}/{identifier}"
        async with session.get(url) as r:
            if r.status != 200:
                return None
            else:
                return await r.json()

    @classmethod
    async def fetch_available_results_list(
        cls, studies_paths: List[str]
    ) -> List[str]:
        async with aiohttp.ClientSession() as session:
            unique_variables = set()
            ret = await asyncio.gather(
                *[
                    cls.fetch_available_results(session, p)
                    for p in studies_paths
                ]
            )
            for variables in ret:
                if variables:
                    unique_variables = unique_variables.union(set(variables))
        return list(unique_variables)

    @classmethod
    async def fetch_result(
        cls,
        session: aiohttp.ClientSession,
        study_path: str,
        desired_data: str,
        filters: dict,
    ) -> Optional[pd.DataFrame]:
        identifier = base62.encodebytes(study_path.encode("utf-8"))
        url = f"{Settings.result_api}/{identifier}/{desired_data}"
        async with session.get(url, params=filters) as r:
            if r.status != 200:
                return None
            else:
                return pd.read_parquet(io.BytesIO(await r.content.read()))

    @classmethod
    async def fetch_result_list(
        cls,
        studies_paths: List[str],
        desired_data: str,
        filters: dict,
        path_part_to_name_study: int,
    ) -> Optional[pd.DataFrame]:
        valid_dfs: List[pd.DataFrame] = []
        async with aiohttp.ClientSession() as session:
            ret = await asyncio.gather(
                *[
                    cls.fetch_result(
                        session, str(pathlib.Path(p)), desired_data, filters
                    )
                    for p in studies_paths
                ]
            )
            for p, df in zip(studies_paths, ret):
                study = pathlib.Path(p).parts[path_part_to_name_study]
                if df is not None:
                    df_cols = df.columns.to_list()
                    df["estudo"] = study
                    df = df[["estudo"] + df_cols]
                    valid_dfs.append(df)
        if len(valid_dfs) > 0:
            complete_df = pd.concat(valid_dfs, ignore_index=True)
            return complete_df
        else:
            return None

    @classmethod
    async def fetch_result_options(
        cls, session: aiohttp.ClientSession, study_path: str, desired_data: str
    ) -> Optional[dict]:
        identifier = base62.encodebytes(study_path.encode("utf-8"))
        url = f"{Settings.result_api}/{identifier}/{desired_data}/options"
        async with session.get(url) as r:
            if r.status != 200:
                return None
            else:
                return await r.json()

    @classmethod
    async def fetch_result_options_list(
        cls, studies_paths: List[str], desired_data: str
    ) -> Optional[dict]:
        valid_opts: List[dict] = []
        async with aiohttp.ClientSession() as session:
            ret = await asyncio.gather(
                *[
                    cls.fetch_result_options(session, str(p), desired_data)
                    for p in studies_paths
                ]
            )
            for opts in ret:
                if opts is not None:
                    valid_opts.append(opts)
        if len(valid_opts) > 0:
            complete_opts = {}
            for o in valid_opts:
                for k, v in o.items():
                    if k not in complete_opts.keys():
                        complete_opts[k] = set(v)
                    else:
                        complete_opts[k].update(v)
            return {k: list(v) for k, v in complete_opts.items()}
        else:
            return None
