import json


class PhoneBook:
    def __init__(self):
        self.json = 'phone_book.json'
        self.book = self.json_read()

    def json_read(self) -> dict:
        with open(self.json, 'r', encoding='utf-8') as file:
            return json.load(file)

    def json_write(self, full_name, inf_dict):
        self.book[full_name] = inf_dict
        with open(self.json, 'w', encoding='utf-8') as file:
            json.dump(self.book, file, indent=2, ensure_ascii=False)

    @staticmethod
    def person_info(name: str, company: str, work_phone: str, pers_phone: str) -> dict:
        return {'last_name': name.split()[0],
                'first_name': name.split()[1],
                'patronymic': name.split()[2],
                'company': company,
                'work_phone': work_phone,
                'pers_phone': pers_phone}

    def add_info(self):
        name = input('Введите Фамилию, Имя, Отчество через пробел: ')
        company = input('Введите название организации: ')
        work_phone = input('Введите номер рабочего телефона: ')
        pers_phone = input('Введите номер личного телефона: ')
        self.json_write(name, self.person_info(name, company, work_phone, pers_phone))


if __name__ == '__main__':
    book = PhoneBook()
    book.add_info()
