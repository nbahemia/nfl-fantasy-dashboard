from io import StringIO
import requests
import pandas as pd
from bs4 import BeautifulSoup


def fetch_adp(position: str) -> pd.DataFrame:
    """
    Fetch Average Draft Position (ADP) data for a given position.

    Args:
        position (str): The position for which to fetch ADP data. Valid values are: qb, rb, wr, te, k, dst
    
    Returns:
        pd.DataFrame: A DataFrame containing the ADP data for the specified position.
    """
    # Fetches the ADP Data from FantasyPros using BeautifulSoup
    url = f"https://www.fantasypros.com/nfl/adp/{position}.php"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Extracting the table with ADP data
    table = soup.find("table", {"id": "data"})
    if not table:
        raise ValueError(f"No data found for position: {position}")
    
    # Convert to DataFrame and clean column names
    df_adp = pd.read_html(StringIO(str(table)))[0]
    df_adp.columns = [' '.join(col).strip() if isinstance(col, tuple) else col for col in df_adp.columns]

    df_adp = extract_player_info(df_adp)

    return df_adp

def extract_player_info(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract and split player name, team, and bye week from its combined column

    Args:
        df (pd.DataFrame): The DataFrame containing player information.

    Returns:
        pd.DataFrame: The DataFrame with extracted player information.
    """

    df.rename(columns={"Player Team (Bye)": "Player_TeamBye"}, inplace=True)

    # Extracting the team 2-3 letter code (e.g. ARI or LV)
    df["Team"] = df["Player_TeamBye"].str.extract(r"\b([A-Z]{2,3})\b")  

    # Extracting the bye week
    df["(Bye)"] = df["Player_TeamBye"].str.extract(r"\((\d+)\)")

    # Extracting the player name by removing the team and bye week information (replacing them with empty strings)
    df["Player"] = df["Player_TeamBye"].str.replace(r"\s+[A-Z]{2,3} \(\d+\)", "", regex=True)

    df.drop(columns=["Player_TeamBye"], inplace=True)
    return df

def fetch_projections(position: str) -> pd.DataFrame:
    """
    Fetch projections for a given position.

    Args:
        position (str): The position for which to fetch projections. Valid values are: qb, rb, wr, te, k, dst

    Returns:
        pd.DataFrame: A DataFrame containing the projection data for the specified position.
    """
    # Fetches the players' Projected Statistics from FantasyPros using BeautifulSoup
    url = f"https://www.fantasypros.com/nfl/projections/{position}.php?week=draft"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Extracting the table with projection data
    table = soup.find("table", {"id": "data"})
    if not table:
        raise ValueError(f"No data found for position: {position}")
    
    # Convert to DataFrame and clean column names
    df_proj = pd.read_html(StringIO(str(table)))[0]
    df_proj.columns = [' '.join(col).strip() if isinstance(col, tuple) else col for col in df_proj.columns]

    # Clean and rename columns
    df_proj.rename(columns={df_proj.columns[0]: "Player"}, inplace=True)
    df_proj["Player"] = df_proj["Player"].str.replace(r"\s+[A-Z]{2,3}$", "", regex=True)

    # Label statistical columns as projections
    cols_to_label = [c for c in df_proj.columns if c != "Player"]
    df_proj.rename(columns={c: f"{c} (Projected)" for c in cols_to_label}, inplace=True)

    return df_proj

def merge_position(position: str) -> pd.DataFrame:
    """
    Merge ADP & Projections for a position.

    Args:
        position (str): The position for which to merge ADP and projections.

    Returns:
        pd.DataFrame: A DataFrame containing the merged ADP and projection data.
    """

    # Fetching the all ADP data for the position
    df_adp = fetch_adp(position)

    # Fetching the projected stats for all players in the position
    df_proj = fetch_projections(position)

    if df_adp.empty:
        raise ValueError(f"No ADP for position: {position}")
    elif df_proj.empty:
        raise ValueError(f"No projections found for position: {position}")
    # Merging the ADP and projection data on the Player column
    df_merged = pd.merge(df_adp, df_proj, on="Player", how="inner")

    # Reordering columns
    cols = ["Player", "Team", "(Bye)"] + [c for c in df_merged.columns if c not in ["Player", "Team", "(Bye)"]]
    df_merged = df_merged[cols]

    return df_merged

def fetch_dst_adp() -> pd.DataFrame:
    """
    Fetch ADP data for DST.

    Returns:
        pd.DataFrame: A DataFrame containing the ADP data for DST.
    """
    # Fetching the ADP data for DST
    url = "https://www.fantasypros.com/nfl/adp/dst.php"
    response = requests.get(url)

    if response.status_code != 200:
        raise ValueError("Failed to retrieve data")
    
    # Convert to a DataFrame
    df_adp = pd.read_html(StringIO(response.text))[0]

    # Rename first column to Team
    df_adp.rename(columns={df_adp.columns[0]: "Team"}, inplace=True)

    # Extracting the team name and bye week
    df_adp['Team'] = df_adp['Team'].astype(str).str.strip()
    df_adp['Team'] = df_adp['Player Team (Bye)'].str.extract(r'^(.+?) \(\d+\)$')[0]
    df_adp['(Bye)'] = df_adp['Player Team (Bye)'].str.extract(r'\((\d+)\)')[0].astype(float)

    # Dropping the original combined column
    df_adp.drop(columns=['Player Team (Bye)'], inplace=True)

    return df_adp

def fetch_dst_projections() -> pd.DataFrame:
    """
    Fetch projections for DST.
    """
    url_proj = "https://www.fantasypros.com/nfl/projections/dst.php?week=draft"
    response = requests.get(url_proj)
    df_proj = pd.read_html(StringIO(response.text))[0]

    if response.status_code != 200:
        raise ValueError("Failed to retrieve data")

    # Rename first column to Team and clean the Team names
    df_proj.rename(columns={df_proj.columns[0]: "Team"}, inplace=True)
    df_proj['Team'] = df_proj['Team'].astype(str).str.strip()

    # Label statistical columns as projections
    cols_to_label = [c for c in df_proj.columns if c != "Team"]
    df_proj.rename(columns={c: f"{c} (Projected)" for c in cols_to_label}, inplace=True)

    return df_proj

def merge_dst() -> pd.DataFrame:
    """
    Merge ADP & projections for DST.

    Args:
        None

    Returns:
        pd.DataFrame: A DataFrame containing the merged ADP and projection data for DST.
    """
    # Fetching all ADP data for the dst
    df_adp = fetch_dst_adp()

    # Fetching projected stats for all teams in the dst
    df_proj = fetch_dst_projections()

    # Merging the ADP and projection data on the Team column
    df_merged = pd.merge(df_adp, df_proj, on="Team", how="inner")
    
    # Reordering columns for readability
    cols = ["Team", "(Bye)"] + [c for c in df_merged.columns if c not in ["Team", "(Bye)"]]
    df_merged = df_merged[cols]

    return df_merged

def fetch_qb_statistics() -> pd.DataFrame:
    """
    Fetch and process advanced quarterback statistics.

    Args:
        None

    Returns:
        pd.DataFrame: A DataFrame containing the advanced quarterback statistics.
    """
    qb_import_df = pd.read_csv("FantasyPros_Fantasy_Football_Advanced_Stats_Report_QB.csv")

    keep_cols = [
        "Player",
        "G",
        "ATT",
        "YDS",      
        "AIR",
        "10+ YDS",
        "20+ YDS",
        "30+ YDS",
        "SACK",
        "BLITZ",
        "POOR",
        "RZ ATT"
    ]


    qb_df = qb_import_df[[col for col in keep_cols if col in qb_import_df.columns]].copy()

    # Rename per-game stats for clarity
    rename_map = {
        "ATT": "ATT_per_game",
        "YDS": "YDS_per_game",
        "AIR": "AIR_per_game",
        "10+ YDS": "10+_YDS_per_game",
        "20+ YDS": "20+_YDS_per_game",
        "30+ YDS": "30+_YDS_per_game",
        "SACK": "SACK_per_game",
        "BLITZ": "BLITZ_per_game",
        "POOR": "POOR_per_game",
        "RZ ATT": "RZ_ATT_per_game"
    }
    qb_df.rename(columns=rename_map, inplace=True)

    # Convert per-game stats to totals
    qb_df["TOTAL_ATT"] = qb_df["ATT_per_game"] * qb_df["G"]
    qb_df["TOTAL_YDS"] = qb_df["YDS_per_game"] * qb_df["G"]
    qb_df["TOTAL_AIR"] = qb_df["AIR_per_game"] * qb_df["G"]
    qb_df["TOTAL_10YDS"] = qb_df["10+_YDS_per_game"] * qb_df["G"]
    qb_df["TOTAL_20YDS"] = qb_df["20+_YDS_per_game"] * qb_df["G"]
    qb_df["TOTAL_30YDS"] = qb_df["30+_YDS_per_game"] * qb_df["G"]
    qb_df["TOTAL_RZ_ATT"] = qb_df["RZ_ATT_per_game"] * qb_df["G"]

    # Removing the team abbreviation for future merge
    qb_df["Player"] = qb_df["Player"].str.replace(r"\s*\([A-Z]{2,3}\)$", "", regex=True)

    return qb_df

def fetch_rb_statistics() -> pd.DataFrame:
    """
    Fetch and process advanced running back statistics.

    Args:
        None

    Returns:
        pd.DataFrame: A DataFrame containing the advanced running back statistics.
    """
    rb_import_df = pd.read_csv("FantasyPros_Fantasy_Football_Advanced_Stats_Report_RB.csv")

    # Selecting relevant columns
    keep_cols = [
            "Player",
            "G",
            "ATT",        
            "YBCON",      
            "YACON",    
            "BRKTKL",    
            "TK LOSS",    
            "TK LOSS YDS",
            "10+ YDS",
            "20+ YDS",
            "30+ YDS",
            "40+ YDS",
            "50+ YDS",
            "TGT",        
            "RZ TGT"    
    ]
    
    # Filtering the DataFrame to keep only the relevant columns
    rb_df = rb_import_df[[col for col in keep_cols if col in rb_import_df.columns]].copy()
    
    # Renaming columns for clarity
    rename_map = {col: f"{col} PER GAME" for col in keep_cols if col not in ["Player", "G"]}
    rb_df.rename(columns=rename_map, inplace=True)

    rb_df["TOTAL_ATT"] = rb_df["ATT PER GAME"] * rb_df["G"]
    rb_df["TOTAL_YBCON"] = rb_df["YBCON PER GAME"] * rb_df["G"]
    rb_df["TOTAL_YACON"] = rb_df["YACON PER GAME"] * rb_df["G"]
    rb_df["TOTAL_BRKTKL"] = rb_df["BRKTKL PER GAME"] * rb_df["G"]
    rb_df["TOTAL_TK_LOSS"] = rb_df["TK LOSS PER GAME"] * rb_df["G"]
    rb_df["TOTAL_TK_LOSS_YDS"] = rb_df["TK LOSS YDS PER GAME"] * rb_df["G"]
    rb_df["TOTAL_10YDS"] = rb_df["10+ YDS PER GAME"] * rb_df["G"]
    rb_df["TOTAL_20YDS"] = rb_df["20+ YDS PER GAME"] * rb_df["G"]
    rb_df["TOTAL_30YDS"] = rb_df["30+ YDS PER GAME"] * rb_df["G"]
    rb_df["TOTAL_40YDS"] = rb_df["40+ YDS PER GAME"] * rb_df["G"]
    rb_df["TOTAL_50YDS"] = rb_df["50+ YDS PER GAME"] * rb_df["G"]
    rb_df["TOTAL_TGT"] = rb_df["TGT PER GAME"] * rb_df["G"]
    rb_df["TOTAL_RZ_TGT"] = rb_df["RZ TGT PER GAME"] * rb_df["G"]

    # Removing the team abbreviation for future merge
    rb_df["Player"] = rb_df["Player"].str.replace(r"\s*\([A-Z]{2,3}\)$", "", regex=True)

    return rb_df

def fetch_wr_statistics() -> pd.DataFrame:
    """
    Fetch and process advanced wide receiver statistics.

    Args:
        None

    Returns:
        pd.DataFrame: A DataFrame containing the advanced wide receiver statistics.
    """
    wr_import_df = pd.read_csv("FantasyPros_Fantasy_Football_Advanced_Stats_Report_WR.csv")

    # Selecting relevant columns
    keep_cols = [
            "Player",
            "G",
            "REC",
            "YDS",
            "YBC",
            "AIR",
            "YAC",
            "YACON",
            "BRKTKL",
            "TGT",
            "CATCHABLE",
            "DROP",
            "RZ TGT",
            "10+ YDS",
            "20+ YDS"
    ]

    # Filtering the DataFrame to keep only the relevant columns
    wr_df = wr_import_df[[col for col in keep_cols if col in wr_import_df.columns]].copy()
    
    # Renaming columns for clarity
    rename_map = {col: f"{col} PER GAME" for col in keep_cols if col not in ["Player", "G"]}
    wr_df.rename(columns=rename_map, inplace=True)

    wr_df["TOTAL_REC"] = wr_df["REC PER GAME"] * wr_df["G"]
    wr_df["TOTAL_YDS"] = wr_df["YDS PER GAME"] * wr_df["G"]
    wr_df["TOTAL_YBC"] = wr_df["YBC PER GAME"] * wr_df["G"]
    wr_df["TOTAL_AIR"] = wr_df["AIR PER GAME"] * wr_df["G"]
    wr_df["TOTAL_YAC"] = wr_df["YAC PER GAME"] * wr_df["G"]
    wr_df["TOTAL_YACON"] = wr_df["YACON PER GAME"] * wr_df["G"]
    wr_df["TOTAL_BRKTKL"] = wr_df["BRKTKL PER GAME"] * wr_df["G"]
    wr_df["TOTAL_TGT"] = wr_df["TGT PER GAME"] * wr_df["G"]
    wr_df["TOTAL_CATCHABLE"] = wr_df["CATCHABLE PER GAME"] * wr_df["G"]
    wr_df["TOTAL_DROP"] = wr_df["DROP PER GAME"] * wr_df["G"]
    wr_df["TOTAL_RZ_TGT"] = wr_df["RZ TGT PER GAME"] * wr_df["G"]
    wr_df["TOTAL_10YDS"] = wr_df["10+ YDS PER GAME"] * wr_df["G"]
    wr_df["TOTAL_20YDS"] = wr_df["20+ YDS PER GAME"] * wr_df["G"]

    # Removing the team abbreviation for future merge
    wr_df["Player"] = wr_df["Player"].str.replace(r"\s*\([A-Z]{2,3}\)$", "", regex=True)

    return wr_df

def fetch_te_statistics() -> pd.DataFrame:
    """
    Fetch and process advanced tight end statistics.

    Args:
        None

    Returns:
        pd.DataFrame: A DataFrame containing the advanced tight end statistics.
    """
    te_import_df = pd.read_csv("FantasyPros_Fantasy_Football_Advanced_Stats_Report_TE.csv")

    # Selecting relevant columns
    keep_cols = [
        "Player",
        "G",
        "REC",
        "YDS",
        "YBC",
        "AIR",
        "YAC",
        "YACON",
        "BRKTKL",
        "TGT",
        "CATCHABLE",
        "DROP",
        "RZ TGT",
        "10+ YDS",
        "20+ YDS"
    ]

    # Filtering the DataFrame to keep only the relevant columns
    te_df = te_import_df[[col for col in keep_cols if col in te_import_df.columns]].copy()

    # Renaming columns for clarity
    rename_map = {col: f"{col} PER GAME" for col in keep_cols if col not in ["Player", "G"]}
    te_df.rename(columns=rename_map, inplace=True)

    te_df["TOTAL_REC"] = te_df["REC PER GAME"] * te_df["G"]
    te_df["TOTAL_YDS"] = te_df["YDS PER GAME"] * te_df["G"]
    te_df["TOTAL_YBC"] = te_df["YBC PER GAME"] * te_df["G"]
    te_df["TOTAL_AIR"] = te_df["AIR PER GAME"] * te_df["G"]
    te_df["TOTAL_YAC"] = te_df["YAC PER GAME"] * te_df["G"]
    te_df["TOTAL_YACON"] = te_df["YACON PER GAME"] * te_df["G"]
    te_df["TOTAL_BRKTKL"] = te_df["BRKTKL PER GAME"] * te_df["G"]
    te_df["TOTAL_TGT"] = te_df["TGT PER GAME"] * te_df["G"]
    te_df["TOTAL_CATCHABLE"] = te_df["CATCHABLE PER GAME"] * te_df["G"]
    te_df["TOTAL_DROP"] = te_df["DROP PER GAME"] * te_df["G"]
    te_df["TOTAL_RZ_TGT"] = te_df["RZ TGT PER GAME"] * te_df["G"]
    te_df["TOTAL_10YDS"] = te_df["10+ YDS PER GAME"] * te_df["G"]
    te_df["TOTAL_20YDS"] = te_df["20+ YDS PER GAME"] * te_df["G"]

    # Removing the team abbreviation for future merge
    te_df["Player"] = te_df["Player"].str.replace(r"\s*\([A-Z]{2,3}\)$", "", regex=True)

    return te_df

def merge_skill_position_metrics(adv_stats: pd.DataFrame, projections: pd.DataFrame) -> pd.DataFrame:
    """
    Merge advanced statistics with projections for skill positions (QB, RB, WR, TE).

    Args:
        adv_stats (pd.DataFrame): The advanced statistics DataFrame for the skill position.
        projections (pd.DataFrame): The projections DataFrame for the skill position.

    Returns:
        pd.DataFrame: A DataFrame containing the merged advanced statistics and projections.
    """

    # Merge the advanced statistics with the projections
    full_player_profile = pd.merge(projections, adv_stats, on="Player", how="left")

    # Fill missing values, indicating they are rookies or reintroduced into the league
    full_player_profile.fillna("N/A", inplace=True)

    return full_player_profile

def main():
    """
    Main function to run the data pipeline for fantasy football statistics.
    Fetches ADP, projections, and advanced statistics for various positions.
    Merges them into a comprehensive DataFrame for analysis.
    """

    # Fetch advanced statistics and projections for skill positions
    adv_stats_qb = fetch_qb_statistics()
    adp_proj_qb = merge_position("qb")
    full_qb_profile = merge_skill_position_metrics(adv_stats_qb, adp_proj_qb)

    adv_stats_rb = fetch_rb_statistics()
    proj_rb = fetch_projections("rb")
    full_rb_profile = merge_skill_position_metrics(adv_stats_rb, proj_rb)

    adv_stats_wr = fetch_wr_statistics()
    proj_wr = fetch_projections("wr")
    full_wr_profile = merge_skill_position_metrics(adv_stats_wr, proj_wr)

    adv_stats_te = fetch_te_statistics()
    proj_te = fetch_projections("te")
    full_te_profile = merge_skill_position_metrics(adv_stats_te, proj_te)

    # Save the two positions without advanced stats
    proj_k = merge_position("k")

    proj_dst = merge_dst()

    # Save the full data to CSV files
    full_qb_profile.to_csv("full_qb_data.csv", index=False)
    full_rb_profile.to_csv("full_rb_data.csv", index=False)
    full_wr_profile.to_csv("full_wr_data.csv", index=False)
    full_te_profile.to_csv("full_te_data.csv", index=False)
    proj_k.to_csv("full_k_data.csv", index=False)
    proj_dst.to_csv("full_dst_data.csv", index=False)

    print("All data fetched and processed successfully.")

if __name__ == "__main__":
    main()