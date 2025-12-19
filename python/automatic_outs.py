from pandas.core.interchange.dataframe_protocol import DataFrame
from pybaseball import cache
from pybaseball import batting_stats
import pandas as pds
from pprint import pprint


def sort_df_by_stat(df: pds.DataFrame, stat_name: str):
    strikeouts_df = df.sort_values(by=stat_name, ascending=True)
    strikeouts_df.reset_index(drop=True)
    strikeouts_df["Rank"] = range(1, len(strikeouts_df) + 1)
    return strikeouts_df[
        [
            "Rank",
            "Name",
            "Season",
            "AB",
            "SO",
            "K%",
            "IFFB",
            "auto_outs",
            "auto_out_rate",
        ]
    ]


def calculate_automatic_outs(batting_stats_df: DataFrame):
    batting_stats_df["auto_outs"] = batting_stats_df["SO"] + batting_stats_df["IFFB"]
    batting_stats_df["auto_out_rate"] = (
        batting_stats_df["auto_outs"] / batting_stats_df["AB"]
    )
    return batting_stats_df


def main():
    cache.enable()
    pds.set_option("display.max_rows", None)
    batting_stats_df = batting_stats(2021, 2025)

    batting_stats_df = calculate_automatic_outs(batting_stats_df)

    strikeouts_subset = sort_df_by_stat(batting_stats_df, "K%")

    print(f"Total Sample Size: {len(strikeouts_subset)}")
    print("Nolan Arenado K% Ranks")
    pprint(strikeouts_subset[strikeouts_subset["Name"] == "Nolan Arenado"])

    auto_outs_subset = sort_df_by_stat(batting_stats_df, "auto_out_rate")

    print("Nolan Arenado Automatic Outs Ranks")
    pprint(auto_outs_subset[auto_outs_subset["Name"] == "Nolan Arenado"])


if __name__ == "__main__":
    main()
