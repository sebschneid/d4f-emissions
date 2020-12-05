import json
import pathlib
from typing import Dict

import pandas as pd  # type: ignore
import plotly  # type: ignore


class App:
    df_country_and_continent_codes: pd.DataFrame
    df_emissions_cum: pd.DataFrame
    code_to_continent: Dict[str, str]

    def __init__(
        self,
        df_country_and_continent_codes: pd.DataFrame,
        df_emissions_cum: pd.DataFrame,
        code_to_continent: Dict[str, str],
    ):
        self.df_country_and_continent_codes = df_country_and_continent_codes
        self.df_emissions_cum = df_emissions_cum
        self.code_to_continent = code_to_continent

    @staticmethod
    def preprocess_cum_emissions(df: pd.DataFrame) -> pd.DataFrame:
        # rename columns
        df.columns = [
            "entity",
            "code",
            "year",
            "cumulative_emissions",
        ]

        # filter world and NaN entries
        df = df[(~df["code"].isna()) & (df.entity != "World")]

        df = df.rename(columns={"entity": "country"})

        return df

    @classmethod
    def create_from_config(cls, config_filepath: pathlib.Path):
        with open(config_filepath) as config_file:
            config = json.load(config_file)

        DATAPATH = pathlib.Path(config["DATAPATH"])

        # emissions data
        df_emissions_cum = pd.read_csv(
            DATAPATH / "emissions/co2-cumulative.csv"
        )
        df_emissions_cum = cls.preprocess_cum_emissions(df_emissions_cum)

        # country codes
        df_country_and_continent_codes = pd.read_csv(
            DATAPATH / "country_codes/country-and-continent-codes-list.csv"
        )
        code_to_continent = {
            code: continent
            for _, (code, continent) in df_country_and_continent_codes[
                ["Three_Letter_Country_Code", "Continent_Name"]
            ]
            .dropna()
            .iterrows()
        }

        # add continent to df
        df_emissions_cum["continent"] = df_emissions_cum["code"].map(
            code_to_continent
        )
        df_emissions_cum = df_emissions_cum[
            ~df_emissions_cum["continent"].isna()
        ]

        return cls(
            df_country_and_continent_codes=df_country_and_continent_codes,
            df_emissions_cum=df_emissions_cum,
            code_to_continent=code_to_continent,
        )

    def plot_cumulative_sunburst(
        self, year: int
    ) -> plotly.graph_objects.Figure:
        df_year = self.df_emissions_cum.query(f"year=={year}")
        fig = plotly.express.sunburst(
            df_year,
            path=["continent", "country"],
            values="cumulative_emissions",
        )
        return fig

    def plot_cumulative_treemap(self, year: int) -> plotly.graph_objects.Figure:
        df_year = self.df_emissions_cum.query(f"year=={year}")
        fig = plotly.express.treemap(
            df_year,
            path=["continent", "country"],
            values="cumulative_emissions",
        )
        return fig
