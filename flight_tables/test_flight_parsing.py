from datetime import datetime
import unittest

from flight_parsing import Flight, ParsedFlights

class SampleData(object):
    
    def __init__(self):
        self.test_flight_departed_1 =   {'actual_datetime': datetime(2020, 1, 30, 15, 15),
                                        'code_share_type': 'CODESHARE_MARKETING_FLIGHT',
                                        'destination': 'YYC',
                                        'flight_id': 'OS8237',
                                        'origin': 'LHR',
                                        'scheduled_datetime': datetime(2020, 1, 30, 14, 30),
                                        'status': 'Departed'}

        self.test_flight_departed_2 =   {'actual_datetime': datetime(2020, 2, 14, 6, 26),
                                        'code_share_type': 'CODESHARE_MARKETING_FLIGHT',
                                        'destination': 'VIE',
                                        'flight_id': 'AC6186',
                                        'origin': 'LHR',
                                        'scheduled_datetime': datetime(2020, 2, 14, 6, 0),
                                        'status': 'Departed'}

        self.test_flight_cancelled_1 =  {'actual_datetime': None,
                                        'code_share_type': 'CODESHARE_MARKETING_FLIGHT',
                                        'destination': 'DOH',
                                        'flight_id': 'BA7008',
                                        'origin': 'LHR',
                                        'scheduled_datetime': datetime(2020, 1, 30, 15, 5),
                                        'status': 'Cancelled'}

    def three_flights_one_cancelled(self):
        return [self.test_flight_departed_1, self.test_flight_departed_2, self.test_flight_cancelled_1]

class TestFlight(unittest.TestCase):
    """Test the class called Flight"""

    def setUp(self):
        self.flight_info = SampleData().test_flight_departed_1
        self.flight = Flight(self.flight_info)

    def test_delay_calculation(self):
        #A Proper Delay
        scheduled_datetime = datetime(2020,2,2,7,30)
        actual_datetime = datetime(2020,2,2,8,30)
        delay_mins = Flight.calculate_delay_minutes(scheduled_datetime, actual_datetime)
        self.assertEqual(delay_mins, 60)

        #An Early Flight
        scheduled_datetime = datetime(2020,2,2,7,30)
        actual_datetime = datetime(2020,2,2,6,30)
        delay_mins = self.flight.calculate_delay_minutes(scheduled_datetime, actual_datetime)
        self.assertEqual(delay_mins, -60)

        #Flight with None as an input
        actual_datetime = None
        scheduled_datetime = datetime(2020,2,2,8,30)
        delay_mins = self.flight.calculate_delay_minutes(scheduled_datetime, actual_datetime)
        self.assertEqual(delay_mins, None)

    def test_the_init(self):
        self.assertIsInstance(self.flight.flight_id, str) #ToDO: assert regex string length >=0 with no whitespace.
        self.assertIsInstance(self.flight.scheduled_datetime, datetime)
        self.assertIsInstance(self.flight.actual_datetime, datetime)#Note: will return None and fail in some cases. 
        self.assertIn(type(self.flight.delay_mins), (float, type(None)))

    def test_to_list(self):
        self.assertIsInstance(self.flight.to_list(), list)
        self.assertEqual(len(self.flight.to_list()), len(self.flight.labels()))

class TestParsedFlights(unittest.TestCase):
    def setUp(self):
        self.batch_info = SampleData().three_flights_one_cancelled()
        self.parsed_flights = ParsedFlights(self.batch_info)
        
    def test_the_init(self):
        self.assertEqual(len(self.parsed_flights.parsed_flights), len(self.batch_info))
        #Check parsed_flights have the right class (the user defined Flight class)
        #   For brevity, just check the first parsed_flight .
        self.assertEqual(str(type(self.parsed_flights.parsed_flights[0])), "<class 'flight_parsing.Flight'>")

    def test_to_dataframe(self):
        flight_df = self.parsed_flights.to_dataframe()
        self.assertEqual(len(flight_df), len(self.batch_info))
        self.assertEqual(list(flight_df.columns), Flight.labels())
        #print(flight_df.head())

if __name__ == '__main__':
   unittest.main()