from typing import Optional, List
import requests
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
    def fetch_available_results(cls, study_path: str) -> Optional[List[str]]:
        identifier = base62.encodebytes(study_path.encode("utf-8"))
        url = f"{Settings.result_api}/{identifier}"
        with requests.get(url) as r:
            if r.status_code != 200:
                return None
            else:
                return r.json()

    @classmethod
    def fetch_available_results_list(
        cls, studies_paths: List[str]
    ) -> List[str]:
        unique_variables = set()
        ret = [cls.fetch_available_results(p) for p in studies_paths]
        for variables in ret:
            if variables:
                unique_variables = unique_variables.union(set(variables))
        return list(unique_variables)

    @classmethod
    def fetch_result(
        cls,
        study_path: str,
        desired_data: str,
        filters: dict,
    ) -> Optional[pd.DataFrame]:
        identifier = base62.encodebytes(study_path.encode("utf-8"))
        url = f"{Settings.result_api}/{identifier}/{desired_data}"
        with requests.get(url, params=filters) as r:
            if r.status_code != 200:
                return None
            else:
                return pd.read_parquet(io.BytesIO(r.content))

    @classmethod
    def fetch_result_list(
        cls,
        studies_paths: List[str],
        studies_labels: List[str],
        desired_data: str,
        filters: dict,
    ) -> Optional[pd.DataFrame]:
        valid_dfs: List[pd.DataFrame] = []
        ret = [
            cls.fetch_result(str(pathlib.Path(p)), desired_data, filters)
            for p in studies_paths
        ]

        for study, df in zip(studies_labels, ret):
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
    def fetch_result_options(
        cls, study_path: str, desired_data: str
    ) -> Optional[dict]:
        identifier = base62.encodebytes(study_path.encode("utf-8"))
        url = f"{Settings.result_api}/{identifier}/{desired_data}/options"
        with requests.get(url) as r:
            if r.status_code != 200:
                return None
            else:
                return r.json()

    @classmethod
    def fetch_result_options_list(
        cls, studies_paths: List[str], desired_data: str
    ) -> Optional[dict]:
        valid_opts: List[dict] = []
        ret = [
            cls.fetch_result_options(str(p), desired_data)
            for p in studies_paths
        ]
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
