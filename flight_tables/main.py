from datetime import datetime, timedelta
from flight_tables.flight_tables import FlightTables

if __name__=="__main__":
    """Save Arrivals and Departures to csv"""
    date = datetime.today().date()-timedelta(days=1)
    date_str = date.isoformat()

    # Save Arrivals CSV
    FlightTables.arrivals_csv(date_str)

    # Save Departures csv
    FlightTables.departures_csv(date_str)
