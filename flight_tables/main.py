from datetime import datetime, timedelta
import sys

from flight_tables.flight_tables import FlightTables

if __name__=="__main__":
    """
    Save Arrivals and Departures to CSV

    Inputs (Optional):
        date_str (str): Date the data is for. Defaults to yesterday. Should be in the past & still available in Heathrow Airport's API.
    Output:
        Saves Arrivals and Departures CSV table to working directory.
    """
    # Determine the Date
    arg_count = len(sys.argv)

    if arg_count == 1:
        # Default Date to Yesterday
        date = datetime.today().date()-timedelta(days=1)
        date_str = date.isoformat()
    elif arg_count == 2:
        date_str = sys.argv[1]
        try:
            date_format = "%Y-%m-%d"
            date = datetime.strptime(date_str, date_format)
        except:
            sys.exit(f"\nINPUT ERROR: Wrong input format. \n\tExpected 'YYYY-MM-DD' formatted string \n\tReceived: {sys.argv[1]}\n")
    else:
        sys.exit(f"\nINPUT ERROR: Too many input arguments.\n")

    # Save Arrivals CSV
    FlightTables.arrivals_csv(date_str)

    # Save Departures csv
    FlightTables.departures_csv(date_str)
