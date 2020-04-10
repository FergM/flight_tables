from datetime import datetime
from heathrow_parsing import Flight, ParsedFlights
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
    #Input: raw_flight
    #Output:
    #   flight_id (str): 
    #   origin (str): Airport Code
    #   destination (str): Airport Code
    #   status (str): Departed, Landed or Cancelled
    #   scheduled_datetime (datetime): Naive datetime
    #   actual_datetime (datetime): Naive datetime
    #   code_share_type (str): main_code, alt_code or only_code

    def setUp(self):
        self.raw_flight = SampleData().test_flight_departed_1

    def test_the_init(self):
        flight = Flight(self.raw_flight)
        self.assertIsInstance(flight.flight_id, str) #ToDO: assert regex string length >=0 with no whitespace.
        self.assertIsInstance(flight.scheduled_datetime, datetime)
        self.assertIsInstance(flight.actual_datetime, datetime)#Note: will return None and fail in some cases. 
        self.assertIn(type(flight.delay_mins), (float, type(None)))

    def test_to_list(self):

if __name__ == '__main__':
   unittest.main()