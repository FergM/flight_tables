from datetime import datetime
from flight_parsing import Flight, ParsedFlights
from heathrow_parsing import extract_flight_heathrow, extract_batch_heathrow
import json
import unittest

class SampleData(object):
    
    def __init__(self):
        self.test_flight_departed_1 = json.loads(r'''{"flightIdentifier":"OS8237","flightNumber":"8237","airlineIataRef":"OS","origin":{"airportIataRef":"LHR","terminalCode":"2","status":{"interpretedStatus":" Departed 15:15  ","category":"INFO","messages":{"message":[{"text":"Departed","data":"15:15"},{"text":" "}]},"code":"AB","statusTime":"2020-01-30T15:15:00.000Z"},"scheduledDateTime":{"utc":"2020-01-30T14:30:00.000","local":"2020-01-30T14:30:00.000","utcOffset":0}},"destination":{"airportIataRef":"YYC"},"stops":{"stop":[],"count":0},"codeShareType":"CODESHARE_MARKETING_FLIGHT","isHadacabCancelled":false}''')
        self.test_flight_departed_2 = json.loads(r'''{"flightIdentifier":"AC6186","flightNumber":"6186","airlineIataRef":"AC","origin":{"airportIataRef":"LHR","terminalCode":"2","status":{"interpretedStatus":" Departed 06:26  ","category":"INFO","messages":{"message":[{"text":"Departed","data":"06:26"},{"text":" "}]},"code":"AB","statusTime":"2020-02-14T06:26:00.000Z"},"scheduledDateTime":{"utc":"2020-02-14T06:00:00.000","local":"2020-02-14T06:00:00.000","utcOffset":0}},"destination":{"airportIataRef":"VIE"},"stops":{"stop":[],"count":0},"codeShareType":"CODESHARE_MARKETING_FLIGHT","isHadacabCancelled":false}''')
        self.test_flight_cancelled_1 = json.loads(r'''{"flightIdentifier":"BA7008","flightNumber":"7008","airlineIataRef":"BA","origin":{"airportIataRef":"LHR","terminalCode":"4","status":{"interpretedStatus":" Cancelled Contact airline","category":"INFO","messages":{"message":[{"text":"Cancelled"},{"text":"Contact airline"}]},"code":"CX","statusTime":"2020-01-30T15:05:00.000Z"},"scheduledDateTime":{"utc":"2020-01-30T15:05:00.000","local":"2020-01-30T15:05:00.000","utcOffset":0}},"destination":{"airportIataRef":"DOH"},"stops":{"stop":[],"count":0},"codeShareType":"CODESHARE_MARKETING_FLIGHT","isHadacabCancelled":false}''')

    def three_flights_one_cancelled(self):
        return [self.test_flight_departed_1, self.test_flight_departed_2, self.test_flight_cancelled_1]

class TestFlight(unittest.TestCase):
    """Test the class called Flight"""

    def setUp(self):
        raw_flight = SampleData().test_flight_departed_1
        self.flight_info = extract_flight_heathrow(raw_flight)

    def test_delay_calculation(self):
        #Instantiate the class
        #   to access delay calc function
        flight = Flight(self.flight_info)

        #A Proper Delay
        scheduled_datetime = datetime(2020,2,2,7,30)
        actual_datetime = datetime(2020,2,2,8,30)
        delay_mins = Flight.calculate_delay_minutes(scheduled_datetime, actual_datetime)
        self.assertEqual(delay_mins, 60)

        #An Early Flight
        scheduled_datetime = datetime(2020,2,2,7,30)
        actual_datetime = datetime(2020,2,2,6,30)
        delay_mins = flight.calculate_delay_minutes(scheduled_datetime, actual_datetime)
        self.assertEqual(delay_mins, -60)

        #Flight with None as an input
        actual_datetime = None
        scheduled_datetime = datetime(2020,2,2,8,30)
        delay_mins = flight.calculate_delay_minutes(scheduled_datetime, actual_datetime)
        self.assertEqual(delay_mins, None)

    def test_the_init(self):
        flight = Flight(self.flight_info)
        self.assertIsInstance(flight.flight_id, str) #ToDO: assert regex string length >=0 with no whitespace.
        self.assertIsInstance(flight.scheduled_datetime, datetime)
        self.assertIsInstance(flight.actual_datetime, datetime)#Note: will return None and fail in some cases. 
        self.assertIn(type(flight.delay_mins), (float, type(None)))

    def test_to_list(self):
        flight = Flight(self.flight_info)
        self.assertIsInstance(flight.to_list(), list)
        self.assertEqual(len(flight.to_list()), len(flight.labels()))

class TestParsedFlights(unittest.TestCase):
    def setUp(self):
        sample_response = {}
        sample_response['flightSummaryList'] = {}
        sample_response['flightSummaryList']['flight'] = None
        sample_response['flightSummaryList']['flight'] = SampleData().three_flights_one_cancelled()
        self.batch_info = extract_batch_heathrow(sample_response)
        
    def test_the_init(self):
        parsed_flights = ParsedFlights(self.batch_info)
        self.assertEqual(len(parsed_flights.parsed_flights), len(self.batch_info))
        #Check parsed_flights have the right class (the user defined Flight class)
        #   For brevity, just check the first parsed_flight .
        self.assertEqual(str(type(parsed_flights.parsed_flights[0])), "<class 'flight_parsing.Flight'>")

    def test_to_dataframe(self):
        parsed_flights = ParsedFlights(self.batch_info)
        flight_df = parsed_flights.to_dataframe()
        self.assertEqual(len(flight_df), len(self.batch_info))
        self.assertEqual(list(flight_df.columns), Flight.labels())
        #print(flight_df.head())

if __name__ == '__main__':
   unittest.main()