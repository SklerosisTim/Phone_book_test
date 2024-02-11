import json


class PhoneBook:
    def __init__(self):
        self.json = 'phone_book.json'
        self.book = self.json_read()
        self.menu_options = {'a': self.add_info,
                             'l': self.print_book,
                             's': self.search,
                             'e': self.edit}
        self.category = ['Фамилия', 'Имя', 'Отчество', 'Организация', 'Рабочий телефон', 'Личный телефон']

    def json_read(self) -> dict:  # получение словаря справочника из json
        with open(self.json, 'r', encoding='utf-8') as file:
            return json.load(file)

    def json_write(self, inf_dict, person_id=None):  # запись информации в json
        pers_id = self.new_pers_id() if not person_id else person_id
        self.book[pers_id] = inf_dict
        with open(self.json, 'w', encoding='utf-8') as file:
            json.dump(self.book, file, indent=2, ensure_ascii=False)

    def new_pers_id(self) -> int:  # генерация нового ID
        num = 0
        while num in [int(key) for key in self.book.keys()]:
            num += 1
        else:
            return num

    def choice_category(self, option: str) -> list:  # выбор категорий для поиска или редактирования
        for num, cat in enumerate(self.category):
            print(num, '=', cat)
        category_index = (input(f'Выберите категории для {option} (через пробел): ')).split()  # список индексов 0-5
        return [self.category[int(num)] for num in category_index]

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
        print('ДОБАВЛЕНИЕ')
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
        print('l = [list] Вывод справочника')
        print('a = [add] Добавление новой записи')
        print('e = [edit] Редактирование существующей записи')
        print('s = [search] Поиск записи')
        print('q = [quit] Закрыть программу')
        self.command()

    def command(self):  # ввод команды, ее распознавание и реализация
        print()
        comm = input('Введите команду: ').lower()
        if comm in self.menu_options:
            self.menu_options[comm]()
        elif comm == 'q':
            return
        else:
            print('Команда введена неверно, повторите пожалуйста: ')
            self.command()

    def print_person_info(self, pers_id):  # вывод одной записи, принимает ID
        pers = self.book[pers_id]
        print(pers['Фамилия'], pers['Имя'], pers['Отчество'], '    id:', pers_id)
        for inf in self.category[3:]:
            print('    ', inf, ':', pers[inf], end='    ')
        print()

    def print_book(self, id_filters: list | None = None):  # вывод справочника в консоль
        print()
        if not id_filters:  # если не передан список ID, вывод всего телефонного справочника
            for key in self.book.keys():
                self.print_person_info(key)
        else:  # если передан список ID, вывод только запрашиваемых записей
            for num in id_filters:
                self.print_person_info(num)
        self.command()

    def find_id(self, find: tuple) -> list:  # принимает кортеж (категория, значение), возвращает список найденных ID
        return [key for key, value in self.book.items() if value[find[0]] == find[1]]

    def search(self):  # поиск
        finding_id = []
        print('ПОИСК')
        category_names = self.choice_category('поиска')  # запрос категорий поиска
        for cat in category_names:
            value = input(f'>{cat}< Введите искомое значение: ').title()  # принимаем значение по каждой категории
            if not finding_id:  # если список ID еще пуст - добавляем в него новые найденные ID
                finding_id += self.find_id((cat, value))
            else:  # если ID уже есть, сравниваем их с новыми, и оставляем только те, что есть в обоих списках
                finding_id = set(finding_id) & set(self.find_id((cat, value)))
        if finding_id:  # вывод результата если он есть
            print('Результат поиска:')
            self.print_book(finding_id)
        else:
            print('Искомые значения не найдены!')
            self.command()

    def edit(self):  # редактирование
        print('РЕДАКТИРОВАНИЕ')
        edit_id = input('Введите ID записи, которую хотите отредактировать: ')  # запрос ID записи
        self.print_person_info(edit_id)
        category_names = self.choice_category('редактирования')  # запрос категорий
        for cat in category_names:  # запрос/запись нового значения для каждой категории
            value = input(f'>{cat}< Старое значение: {self.book[edit_id][cat]}    Введите новое значение: ').title()
            self.book[edit_id][cat] = value
        self.print_person_info(edit_id)
        self.json_write(self.book[edit_id], edit_id)
        self.command()


if __name__ == '__main__':
    book = PhoneBook()
    book.menu()
