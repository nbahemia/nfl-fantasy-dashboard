from io import StringIO
import requests
import pandas as pd
from bs4 import BeautifulSoup

def fetch_qb_statistics():
    """
    Load and process quarterback statistics from the downloaded FantasyPros CSV.
    Renames raw columns to 'per game' versions and adds season totals.
    """

    qb_import_df = pd.read_csv("downloaded_data\FantasyPros_Fantasy_Football_Advanced_Stats_Report_QB.csv")

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

    qb_df["Player"] = qb_df["Player"].str.replace(r"\s*\([A-Z]{2,3}\)$", "", regex=True)
    print(qb_df["Player"])
    return qb_df

def fetch_rb_statistics():
    """
    Fetch and process running back statistics from SumerSports.
    """

    rb_import_df = pd.read_csv("downloaded_data\FantasyPros_Fantasy_Football_Advanced_Stats_Report_RB.csv")

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

    rb_df = rb_import_df[[col for col in keep_cols if col in rb_import_df.columns]].copy()


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

    return rb_df

def fetch_wr_statistics():
    """
    Fetch and process wide receiver statistics from FantasyPros CSV.
    Converts per-game stats into season totals for key metrics.
    """

    wr_import_df = pd.read_csv("downloaded_data\FantasyPros_Fantasy_Football_Advanced_Stats_Report_WR.csv")

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

    wr_df = wr_import_df[[col for col in keep_cols if col in wr_import_df.columns]].copy()

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

    return wr_df

def fetch_te_statistics():
    te_import_df = pd.read_csv("downloaded_data\FantasyPros_Fantasy_Football_Advanced_Stats_Report_TE.csv")

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

    te_df = te_import_df[[col for col in keep_cols if col in te_import_df.columns]].copy()

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

    return te_df

if __name__ == "__main__":
    qb_df = fetch_qb_statistics()
    rb_df = fetch_rb_statistics()
    wr_df = fetch_wr_statistics()
    te_df = fetch_te_statistics()

    print("Quarterback Statistics:")
    print(qb_df)

    print("\nRunning Back Statistics:")
    print(rb_df)

    print("\nWide Receiver Statistics:")
    print(wr_df)

    print("\nTight End Statistics:")
    print(te_df)
