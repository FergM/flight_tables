from datetime import datetime, timedelta
import json
import unittest

from flight_tables.heathrow_parsing import extract_batch_heathrow, extract_flight_heathrow, fetch_heathrow_data

class SampleData(object):
    
    def __init__(self):
      
        self.raw_flight_1 = json.loads(r'''{"flightIdentifier":"OS8237","flightNumber":"8237","airlineIataRef":"OS","origin":{"airportIataRef":"LHR","terminalCode":"2","status":{"interpretedStatus":" Departed 15:15  ","category":"INFO","messages":{"message":[{"text":"Departed","data":"15:15"},{"text":" "}]},"code":"AB","statusTime":"2020-01-30T15:15:00.000Z"},"scheduledDateTime":{"utc":"2020-01-30T14:30:00.000","local":"2020-01-30T14:30:00.000","utcOffset":0}},"destination":{"airportIataRef":"YYC"},"stops":{"stop":[],"count":0},"codeShareType":"CODESHARE_OPERATING_FLIGHT","isHadacabCancelled":false}''')
        self.raw_flight_2 = json.loads(r'''{"flightIdentifier":"AC6186","flightNumber":"6186","airlineIataRef":"AC","origin":{"airportIataRef":"LHR","terminalCode":"2","status":{"interpretedStatus":" Departed 06:26  ","category":"INFO","messages":{"message":[{"text":"Departed","data":"06:26"},{"text":" "}]},"code":"AB","statusTime":"2020-02-14T06:26:00.000Z"},"scheduledDateTime":{"utc":"2020-02-14T06:00:00.000","local":"2020-02-14T06:00:00.000","utcOffset":0}},"destination":{"airportIataRef":"VIE"},"stops":{"stop":[],"count":0},"codeShareType":"CODESHARE_MARKETING_FLIGHT","isHadacabCancelled":false}''')
        self.raw_flight_3 = json.loads(r'''{"flightIdentifier":"BA7008","flightNumber":"7008","airlineIataRef":"BA","origin":{"airportIataRef":"LHR","terminalCode":"4","status":{"interpretedStatus":" Cancelled Contact airline","category":"INFO","messages":{"message":[{"text":"Cancelled"},{"text":"Contact airline"}]},"code":"CX","statusTime":"2020-01-30T15:05:00.000Z"},"scheduledDateTime":{"utc":"2020-01-30T15:05:00.000","local":"2020-01-30T15:05:00.000","utcOffset":0}},"destination":{"airportIataRef":"DOH"},"stops":{"stop":[],"count":0},"codeShareType":"NORMAL_FLIGHT","isHadacabCancelled":false}''')
        #^ 3 is a Cancelled Flight

        self.raw_flight_list = [self.raw_flight_1, self.raw_flight_2, self.raw_flight_3]

        mock_response = {} # is formatted like: {"flightSummaryList": {"flight":[]}}
        mock_response['flightSummaryList'] = {}
        mock_response['flightSummaryList']['flight'] = self.raw_flight_list
        self.mock_response = mock_response

        self.flight_info_1 =   {'actual_datetime': datetime(2020, 1, 30, 15, 15),
                                        'code_share_type': 'main_code',
                                        'destination': 'YYC',
                                        'flight_id': 'OS8237',
                                        'origin': 'LHR',
                                        'scheduled_datetime': datetime(2020, 1, 30, 14, 30),
                                        'status': 'Departed'}

        self.flight_info_2 =   {'actual_datetime': datetime(2020, 2, 14, 6, 26),
                                        'code_share_type': 'alt_code',
                                        'destination': 'VIE',
                                        'flight_id': 'AC6186',
                                        'origin': 'LHR',
                                        'scheduled_datetime': datetime(2020, 2, 14, 6, 0),
                                        'status': 'Departed'}

        # A Cancelled Flight
        self.flight_info_3 =  {'actual_datetime': None,
                                        'code_share_type': 'no_codeshare',
                                        'destination': 'DOH',
                                        'flight_id': 'BA7008',
                                        'origin': 'LHR',
                                        'scheduled_datetime': datetime(2020, 1, 30, 15, 5),
                                        'status': 'Cancelled'}

        self.mock_parsed_flights = [self.flight_info_1, self.flight_info_2, self.flight_info_3]

class TestHeathrowFlight(unittest.TestCase):
    def setUp(self):
        self.raw_flight_list = SampleData().raw_flight_list

    def test_flights(self):
        for i, raw_flight in enumerate(self.raw_flight_list):
            flight_info = extract_flight_heathrow(raw_flight)
            with self.subTest(list_position=i, flight_id = flight_info["flight_id"]):
                self.flight_validation(flight_info)

    def flight_validation(self, flight_info):
        codeshare_types = ["alt_code", "main_code", "no_codeshare"]
        status_types = [ "Landed", "Departed", "Cancelled"]
        actual_datetime_types = (datetime, type(None))
        self.assertIsInstance(flight_info["scheduled_datetime"], datetime)
        self.assertIsInstance(flight_info["actual_datetime"], actual_datetime_types)
        if type(flight_info["actual_datetime"]) == datetime:
            self.assertEqual(flight_info["actual_datetime"].tzinfo, None)
        self.assertEqual(flight_info["scheduled_datetime"].tzinfo, None)

        self.assertIsInstance(flight_info["origin"], str)
        self.assertIsInstance(flight_info["destination"], str)
        self.assertTrue(len(flight_info["origin"]), 3)
        self.assertTrue(len(flight_info["destination"]), 3)
        
        self.assertIsInstance(flight_info["flight_id"], str) # Can extend to check start is letter and end is number.
        self.assertIn(flight_info["code_share_type"], codeshare_types)
        
        self.assertIn(flight_info["status"], status_types)

class TestHeathrowBatch(unittest.TestCase):
    """Test the function called `extract_flight_heathrow`"""

    def setUp(self):
        self.mock_response = SampleData().mock_response
        self.expected_parsed_flights = SampleData().mock_parsed_flights

    def test_batch_extractor(self):
        self.parsed_flights = extract_batch_heathrow(self.mock_response)

        self.assertIsInstance(self.parsed_flights, list)
        self.assertEqual(len(self.parsed_flights), 3)

        self.assertEqual(self.parsed_flights, self.expected_parsed_flights)

class TestAPICaller(unittest.TestCase):
    
    def test_api_endpoint(self):
        """Note this test is dynamic:
                i.e. uses """
        yesterday = datetime.today() - timedelta(days=1)
        yesterday_str = yesterday.strftime('%Y-%m-%d')

        response = fetch_heathrow_data(yesterday_str, "arrivals")

        raw_flights_list = response["flightSummaryList"]["flight"]

        self.assertNotEqual(len(raw_flights_list), 0)

if __name__ == '__main__':
   unittest.main()
