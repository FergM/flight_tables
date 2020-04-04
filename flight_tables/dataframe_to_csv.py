from date_to_dict import fetch_heathrow_data
from dict_to_dataframe import dict_to_dataframe
import pandas as pd

def df_to_csv(df, file_name):
    """Only save if file doesn't exist."""
    try:
        with open( file_name, "x" ) as f:
            df.to_csv(file_name)
    except OSError as exception:
        print(f"Exception Occurred handling the file name: {file_name}")
        print(exception)

def csv_to_df(file_name):
    with open( file_name, "r" ) as f:
        df = pd.read_csv(file_name)
    return df

if __name__=="__main__":
    iso_date_str = "2020-03-20"
    direction = "departures"
    file_name = f"heathrow_{direction}_{iso_date_str}.csv"

    heathrow_data = fetch_heathrow_data(iso_date_str, direction)
    heathrow_df = dict_to_dataframe(heathrow_data)

    df_to_csv(heathrow_df, file_name)

    reloaded_df = csv_to_df(file_name)
    print("Original df last lines:\n", heathrow_df.tail(5))
    print("Reloaded df last lines:\n", reloaded_df.tail(5))
