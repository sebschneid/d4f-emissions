import sys
import pathlib

import pandas as pd

DATADIR = pathlib.Path(__file__).parent.parent / "data"
EMISSIONS_DIR = "OWID_co2-and-other-ghg-emissions"
CUMULATIVE_EMISSIONS_FILE = "cumulative-co-emissions.csv"

country_codes_german = pd.read_csv(
    DATADIR / "country_codes_german.csv", header=None
)
country_and_continent_codes = pd.read_csv(
    DATADIR / "country-and-continent-codes-list.csv"
)
df_cumulative_emissions = pd.read_csv(
    DATADIR / EMISSIONS_DIR / CUMULATIVE_EMISSIONS_FILE
)
df_cumulative_emissions.columns = [
    "entity",
    "code",
    "year",
    "cumulative_emissions",
]


df_co2_cumulative_countries = df_cumulative_emissions[
    (~df_cumulative_emissions["code"].isna())
    & (df_cumulative_emissions.entity != "World")
]
# df_co2_cumulative_with_population = df_cumulative_emissions.set_index(
#     ["code", "year"]
# ).join(
#     df_co2_gdp[["population", "code", "year"]].set_index(["code", "year"]),
#     on=["code", "year"],
# )
df_co2_cumulative_countries_2018 = df_cumulative_emissions.query(
    "year==2018"
).copy()


code_to_continent = {
    code: continent
    for _, (code, continent) in country_and_continent_codes[
        ["Three_Letter_Country_Code", "Continent_Name"]
    ]
    .dropna()
    .iterrows()
}

three_to_two_letter_codes = {
    three_letter_code: two_letter_code
    for _, (three_letter_code, two_letter_code) in country_and_continent_codes[
        ["Three_Letter_Country_Code", "Two_Letter_Country_Code"]
    ]
    .dropna()
    .iterrows()
}


two_letter_code_to_german_country_name = {
    code: name for _, (code, name) in country_codes_german.dropna().iterrows()
}

df_cumulative_emissions["continent"] = df_cumulative_emissions["code"].map(
    code_to_continent
)
df_co2_cumulative_with_continents = df_cumulative_emissions[
    ~df_cumulative_emissions["continent"].isna()
].query("year==2018")

continents = (
    df_co2_cumulative_with_continents.groupby("continent")
    .sum()["cumulative_emissions"]
    .index
)
continent_emissions = (
    df_co2_cumulative_with_continents.groupby("continent")
    .sum()["cumulative_emissions"]
    .values
)

continent_translator = {
    "Africa": "Afrika",
    "Asia": "Asien",
    "Europe": "Europa",
    "North America": "Nordamerika",
    "Oceania": "Ozeanine",
    "South America": "Südamerika",
}

df_co2_cumulative_with_continents["country_german"] = (
    df_co2_cumulative_with_continents["code"]
    .map(three_to_two_letter_codes)
    .map(two_letter_code_to_german_country_name)
)

df_co2_cumulative_with_continents["cumulative_emissions"].plot()
