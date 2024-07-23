from typing import Optional, List, Dict
import requests
import pandas as pd
import base62
import io
import pathlib
from src.utils.settings import Settings
import src.utils.constants as constants


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
                if r.headers["Content-Type"] == "application/json":
                    return r.json()
                else:
                    return None

    @classmethod
    def fetch_available_results_list(
        cls, studies_paths: List[str]
    ) -> Dict[str, List[str]]:
        ret = {p: cls.fetch_available_results(p) for p in studies_paths}
        metadata_names = constants.SYNTHESIS_METADATA_NAMES
        available_variables: Dict[str, pd.DataFrame] = {
            cat: [pd.DataFrame()] for cat in metadata_names.keys()
        }
        for p, results in ret.items():
            if results is None:
                continue
            for cat, metadata_file in metadata_names.items():
                if metadata_file in results:
                    metadata = cls.fetch_result(
                        p, metadata_file, {"preprocess": "FULL"}
                    )
                    metadata["estudo"] = p
                    if metadata is not None:
                        available_variables[cat].append(metadata)
        for cat in available_variables.keys():
            available_variables[cat] = pd.concat(
                available_variables[cat], ignore_index=True
            )
            available_variables[cat] = (
                available_variables[cat]
                .drop_duplicates(subset=["chave", "estudo"], ignore_index=True)
                .to_json(orient="split")
            )
        return available_variables

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
                try:
                    df = pd.read_parquet(io.BytesIO(r.content))
                except Exception:
                    return None
                return df

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
    def fetch_study_SBM_spatial_variable_list(
        cls,
        study_path: str,
        desired_variables: List[str],
        filters: dict,
    ) -> Optional[pd.DataFrame]:
        ret = {
            v: cls.fetch_result(str(pathlib.Path(study_path)), v, filters)
            for v in desired_variables
        }
        df_agg = {
            "NEWAVE": constants.SUBMERCADOS_NEWAVE.copy(),
            "DECOMP": constants.SUBMERCADOS_DECOMP.copy(),
        }.get(filters["programa"])
        if df_agg is None:
            return None
        df_agg = df_agg.set_index("nome")

        for v, df in ret.items():
            if df is not None:
                df["submercado"] = df.apply(
                    lambda linha: constants.MAPA_NOMES_SUBMERCADOS.get(
                        linha["submercado"], linha["submercado"]
                    ),
                    axis=1,
                )
                df_agg.loc[df["submercado"], v.split("_")[0]] = df[
                    "valor"
                ].to_numpy()
        df_ret = df_agg.fillna(0.0).reset_index().set_index("submercado")
        return df_ret

    @classmethod
    def fetch_study_INT_spatial_variable_list(
        cls,
        study_path: str,
        filters: dict,
    ) -> Optional[pd.DataFrame]:
        df = cls.fetch_result(
            str(pathlib.Path(study_path)), "INT_SBP_EST", filters
        )
        if df is None:
            return None
        filters["programa"]
        df_agg = {
            "NEWAVE": constants.INTERCAMBIOS_SUBMERCADOS_NEWAVE.copy(),
            "DECOMP": constants.INTERCAMBIOS_SUBMERCADOS_DECOMP.copy(),
        }.get(filters["programa"])
        if df_agg is None:
            return None

        for c in ["submercadoDe", "submercadoPara"]:
            df[c] = df.apply(
                lambda linha: constants.MAPA_NOMES_SUBMERCADOS.get(
                    linha[c], linha[c]
                ),
                axis=1,
            )

        valores = []
        for _, linha in df_agg.iterrows():
            interc_direto = df.loc[
                (df["submercadoDe"] == linha["source"])
                & (df["submercadoPara"] == linha["target"]),
                "valor",
            ]
            interc_direto = (
                interc_direto.iloc[0] if not interc_direto.empty else 0.0
            )
            interc_inverso = df.loc[
                (df["submercadoDe"] == linha["target"])
                & (df["submercadoPara"] == linha["source"]),
                "valor",
            ]
            interc_inverso = (
                interc_inverso.iloc[0] if not interc_inverso.empty else 0.0
            )
            valores.append(interc_direto - interc_inverso)
        df_agg["valor"] = valores
        return df_agg.fillna(0.0)

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

    @classmethod
    def fetch_spatial_options_list(cls, path: str) -> Optional[dict]:
        ret = cls.fetch_result_options(str(path), "EARPF_SBM_EST")
        if ret:
            complete_opts = {}
            for k, v in ret.items():
                if k not in complete_opts.keys():
                    complete_opts[k] = set(v)
                else:
                    complete_opts[k].update(v)
            return {k: list(v) for k, v in complete_opts.items()}
        else:
            return None
