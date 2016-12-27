import unittest

from proboscis import TestProgram
from proboscis import test

from Plivo.client import PlivoClient


class PlivoTest(unittest.TestCase):

    @test()
    def send_search_request():
        client = PlivoClient.PlivoClient()
        print("################################ Starting test for search number ################################")
        headers = {
            "Authorization": "Basic TUFOSlJJT1ROSk9UTk1OWkMxT0Q6TkRWbU9UUTVNVFkyTW1Vek4yTmtPVFU0TW1SbVlqQXhNelV6TUdabA=="}
        resp = client.send_search_number_request(headers)
        data = client.get_data_for_call_api(resp.content)
        api_id = data['api_id']
        number_details = data['objects'][1:2]
        client.verify_search_number_request(resp)

    @test()
    def buy_number_test():
        client = PlivoClient.PlivoClient()
        print("################################ Starting test for buy number ################################")
        headers = {
            "Authorization": "Basic TUFOSlJJT1ROSk9UTk1OWkMxT0Q6TkRWbU9UUTVNVFkyTW1Vek4yTmtPVFU0TW1SbVlqQXhNelV6TUdabA==", "Content-Type": "application/json"}
        resp = client.send_buy_number_request(headers)
        client.verify_buy_number_response(resp)

TestProgram().run_and_exit()