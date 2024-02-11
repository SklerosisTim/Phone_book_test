import json


class PhoneBook:
    def __init__(self):
        self.json = 'phone_book.json'
        self.book = self.json_read()
        self.menu_options = {'add': self.add_info,
                             'list': self.print_book,
                             'search': self.search}
        self.pers_id_numbers = []
        self.category = ['Фамилия', 'Имя', 'Отчество', 'Организация', 'Рабочий телефон', 'Личный телефон']

    def json_read(self) -> dict:  # получение словаря справочника из json
        with open(self.json, 'r', encoding='utf-8') as file:
            return json.load(file)

    def json_write(self, inf_dict):  # запись новой информации в json
        self.add_pers_id()
        self.book[self.pers_id_numbers[-1]] = inf_dict
        with open(self.json, 'w', encoding='utf-8') as file:
            json.dump(self.book, file, indent=2, ensure_ascii=False)

    def add_pers_id(self):  # добавление ID записи
        num = 0
        while num in self.pers_id_numbers:
            num += 1
        else:
            self.pers_id_numbers.append(num)

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
        self.json_write(self.person_info(name, company, work_phone, pers_phone))
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

    def print_person_info(self, dict_inf: dict):  # вывод одной записи
        inform = self.category[3:]
        print(dict_inf['Фамилия'], dict_inf['Имя'], dict_inf['Отчество'])
        for inf in inform:
            print('    ', inf, ':', dict_inf[inf], end='    ')
        print()

    def print_book(self, id_filters: list | None = None):  # вывод справочника в консоль
        print()
        if not id_filters:  # если не передан список ID, вывод всего телефонного справочника
            for pers in self.book.values():
                self.print_person_info(pers)
        else:  # если передан список ID, вывод только запрашиваемых записей
            for num in id_filters:
                self.print_person_info(self.book[num])
        self.command()

    # поиск по категории и значению, принимает кортеж (категория, значение), возвращает список найденных ID
    def find_id(self, find: tuple) -> list:
        return [key for key, value in self.book.items() if value[find[0]] == find[1]]

    def search(self):  # запрос категорий поиска, искомых значений по каждой из них, и вывод результата если он есть
        finding_id = []
        category = ['Фамилия', 'Имя', 'Отчество', 'Организация', 'Рабочий телефон', 'Личный телефон']
        for num, cat in enumerate(category):
            print(num, '=', cat)
        category_index = (input('Выберите категории поиска (через пробел): ')).split()  # список индексов 0-5
        category_names = [category[int(num)] for num in category_index]  # список самих категорий
        for cat in category_names:
            value = input(f'>{cat}< Введите искомое значение: ').title()  # принимаем значение по каждой категории
            if not finding_id:  # если список ID еще пуст - добавляем в него новые найденные ID
                finding_id += self.find_id((cat, value))
            else:  # если ID уже есть, сравниваем их с новыми, и оставляем только те, что есть в обоих списках
                finding_id = set(finding_id) & set(self.find_id((cat, value)))
        if finding_id:
            print('Результат поиска:')
            self.print_book(finding_id)
        else:
            print('Искомые значения не найдены!')
            self.command()


if __name__ == '__main__':
    book = PhoneBook()
    book.menu()
