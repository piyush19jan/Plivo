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
        client.verify_search_number_request(resp)
        print("################################ Completed test for search number ################################")

    @test(depends_on=[send_search_request])
    def buy_number_test():
        client = PlivoClient.PlivoClient()
        print("################################ Starting test for buy number ################################")
        headers = {
            "Authorization": "Basic TUFOSlJJT1ROSk9UTk1OWkMxT0Q6TkRWbU9UUTVNVFkyTW1Vek4yTmtPVFU0TW1SbVlqQXhNelV6TUdabA==", "Content-Type": "application/json"}
        resp = client.send_buy_number_request(headers)
        client.verify_buy_number_response(resp)
        print("################################ Ended test for buy number ################################")

    @test(depends_on=[buy_number_test])
    def make_outbound_call_test():
        print("################################ Starting test for making outbound calls ################################")
        client = PlivoClient.PlivoClient()
        headers = {
            "Authorization": "Basic TUFOSlJJT1ROSk9UTk1OWkMxT0Q6TkRWbU9UUTVNVFkyTW1Vek4yTmtPVFU0TW1SbVlqQXhNelV6TUdabA==", "Content-Type": "application/json"}
        response = client.make_outbound_call_request(headers)
        client.verify_make_outboud_call_response(response)
        print("################################ Ended test for making outbound calls ################################")

    @test(depends_on=[make_outbound_call_test])
    def make_get_live_call_test():
        print("################################ Starting test for getting live calls ################################")
        client = PlivoClient.PlivoClient()
        headers = {
            "Authorization": "Basic TUFOSlJJT1ROSk9UTk1OWkMxT0Q6TkRWbU9UUTVNVFkyTW1Vek4yTmtPVFU0TW1SbVlqQXhNelV6TUdabA=="}
        response = client.get_ongoing_live_calls(headers)
        client.verify_ongoing_live_call_response(response)
        print("################################ Ended test for getting live calls ################################")

    @test(depends_on=[make_get_live_call_test])
    def make_get_live_call_details_test():
        print("################################ Starting test for getting live call detials ################################")
        client = PlivoClient.PlivoClient()
        headers = {
            "Authorization": "Basic TUFOSlJJT1ROSk9UTk1OWkMxT0Q6TkRWbU9UUTVNVFkyTW1Vek4yTmtPVFU0TW1SbVlqQXhNelV6TUdabA=="}
        response = client.get_live_call_details(headers)
        client.verify_live_call_details_response(response)
        print("################################ Ended test for getting live call detials ################################")

TestProgram().run_and_exit()