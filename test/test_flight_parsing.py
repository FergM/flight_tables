from datetime import datetime
import unittest

from flight_tables.flight_parsing import Flight, ParsedFlights

class SampleData(object):
    
    def __init__(self):
        self.test_flight_departed_1 =   {'actual_datetime': datetime(2020, 1, 30, 15, 15),
                                        'code_share_type': 'main_code',
                                        'destination': 'YYC',
                                        'flight_id': 'OS8237',
                                        'origin': 'LHR',
                                        'scheduled_datetime': datetime(2020, 1, 30, 14, 30),
                                        'status': 'Departed'}

        self.test_flight_departed_2 =   {'actual_datetime': datetime(2020, 2, 14, 6, 26),
                                        'code_share_type': 'alt_code',
                                        'destination': 'VIE',
                                        'flight_id': 'AC6186',
                                        'origin': 'LHR',
                                        'scheduled_datetime': datetime(2020, 2, 14, 6, 0),
                                        'status': 'Departed'}

        self.test_flight_cancelled_1 =  {'actual_datetime': None,
                                        'code_share_type': 'no_codeshare',
                                        'destination': 'DOH',
                                        'flight_id': 'BA7008',
                                        'origin': 'LHR',
                                        'scheduled_datetime': datetime(2020, 1, 30, 15, 5),
                                        'status': 'Cancelled'}

        self.flight_info_list = [self.test_flight_departed_1, self.test_flight_departed_2, self.test_flight_cancelled_1]

class TestFlight(unittest.TestCase):
    """Test the class called Flight"""

    def setUp(self):
        self.flight_info_list = SampleData().flight_info_list

    def test_runner(self):
        # Check 1
        self.check_delay_calculation()

        for i, raw_flight in enumerate(self.flight_info_list):
            flight_info = self.flight_info_list[i]
            flight = Flight(flight_info)
            with self.subTest(list_position=i, flight_id = flight_info["flight_id"]):
                # Checks 2 and 3
                self.flight_validation(flight)
                self.check_to_list(flight)

    def check_delay_calculation(self):
        #A Proper Delay
        scheduled_datetime = datetime(2020,2,2,7,30)
        actual_datetime = datetime(2020,2,2,8,30)
        delay_mins = Flight.calculate_delay_minutes(scheduled_datetime, actual_datetime)
        self.assertEqual(delay_mins, 60)

        #An Early Flight
        scheduled_datetime = datetime(2020,2,2,7,30)
        actual_datetime = datetime(2020,2,2,6,30)
        delay_mins = Flight.calculate_delay_minutes(scheduled_datetime, actual_datetime)
        self.assertEqual(delay_mins, -60)

        #Flight with None as an input
        actual_datetime = None
        scheduled_datetime = datetime(2020,2,2,8,30)
        delay_mins = Flight.calculate_delay_minutes(scheduled_datetime, actual_datetime)
        self.assertEqual(delay_mins, None)

    def flight_validation(self, flight):
        codeshare_types = ["alt_code", "main_code", "no_codeshare"]
        status_types = [ "Landed", "Departed", "Cancelled"]
        actual_datetime_types = (datetime, type(None))
        self.assertIsInstance(flight.scheduled_datetime, datetime)
        self.assertIsInstance(flight.actual_datetime, actual_datetime_types)
        if type(flight.actual_datetime) == datetime:
            self.assertEqual(flight.actual_datetime.tzinfo, None)
        self.assertEqual(flight.scheduled_datetime.tzinfo, None)

        self.assertIsInstance(flight.origin, str)
        self.assertIsInstance(flight.destination, str)
        self.assertTrue(len(flight.origin), 3)
        self.assertTrue(len(flight.destination), 3)

        self.assertIsInstance(flight.flight_id, str) # Can extend to check start is letter and end is number; no whitespace.
        self.assertIn(flight.code_share_type, codeshare_types)

        self.assertIn(flight.status, status_types)
        self.assertIn(type(flight.delay_mins), (float, type(None)))

    def check_to_list(self, flight):
        self.assertIsInstance(flight.to_list(), list)
        self.assertEqual(len(flight.to_list()), len(flight.labels()))

class TestParsedFlights(unittest.TestCase):
    def setUp(self):
        self.batch_info = SampleData().flight_info_list
        self.parsed_flights = ParsedFlights(self.batch_info)
        
    def test_the_init(self):
        self.assertEqual(len(self.parsed_flights.parsed_flights), len(self.batch_info))
        #Check parsed_flights have the right class (the user defined Flight class)
        #   For brevity, just check the first parsed_flight .
        self.assertEqual(str(type(self.parsed_flights.parsed_flights[0])), "<class 'flight_tables.flight_parsing.Flight'>")

    def test_to_dataframe(self):
        flight_df = self.parsed_flights.to_dataframe()
        self.assertEqual(len(flight_df), len(self.batch_info))
        self.assertEqual(list(flight_df.columns), Flight.labels())
        #print(flight_df.head())

if __name__ == '__main__':
   unittest.main()
