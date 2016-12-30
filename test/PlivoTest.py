import unittest
import json

from proboscis import TestProgram
from proboscis import test

from Plivo.client import PlivoClient


class PlivoTest(unittest.TestCase):

    @test()
    def send_search_request():
        client = PlivoClient.PlivoClient()
        print("########### Starting test for search number ###########")
        resp = client.send_search_number_request()
        client.verify_search_number_request(resp)
        print("########### Completed test for search number ###########")

    @test(depends_on=[send_search_request])
    def buy_number_test():
        client = PlivoClient.PlivoClient()
        print("########### Starting test for buy number ###########")
        resp = client.send_buy_number_request()
        client.verify_buy_number_response(resp)
        print("########### Ended test for buy number ###########")

    @test(depends_on=[buy_number_test])
    def make_outbound_call_test():
        print("########### Starting test for making outbound calls ###########")
        client = PlivoClient.PlivoClient()
        response = client.make_outbound_call_request()
        client.verify_make_outboud_call_response(response)
        print("########### Ended test for making outbound calls ###########")

    @test(depends_on=[make_outbound_call_test])
    def make_get_live_call_test():
        print("########### Starting test for getting live calls ###########")
        client = PlivoClient.PlivoClient()
        response = client.get_ongoing_live_calls()
        client.verify_ongoing_live_call_response(response)
        print("########### Ended test for getting live calls ###########")

    @test(depends_on=[make_get_live_call_test])
    def make_get_live_call_details_test():
        print("########### Starting test for getting live call detials ###########")
        client = PlivoClient.PlivoClient()
        response = client.get_live_call_details()
        client.verify_live_call_details_response(json.loads(response.content))
        print("########### Ended test for getting live call detials ###########")

TestProgram().run_and_exit()