import math
import pandas as pds
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr


def main():
    pitcher_stats_full = prep_data(pds.read_csv("./pitchers-ip-vs-krate-2002-2025.csv"))
    pitcher_stats_2002 = pitcher_stats_full[pitcher_stats_full["Season"] == 2002]
    pitcher_stats_2025 = pitcher_stats_full[pitcher_stats_full["Season"] == 2025]

    graph_krate_vs_pitches(pitcher_stats_2002, "2002")
    graph_krate_vs_pitches(pitcher_stats_2025, "2025")
    graph_krate_vs_pitches(pitcher_stats_full, "Full")
    print(pitcher_stats_full)

    total_corr = pitcher_stats_full["K%"].corr(pitcher_stats_full["pitches_per_ip"])
    corr_by_season = (
        pitcher_stats_full.groupby("Season")[["K%", "pitches_per_ip"]]
        .corr()
        .unstack()
        .iloc[:, 1]
    )
    print(total_corr)

    graph_correlation_by_year(corr_by_season)


def prep_data(pitcher_stats: pds.DataFrame) -> pds.DataFrame:
    pitcher_stats["IP_norm"] = pitcher_stats["IP"].apply(normalize_innings_pitched)

    pitcher_stats["pitches_per_ip"] = (
        pitcher_stats["Pitches"] / pitcher_stats["IP_norm"]
    )

    return pitcher_stats


"""
Baseball's goofy way of saying .1 innings is 1/3 of an inning is hard to do math on.
Convert to actual thirds.
This is subject to rounding errors but they're so small I don't think they'll affect
the results in any significant way. For example, the input 125.1 returns 125.33333333333331.
"""


def normalize_innings_pitched(innings_pitched: float) -> float:
    floor_value = math.floor(innings_pitched)
    decimal_value = innings_pitched - floor_value
    return floor_value + (decimal_value * 10 * (1 / 3))


def graph_krate_vs_pitches(pitcher_stats: pds.DataFrame, year_label: str):
    # Calculate correlation
    correlation, p_value = pearsonr(
        pitcher_stats["K%"], pitcher_stats["pitches_per_ip"]
    )

    # Set style
    sns.set_style("whitegrid")

    # Create scatter plot with trend line
    plt.figure(figsize=(10, 6))
    sns.regplot(
        data=pitcher_stats,
        x="K%",
        y="pitches_per_ip",
        scatter_kws={"s": 100, "alpha": 0.6},
        line_kws={"color": "red", "linewidth": 2},
    )

    plt.title(f"Pitcher Statistics {year_label}", fontsize=14, fontweight="bold")
    plt.xlabel("K%", fontsize=12)
    plt.ylabel("Pitches per IP", fontsize=12)

    # Add correlation to the plot
    plt.text(
        0.05,
        0.95,
        f"Correlation: {correlation:.3f}",
        transform=plt.gca().transAxes,
        fontsize=11,
        verticalalignment="top",
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
    )

    plt.tight_layout()
    plt.show()


def graph_correlation_by_year(df: pds.Series):
    sns.set_style("whitegrid")

    # Create line plot
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, marker="o", linewidth=2, markersize=8)

    plt.title("Correlation Over Time", fontsize=14, fontweight="bold")
    plt.xlabel("Year", fontsize=12)
    plt.ylabel("Correlation", fontsize=12)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
