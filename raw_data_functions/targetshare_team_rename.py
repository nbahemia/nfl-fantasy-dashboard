import os
import pandas as pd

def team_abbreviator() -> pd.DataFrame:
    """
    Load team abbreviation mappings from a CSV file.
    """

    team_abbreviation_map = {
        "Arizona Cardinals": "ARI",
        "Atlanta Falcons": "ATL",
        "Baltimore Ravens": "BAL",
        "Buffalo Bills": "BUF",
        "Carolina Panthers": "CAR",
        "Chicago Bears": "CHI",
        "Cincinnati Bengals": "CIN",
        "Cleveland Browns": "CLE",
        "Dallas Cowboys": "DAL",
        "Denver Broncos": "DEN",
        "Detroit Lions": "DET",
        "Green Bay Packers": "GB",
        "Houston Texans": "HOU",
        "Indianapolis Colts": "IND",
        "Jacksonville Jaguars": "JAX",
        "Kansas City Chiefs": "KC",
        "Las Vegas Raiders": "LV",
        "Los Angeles Chargers": "LAC",
        "Los Angeles Rams": "LAR",
        "Miami Dolphins": "MIA",
        "Minnesota Vikings": "MIN",
        "New England Patriots": "NE",
        "New Orleans Saints": "NO",
        "New York Giants": "NYG",
        "New York Jets": "NYJ",
        "Philadelphia Eagles": "PHI",
        "Pittsburgh Steelers": "PIT",
        "San Francisco 49ers": "SF",
        "Seattle Seahawks": "SEA",
        "Tampa Bay Buccaneers": "TB",
        "Tennessee Titans": "TEN",
        "Washington Commanders": 'WAS'

    }

    df = pd.read_csv(r"downloaded_data/FantasyPros_Fantasy_Football_2024_Target_Distribution.csv")

    df["Team Abbr"] = df["Team"].replace(team_abbreviation_map)
    cols = ["Team", "Team Abbr"] + [c for c in df.columns if c not in ["Team", "Team Abbr"]]
    
    df = df[cols]

    return df

def main():
    df = team_abbreviator()

    os.makedirs("derived_data", exist_ok=True)

    df.to_csv("derived_data/team_abbreviations.csv", index=False)


if __name__ == "__main__":
    main()