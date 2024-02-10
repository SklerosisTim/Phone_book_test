import json


class PhoneBook:
    def __init__(self):
        self.json = 'phone_book.json'
        self.book = self.json_read()
        self.menu_options = {'add': self.add_info,
                             'list': self.print_book}

    def json_read(self) -> dict:  # получение словаря справочника из json
        with open(self.json, 'r', encoding='utf-8') as file:
            return json.load(file)

    def json_write(self, full_name, inf_dict):  # запись новой информации в json
        self.book[full_name] = inf_dict
        with open(self.json, 'w', encoding='utf-8') as file:
            json.dump(self.book, file, indent=2, ensure_ascii=False)

    @staticmethod
    # словарь персональной информации для записи в json
    def person_info(name: str, company: str, work_phone: str, pers_phone: str) -> dict:
        return {'Фамилия': name.split()[0],
                'Имя': name.split()[1],
                'Отчество': name.split()[2],
                'Организация': company,
                'Рабочий телефон': work_phone,
                'Личный телефон': pers_phone}

    def add_info(self):  # запрос на ввод новой информации и ее запись в справочник
        name = input('Введите Фамилию, Имя, Отчество через пробел: ').title()
        company = input('Введите название организации: ').title()
        work_phone = input('Введите номер рабочего телефона: ')
        pers_phone = input('Введите номер личного телефона: ')
        self.json_write(name, self.person_info(name, company, work_phone, pers_phone))
        self.command()

    def menu(self):  # стартовое меню с запросом команд
        print()
        print('ТЕЛЕФОННЫЙ СПРАВОЧНИК')
        print('Список команд:')
        print('list = вывод справочника')
        print('add = добавление новой записи')
        print('edit = редактирование существующей записи')
        print('search = поиск записи')
        print('q = закрыть программу')
        self.command()

    def command(self):  # ввод команды, ее распознавание и реализация
        print()
        comm = input('Введите команду: ')
        if comm in self.menu_options:
            self.menu_options[comm]()
        elif comm == 'q':
            return
        else:
            print('Команда введена неверно, повторите пожалуйста: ')
            self.command()

    def print_book(self):  # вывод справочника в консоль
        inform = 'Организация', 'Рабочий телефон', 'Личный телефон'
        for pers, value in self.book.items():
            print()
            print(pers)
            for inf in inform:
                print(inf, ':', value[inf], end='    ')
            print()
        self.command()


if __name__ == '__main__':
    book = PhoneBook()
    book.menu()
