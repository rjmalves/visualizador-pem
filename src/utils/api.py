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
        url = f"{Settings.result_api}/{identifier}/"
        r = cls.session.get(url)
        if r.status_code != 200:
            return None
        else:
            return r.json()

    @classmethod
    def fetch_available_results_list(
        cls, studies_paths: List[str]
    ) -> List[str]:
        unique_variables = set()
        for p in studies_paths:
            variables = cls.fetch_available_results(p)
            if variables:
                unique_variables = unique_variables.union(set(variables))
        return list(unique_variables)

    @classmethod
    def fetch_result(
        cls, study_path: str, desired_data: str
    ) -> Optional[pd.DataFrame]:
        identifier = base62.encodebytes(study_path.encode("utf-8"))
        url = f"{Settings.result_api}/{identifier}/{desired_data if desired_data else ''}"
        r = cls.session.get(url)
        if r.status_code != 200:
            return None
        else:
            return pd.read_parquet(io.BytesIO(r.content))

    @classmethod
    def fetch_result_list(
        cls, studies_paths: List[str], desired_data: str
    ) -> Optional[pd.DataFrame]:
        valid_dfs: List[pd.DataFrame] = []
        for p in studies_paths:
            path = pathlib.Path(p)
            study = path.parts[-2]
            df = cls.fetch_result(str(path), desired_data)
            if df is not None:
                df_cols = df.columns.to_list()
                df["Estudo"] = study
                df = df[["Estudo"] + df_cols]
                valid_dfs.append(df)
        if len(valid_dfs) > 0:
            complete_df = pd.concat(valid_dfs, ignore_index=True)
            return complete_df
        else:
            return None
