from io import StringIO
import requests
import pandas as pd
from bs4 import BeautifulSoup

def fetch_adp(position):
    """
    Fetch Average Draft Position (ADP) data for a given position.
    position: qb, rb, wr, te, k, dst
    """
    url = f"https://www.fantasypros.com/nfl/adp/{position}.php"
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    table = soup.find("table", {"id": "data"})

    df_adp = pd.read_html(StringIO(str(table)))[0]
    df_adp.columns = [' '.join(col).strip() if isinstance(col, tuple) else col for col in df_adp.columns]

    df_adp.rename(columns={"Player Team (Bye)": "Player_TeamBye"}, inplace=True)
    df_adp["Team"] = df_adp["Player_TeamBye"].str.extract(r"\b([A-Z]{2,3})\b")  
    df_adp["(Bye)"] = df_adp["Player_TeamBye"].str.extract(r"\((\d+)\)")
    df_adp["Player"] = df_adp["Player_TeamBye"].str.replace(r"\s+[A-Z]{2,3} \(\d+\)", "", regex=True)
    df_adp.drop(columns=["Player_TeamBye"], inplace=True)

    return df_adp

def fetch_projections(position):
    """
    Fetch projections for a given position.
    position: qb, rb, wr, te, k, dst
    """
    url = f"https://www.fantasypros.com/nfl/projections/{position}.php?week=draft"
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    table = soup.find("table", {"id": "data"})

    df_proj = pd.read_html(StringIO(str(table)))[0]
    df_proj.columns = [' '.join(col).strip() if isinstance(col, tuple) else col for col in df_proj.columns]

    df_proj.rename(columns={df_proj.columns[0]: "Player"}, inplace=True)
    df_proj["Player"] = df_proj["Player"].str.replace(r"\s+[A-Z]{2,3}$", "", regex=True)

    cols_to_label = [c for c in df_proj.columns if c != "Player"]
    df_proj.rename(columns={c: f"{c} (Projected)" for c in cols_to_label}, inplace=True)
    return df_proj

def merge_position(position):
    """
    Merge ADP & Projections for a position.
    """
    df_adp = fetch_adp(position)
    df_proj = fetch_projections(position)

    df_merged = pd.merge(df_adp, df_proj, on="Player", how="inner")

    cols = ["Player", "Team", "(Bye)"] + [c for c in df_merged.columns if c not in ["Player", "Team,", "(Bye)"]]
    df_merged = df_merged[cols]

    return df_merged

def merge_dst():
    """
    Merge ADP & projections for DST.
    """
    url_adp = "https://www.fantasypros.com/nfl/adp/dst.php"
    df_adp = pd.read_html(StringIO(requests.get(url_adp).text))[0]
    df_adp.rename(columns={df_adp.columns[0]: "Team"}, inplace=True)
    df_adp['Team'] = df_adp['Team'].astype(str).str.strip()
    df_adp['Team'] = df_adp['Player Team (Bye)'].str.extract(r'^(.+?) \(\d+\)$')[0]
    df_adp['(Bye)'] = df_adp['Player Team (Bye)'].str.extract(r'\((\d+)\)')[0].astype(float)
    df_adp.drop(columns=['Player Team (Bye)'], inplace=True)

    url_proj = "https://www.fantasypros.com/nfl/projections/dst.php?week=draft"
    df_proj = pd.read_html(StringIO(requests.get(url_proj).text))[0]
    df_proj.rename(columns={df_proj.columns[0]: "Team"}, inplace=True)
    df_proj['Team'] = df_proj['Team'].astype(str).str.strip()

    cols_to_label = [c for c in df_proj.columns if c != "Team"]
    df_proj.rename(columns={c: f"{c} (Projected)" for c in cols_to_label}, inplace=True)

    df_merged = pd.merge(df_adp, df_proj, on="Team", how="inner")
    
    cols = ["Team", "(Bye)"] + [c for c in df_merged.columns if c not in ["Team", "(Bye)"]]
    df_merged = df_merged[cols]

    return df_merged

if __name__ == "__main__":
    positions = ["qb", "rb", "wr", "te", "k"]
    
    for pos in positions:
        df = merge_position(pos)
        df.to_csv(f"{pos}_data.csv", index=False)
        print(f"Saved {pos}_data.csv")
    
    df_dst = merge_dst()
    df_dst.to_csv("dst_data.csv", index=False)
    print(f"Saved dst_data.csv")

