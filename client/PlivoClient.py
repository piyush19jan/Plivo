import requests
import json
import os
import re

class PlivoClient():

    search_url = "https://api.plivo.com/v1/Account/{auth_id}/PhoneNumber/?country_iso=US"
    buy_url = "https://api.plivo.com/v1/Account/{auth_id}/PhoneNumber/{number}/"
    call_url = "https://api.plivo.com/v1/Account/{auth_id}/Call/"
    live_calls_url = "https://api.plivo.com/v1/Account/{auth_id}/Call/?status=live"
    live_call_details_url = "https://api.plivo.com/v1/Account/{auth_id}/Call/{call_uuid}/?status=live"

    def __init__(self):
        fileDir = os.path.dirname(os.path.realpath('__file__'))
        filename = os.path.join(fileDir, '../resource/config.json')
        filename = os.path.abspath(os.path.realpath(filename))
        with open(filename) as data_file:
            self.data = json.load(data_file)

    def set_numbers(self, numbers):
        global number1
        global number2
        number1 = "18883964261"
        number2 = "18883424094"

    def get_numbers(self, number):
        if number == 1:
            return number1
        else:
            return number2

    def send_search_number_request(self, headers):
        search_url = self.search_url.replace("{auth_id}", self.data['auth_id'])
        response = requests.get(search_url, headers=headers)
        print(response.status_code)
        print(response.json)
        return response

    def verify_search_number_request(self, response):
        assert response.status_code == 200
        resp = response.content
        data_dict = json.loads(resp)
        number_list = data_dict['objects'][0:2]
        numbers = []
        for number_object in number_list:
            numbers.append(number_object['number'])
            assert number_object['country'] == 'UNITED STATES'
            assert number_object['region'] == 'United States'
            assert len(number_object['resource_uri']) > 0
        self.set_numbers(numbers)
        return data_dict

    def get_data_for_call_api(self, response):
        data_dict = json.loads(response)
        return data_dict

    def send_buy_number_request(self, headers):
        buy_url1 = self.buy_url.replace("{number}", self.get_numbers(1)).replace("{auth_id}", self.data['auth_id'])
        buy_url2 = self.buy_url.replace("{number}", self.get_numbers(2)).replace("{auth_id}", self.data['auth_id'])
        response1 = requests.post(buy_url1, headers=headers)
        response2 = requests.post(buy_url2, headers=headers)
        resp_dict = {"response1": response1, "response2": response2}
        return resp_dict

    def verify_buy_number_response(self, response):
        pattern = "^[a-zA-Z0-9-]*$"
        assert response['response1'].status_code == 201
        assert response['response2'].status_code == 201
        resp_data1 = json.loads(response['response1'])
        resp_data2 = json.loads(response['response1'])
        assert resp_data1['message'] == 'created'
        assert resp_data1['status'] == 'fulfilled'
        assert resp_data1['numbers'][0]['number'] == self.get_numbers(1)
        assert resp_data1['numbers'][0]['status'] == 'Success'
        assert re.match(pattern, resp_data1['api_id'])
        assert resp_data2['message'] == 'created'
        assert resp_data2['status'] == 'fulfilled'
        assert resp_data2['numbers'][0]['number'] == self.get_numbers(2)
        assert resp_data2['numbers'][0]['status'] == 'Success'
        assert re.match(pattern, resp_data2['api_id'])

    def make_outbound_call_request(self, headers):
        call_url = self.call_url.replace("{auth_id}", self.data['auth_id'])
        payload = {}
        payload['from'] = "18883964261"
        payload['to'] = "18883424094"
        payload['answer_url'] = "https://s3.amazonaws.com/plivosamplexml/speak_url.xml"
        payload_json = json.dumps(payload)
        response = requests.post(call_url, data=payload_json, headers=headers)
        return response

    def verify_make_outboud_call_response(self, response):
        pattern = "^[a-zA-Z0-9-]*$"
        assert response.status_code == 201
        resp_data = json.loads(response)
        assert resp_data['message'] == 'call fired'
        assert re.match(pattern, resp_data['request_uuid'])

    def get_ongoing_live_calls(self, headers):
        live_call_url = self.live_calls_url.replace("{auth_id}", self.data['auth_id'])
        response = requests.get(live_call_url, headers=headers)
        return response

    def verify_ongoing_live_call_response(self, response):
        global call_uuid
        assert response.status_code == 200
        resp_data = json.loads(response)
        assert len(resp_data['calls']) > 0
        call_uuid = resp_data['calls'][0]
        print(call_uuid)

    def get_live_call_details(self, headers):
        live_call_detail_url =self.live_call_details_url.replace("{auth_id}", self.data['auth_id']).replace("{call_uuid}", call_uuid)
        print(live_call_detail_url)
        response = requests.get(live_call_detail_url, headers=headers)
        return response

    def verify_live_call_details_response(self, response):
        pattern = "^[a-zA-Z0-9-]*$"
        assert response.status_code == 200
        resp_data = json.loads(response)
        assert resp_data['direction'] == 'inbound'
        assert resp_data['from'] == self.get_numbers(1)
        assert resp_data['to'] == self.get_numbers(2)
        assert resp_data['call_status'] == 'in-progress'
        assert re.match(pattern, resp_data['api_id'])
        assert resp_data['caller_name'] == "+" + self.get_numbers(1)
        assert re.match(pattern, resp_data['call_uuid'])





