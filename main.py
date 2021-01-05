import requests


class _Request:
    def __init__(self, url, **kwargs):
        self.url = url
        self.options = kwargs

    def do_request(self, type_request):
        """
        :param type_request: тип HTTP запроса
        :return: метод возвращает текст запроса
        """
        response = requests.request(type_request, self.url, **self.options)
        return response.text

class HTTPAlchemy:
    def __init__(self):
        pass

    @staticmethod
    def menu():
        menu_items = [
            '1 - make a requests'
        ]
        unpacking_menu_items = '\n'.join(menu_items)
        menu_input = input(f"Hello!\n{unpacking_menu_items}\nWrite number: ")

        menu = {
            '1' : HTTPAlchemy.do_request
        }
        try:
            menu[menu_input]()
        except KeyError:
            print('There is no such menu number!')

    @staticmethod
    def do_request():
        while True:
            url_and_type = input('Enter the request type and link separated by a space (example - get https://www.google.com/): ')

            try:
                type_requests = url_and_type.split(' ')[0]
                url = url_and_type.split(' ')[1]
            except IndexError:
                print('Wrong format!')

            additional_arguments = input('Enter the parameters that you want to use when prompted, separated by a space(params, data, json, headers,none if you dont want to specify parameters): ')
            request_items = {}

            if additional_arguments != 'none':
                for argument in additional_arguments.split(' '):
                    arg = input(f'Enter the {argument} of request: ')
                    request_items[argument] = eval(arg)

            request = _Request(url, **request_items)
            print(f'Server response:\n{request.do_request(type_requests)}')



http_alchemy = HTTPAlchemy()
http_alchemy.menu()


