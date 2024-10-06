import json


class FilterModule(object):

    def filters(self):
        return {
            'json_to_list': self.json_to_list,
            'print_message': self.print_message
        }

    def print_message(self, msg):
        extended_message = 'extended ' + msg
        return extended_message

    def json_to_list(self, json_data):
        json_data = json.loads(json_data)
        json_list = []

        for item in json_data:
            json_list.append([item["name"], item["age"]])

        return json_list
