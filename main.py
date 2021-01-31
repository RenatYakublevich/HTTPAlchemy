import sys
import requests


class _Request:
    def __init__(self, url, **kwargs):
        self.url = url
        self.options = kwargs

    def send_request(self, type_request, type_return):
        """
        :param type_request: тип HTTP запроса
        :param type_return: тип возвращаемого значения -> response_items
        :return: метод возвращает ответ сервера на запрос
        """
        response = requests.request(type_request, self.url, **self.options)

        response_items = {
            'text' : response.text,
            'status_code' : response.status_code
        }
        return response_items[type_return]

class HTTPAlchemy:
    def __init__(self):
        self.request_items = dict()
        self.parameters = None
        self.count_presets = 0

    def menu(self):
        """
        Функция отвечает за UI навигацию пользователя
        """
        menu_list = [
            '1.Make a requests',
            '2.Save Preset',
            '3.Load Preset'
        ]
        unpacking_menu_items = '\n'.join(menu_list)
        menu_input = input(f"Hello!\n{unpacking_menu_items}\nWrite number: ")

        menu_items = {
            '1': [self.input_info_request, self.do_request],
            '2': [self.input_info_request, self.save_preset],
            '3': [self.load_preset, self.do_request]
        }
        try:
            [command() for command in menu_items[menu_input]]
        except KeyError:
            print('There is no such menu number!')

    def do_request(self):
        """
        Функция отвечает за инициализацию класса запроса и вывод результата
        """
        try:
            type_requests = self.parameters.split(' ')[0]
            url = self.parameters.split(' ')[1]
            type_return = self.parameters.split(' ')[2]
        except IndexError:
            print('Wrong format!')
            sys.exit()
        if self.request_items:
            request = _Request(url, **self.request_items)
        else:
            request = _Request(url)
        print(f'Server response:\n{request.send_request(type_requests, type_return)}')

    def input_info_request(self):
        """
        Функция отвечает за ввод данных пользователем
        """
        self.parameters = input('Enter the request type and link separated by a space and the type of the returned request (example - get https://www.google.com/ json): ')
        additional_arguments = input('Enter the parameters that you want to use when prompted, separated by a space(params, data, json, headers,none if you dont want to specify parameters): ')
        self.request_items = {}

        if additional_arguments.lower() != 'none':
            for argument in additional_arguments.split(' '):
                arg = input(f'Enter the {argument} of request: ')
                self.request_items[argument] = eval(arg)

    def save_preset(self):
        """
        Функция отвечает за сохранение пресета в файл presets.txt
        """
        with open('presets.txt','r',encoding='utf-8') as file:
            all_lines = [line.strip() for line in file]
            self.count_presets = len(list(filter(lambda x: x.startswith('Preset #'), all_lines)))

        with open('presets.txt','a',encoding='utf-8') as file:
            file.write(f'\nPreset #{self.count_presets + 1}\n')
            file.write('\n'.join([self.parameters]) + '\n')
            keys = [key for key in self.request_items.keys()]
            values = [value for value in self.request_items.values()]
            for count in range(len(self.request_items.keys())):
                file.write(f'{keys[count]}={values[count]} ')
        print('Preset saved!')

    def load_preset(self):
        """
        Функция отвечает за загрузку пресета из файла presets.txt
        У пресета есть 2 обязательных лайна: номер пресета(пример - Preset #1) и
        описание запроса(пример - get https://vk.com/ text)
        3 лайн не обязательный: необязательные аргументы(пример - params={'code':'run 1 + 2'})
        """
        number_preset = int(input('Write number preset: '))
        with open('presets.txt','r',encoding='utf-8') as file:
            all_lines = [line.strip() for line in file]
            try:
                count_line_info = all_lines.index(f'Preset #{number_preset}')
            except ValueError:
                print('Preset not found')
                sys.exit()
            self.parameters = all_lines[count_line_info + 1]
            try:
                request_items_line = all_lines[count_line_info + 2]
                for request_item in range(int(len(request_items_line.split('=')))):
                    self.request_items[request_items_line.split('=')[request_item]] = eval(request_items_line.split('=')[request_item + 1])
            except IndexError:
                pass


alchemy = HTTPAlchemy()
alchemy.menu()