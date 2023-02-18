import pandas as pd

def prep_parquet(csv_file_path:str, playtime:int) -> tuple:
    """
    Read original csv and remove players who join the game once
    """
    df = pd.read_csv(csv_file_path)
    df = df.rename(columns={" level":"level"," race":"race"," charclass":"charclass"," zone":"zone",\
                            " guild":"guild"," timestamp":"timestamp"})
    playonce_users = df.groupby(["char"]).size()[df.groupby(["char"]).size()==playtime]
    playonce_user_ids = playonce_users.index

    df_playonce_users = df.query("char in @playonce_user_ids")
    df_playonce_users = df_playonce_users.reset_index()
    df_playonce_users = df_playonce_users.astype({"timestamp":"datetime64"})
    df_playonce_users.to_parquet("./data/playonce.parquet")

    df = df.query("char not in @playonce_user_ids")
    df = df.reset_index()
    df = df.drop(["index"], axis=1)
    df = df.astype({"timestamp":"datetime64"})
    df.to_parquet("./data/wowah_data.parquet")

    return df.shape
