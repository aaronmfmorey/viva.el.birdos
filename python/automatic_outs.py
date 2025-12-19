from pandas.core.interchange.dataframe_protocol import DataFrame
from pybaseball import cache
from pybaseball import batting_stats
import pandas as pd
from pprint import pprint
import matplotlib.pyplot as plt
import seaborn as sns


def sort_df_by_stat(df: pd.DataFrame, stat_name: str):
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
            "wRC+",
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


def build_chart(df: pd.DataFrame, variable_field: str):
    plt.figure(figsize=(10, 6))
    sns.regplot(
        data=df,
        x=variable_field,
        y="wRC+",
        scatter_kws={"alpha": 0.6, "s": 50},  # s controls point size
        line_kws={"color": "red", "linewidth": 2},
    )
    plt.title(
        f"Relationship between {variable_field} and wRC+",
        fontsize=14,
        fontweight="bold",
    )
    plt.xlabel(variable_field, fontsize=12)
    plt.ylabel("Auto Out Rate", fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def main():
    cache.enable()
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    batting_stats_df = batting_stats(2021, 2025)

    batting_stats_df = calculate_automatic_outs(batting_stats_df)

    strikeouts_subset = sort_df_by_stat(batting_stats_df, "K%")

    print(f"Total Sample Size: {len(strikeouts_subset)}")
    print("Nolan Arenado K% Ranks")
    pprint(strikeouts_subset[strikeouts_subset["Name"] == "Nolan Arenado"])
    print(
        f"Overall Correlation between K% and wRC+:\n{batting_stats_df[['K%', 'wRC+']].corr()}"
    )
    build_chart(batting_stats_df, "K%")

    auto_outs_subset = sort_df_by_stat(batting_stats_df, "auto_out_rate")

    print("Nolan Arenado Automatic Outs Ranks")
    pprint(auto_outs_subset[auto_outs_subset["Name"] == "Nolan Arenado"])
    print(
        f"Overall Correlation between AutoOut% and wRC+:\n{batting_stats_df[['auto_out_rate', 'wRC+']].corr()}"
    )
    build_chart(batting_stats_df, "auto_out_rate")


if __name__ == "__main__":
    main()
