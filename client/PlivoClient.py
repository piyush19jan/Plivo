import requests
import json
import os

class PlivoClient():

    search_url = "https://api.plivo.com/v1/Account/MANJRIOTNJOTNMNZC1OD/PhoneNumber/?country_iso=US"
    buy_url = "https://api.plivo.com/v1/Account/{auth_id}/PhoneNumber/{number}/"

    def __init__(self):
        fileDir = os.path.dirname(os.path.realpath('__file__'))
        filename = os.path.join(fileDir, '../resource/config.json')
        filename = os.path.abspath(os.path.realpath(filename))
        with open(filename) as data_file:
            self.data = json.load(data_file)

    def set_numbers(self, numbers):
        global number1
        global number2
        number1= numbers[0]
        number2 = numbers[1]

    def get_numbers(self, number):
        if number == 1:
            return number1
        else:
            return number2

    def send_search_number_request(self, headers):
        response = requests.get(self.search_url, headers=headers)
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
        print(self.get_numbers(1))
        print(self.get_numbers(2))
        return data_dict

    def get_data_for_call_api(self, response):
        data_dict = json.loads(response)
        return data_dict

    def send_buy_number_request(self, headers):
        buy_url1 = self.buy_url.replace("{number}", self.get_numbers(1)).replace("{auth_id}", self.data['auth_id'])
        buy_url2 = self.buy_url.replace("{number}", self.get_numbers(2)).replace("{auth_id}", self.data['auth_id'])
        response1 = requests.post(buy_url1, headers=headers)
        response2 = requests.post(buy_url2, headers=headers)
        print(response1.status_code)
        print(response1.json())
        print(response2.status_code)
        print(response2.json())

    def verify_buy_number_response(self, response):
        assert response.status_code == 201
