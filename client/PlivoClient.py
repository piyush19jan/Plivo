import requests
import json
import os
import re
import base64
from numbers import Number
import time

class PlivoClient():

    search_url = "https://api.plivo.com/v1/Account/{auth_id}/PhoneNumber/?country_iso=US"
    buy_url = "https://api.plivo.com/v1/Account/{auth_id}/PhoneNumber/{number}/"
    call_url = "https://api.plivo.com/v1/Account/{auth_id}/Call/"
    live_calls_url = "https://api.plivo.com/v1/Account/{auth_id}/Call/"
    live_call_details_url = "https://api.plivo.com/v1/Account/{auth_id}/Call/{call_uuid}/"

    def __init__(self):
        fileDir = os.path.dirname(os.path.realpath('__file__'))
        filename = os.path.join(fileDir, '../resource/config.json')
        filename = os.path.abspath(os.path.realpath(filename))
        with open(filename) as data_file:
            self.data = json.load(data_file)
        self.encodedString = base64.b64encode(str.encode(self.data['auth_id']+":"+self.data['auth_token']))
        self.encodedString = str(self.encodedString, 'utf-8')
        self.header = {
            "Authorization": "Basic " + self.encodedString
        }

    def set_numbers(self, numbers):
        global number1
        global number2
        number1 = numbers[0]
        number2 = numbers[1]

    def get_numbers(self, number):
        if number == 1:
            return number1
        else:
            return number2

    def send_search_number_request(self):
        search_url = self.search_url.replace("{auth_id}", self.data['auth_id'])
        response = requests.get(search_url, headers=self.header)
        print(response.status_code)
        print(response.json)
        return response

    def verify_search_number_request(self, response):
        assert response.status_code == 200
        resp = response.content
        print(resp)
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

    def send_buy_number_request(self):
        buy_url1 = self.buy_url.replace("{number}", self.get_numbers(1)).replace("{auth_id}", self.data['auth_id'])
        buy_url2 = self.buy_url.replace("{number}", self.get_numbers(2)).replace("{auth_id}", self.data['auth_id'])
        self.header.update({"Content-Type": "application/json"})
        response1 = requests.post(buy_url1, headers=self.header)
        response2 = requests.post(buy_url2, headers=self.header)
        resp_dict = {"response1": response1, "response2": response2}
        return resp_dict

    def verify_buy_number_response(self, response):
        pattern = "^[a-zA-Z0-9-]*$"
        assert response['response1'].status_code == 201
        assert response['response2'].status_code == 201
        resp_data1 = json.loads(response['response1'].content)
        resp_data2 = json.loads(response['response2'].content)
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

    def make_outbound_call_request(self):
        call_url = self.call_url.replace("{auth_id}", self.data['auth_id'])
        payload = {}
        payload['from'] = self.get_numbers(1)
        payload['to'] = self.get_numbers(2)
        payload['answer_url'] = "https://s3.amazonaws.com/plivosamplexml/speak_url.xml"
        payload_json = json.dumps(payload)
        self.header.update({"Content-Type": "application/json"})
        response = requests.post(call_url, data=payload_json, headers=self.header)
        return response

    def verify_make_outboud_call_response(self, response):
        pattern = "^[a-zA-Z0-9-]*$"
        assert response.status_code == 201
        resp_data = json.loads(response.content)
        assert resp_data['message'] == 'call fired'
        assert re.match(pattern, resp_data['request_uuid'])

    def get_ongoing_live_calls(self):
        live_call_url = self.live_calls_url.replace("{auth_id}", self.data['auth_id'])
        response = requests.get(live_call_url, headers=self.header)
        return response

    def verify_ongoing_live_call_response(self, response):
        pattern = "^[+0-9-]*$"
        global call_uuid
        assert response.status_code == 200
        resp_data = json.loads(response.content)
        assert len(resp_data['objects']) > 0
        assert resp_data['meta']['total_count'] == len(resp_data['objects'])
        call_uuid = resp_data['objects'][0]['call_uuid']
        call_detail = resp_data['objects']
        for data in call_detail:
            self.verify_live_call_details_response(data)

    def get_live_call_details(self):
        live_call_detail_url =self.live_call_details_url.replace("{auth_id}", self.data['auth_id']).replace("{call_uuid}", call_uuid)
        print(live_call_detail_url)
        response = requests.get(live_call_detail_url, headers=self.header)
        return response

    def verify_live_call_details_response(self, response):
        pattern = "^[+0-9-]*$"
        assert isinstance(response['bill_duration'], Number)
        assert isinstance(response['billed_duration'], Number)
        assert isinstance(response['call_duration'], Number)
        assert response['call_direction'] == 'inbound' or response['call_direction'] == 'outbound'
        assert response['call_uuid'] in response['resource_uri']
        assert re.match(pattern, response['from_number'])
        assert re.match(pattern, response['to_number'])
        time.strptime(response['answer_time'].split('+')[0], '%Y-%m-%d %H:%M:%S')
        time.strptime(response['initiation_time'].split('+')[0], '%Y-%m-%d %H:%M:%S')
        time.strptime(response['end_time'].split('+')[0], '%Y-%m-%d %H:%M:%S')
        assert isinstance(float(response['total_amount']), Number)
        assert isinstance(float(response['total_rate']), Number)





