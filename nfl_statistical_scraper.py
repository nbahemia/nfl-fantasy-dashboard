from io import StringIO
import requests
import pandas as pd
from bs4 import BeautifulSoup

def fetch_qb_statistics():
    """
    Fetch and process quarterback statistics from SumerSports.
    """

    url = "https://www.fantasypros.com/nfl/advanced-stats-qb.php"
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    table = soup.find("table", {"id": "data"})

    qb_df = pd.read_html(StringIO(str(table)))[0]

    if isinstance(qb_df.columns, pd.MultiIndex):
        qb_df.columns = [' '.join(col).strip() for col in qb_df.columns.values]
    else:
        qb_df.columns = [col.strip() for col in qb_df.columns]

    keep_cols = [
        "Unnamed: 1_level_0 Player",
        "PASSING ATT",
        "PASSING Y/A",
        "PASSING AIR",
        "DEEP BALL PASSING 10+ YDS",
        "DEEP BALL PASSING 20+ YDS",
        "DEEP BALL PASSING 30+ YDS",
        "PRESSURE PKT TIME",
        "PRESSURE SACK",
        "PRESSURE BLITZ",
        "MISC POOR",
        "MISC RZ ATT"
    ]

    qb_df = qb_df[[col for col in keep_cols if col in qb_df.columns]]
    qb_df.rename(columns={"Unnamed: 1_level_0 Player": "PLAYER"}, inplace=True)

    return qb_df

def fetch_rb_statistics():
    """
    Fetch and process running back statistics from SumerSports.
    """

    url = "https://www.fantasypros.com/nfl/advanced-stats-rb.php"
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    table = soup.find("table", {"id": "data"})

    rb_df = pd.read_html(StringIO(str(table)))[0]

    if isinstance(rb_df.columns, pd.MultiIndex):
        rb_df.columns = [' '.join(col).strip() for col in rb_df.columns.values]
    else:
        rb_df.columns = [col.strip() for col in rb_df.columns]

    keep_cols = [
        "Unnamed: 1_level_0 Player",
        "RUSHING ATT",
        "RUSHING YBCON",
        "RUSHING YACON",
        "RUSHING YACON/ATT",
        "RUSHING BRKTKL",
        "RUSHING TK LOSS",
        "RUSHING TK LOSS YDS",
        "BIG RUSH PLAYS 10+ YDS",
        "BIG RUSH PLAYS 20+ YDS",
        "BIG RUSH PLAYS 30+ YDS",
        "BIG RUSH PLAYS 40+ YDS",
        "BIG RUSH PLAYS 50+ YDS",
        "RECEIVING TGT",
        "RECEIVING RZ TGT"
    ]

    rb_df = rb_df[[col for col in keep_cols if col in rb_df.columns]]
    rb_df.rename(columns={"Unnamed: 1_level_0 Player": "PLAYER"}, inplace=True)

    return rb_df

def fetch_wr_statistics():
    """
    Fetch and process wide receiver statistics from SumerSports.
    """

    url = "https://www.fantasypros.com/nfl/advanced-stats-wr.php"
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    table = soup.find("table", {"id": "data"})

    wr_df = pd.read_html(StringIO(str(table)))[0]

    if isinstance(wr_df.columns, pd.MultiIndex):
        wr_df.columns = [' '.join(col).strip() for col in wr_df.columns.values]
    else:
        wr_df.columns = [col.strip() for col in wr_df.columns]

    keep_cols = [
        "Unnamed: 1_level_0 Player", 
        "RECEIVING YAC", 
        "RECEIVING YBC", 
        "RECEIVING AIR", 
        "TARGETS BRKTKL", 
        "TARGETS TGT", 
        "TARGETS % TM", 
        "TARGETS CATCHABLE", 
        "TARGETS DROP", 
        "TARGETS RZ TGT", 
        "BIG PLAYS 10+ YDS", 
        "BIG PLAYS 20+ YDS"
    ]

    wr_df = wr_df[[col for col in keep_cols if col in wr_df.columns]]
    wr_df.rename(columns={"Unnamed: 1_level_0 Player": "PLAYER"}, inplace=True)

    return wr_df

def fetch_te_statistics():
    """
    Fetch and process wide receiver statistics from SumerSports.
    """

    url = "https://www.fantasypros.com/nfl/advanced-stats-te.php"
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    table = soup.find("table", {"id": "data"})

    te_df = pd.read_html(StringIO(str(table)))[0]

    if isinstance(te_df.columns, pd.MultiIndex):
        te_df.columns = [' '.join(col).strip() for col in te_df.columns.values]
    else:
        te_df.columns = [col.strip() for col in te_df.columns]

    keep_cols = [
        "Unnamed: 1_level_0 Player", 
        "RECEIVING YBC",
        "RECEIVING AIR", 
        "RECEIVING YAC", 
        "RECEIVING YACON", 
        "RECEIVING BRKTKL", 
        "TARGETS TGT", 
        "TARGETS % TM", 
        "TARGETS CATCHABLE", 
        "TARGETS DROP", 
        "TARGETS RZ TGT", 
        "BIG PLAYS 10+ YDS", 
        "BIG PLAYS 20+ YDS"
    ]


    te_df = te_df[[col for col in keep_cols if col in te_df.columns]]
    te_df.rename(columns={"Unnamed: 1_level_0 Player": "PLAYER"}, inplace=True)

    return te_df

if __name__ == "__main__":
    qb_df = fetch_qb_statistics()
    rb_df = fetch_rb_statistics()
    wr_df = fetch_wr_statistics()
    te_df = fetch_te_statistics()

    print("Quarterback Statistics:")
    print(qb_df.head())

    print("\nRunning Back Statistics:")
    print(rb_df.head())

    print("\nWide Receiver Statistics:")
    print(wr_df.head())

    print("\nTight End Statistics:")
    print(te_df.head())
