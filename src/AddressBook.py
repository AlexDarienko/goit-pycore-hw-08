from collections import UserDict
from datetime import datetime, timedelta
import re
import pickle

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if self.is_valid(value):
            super().__init__(value)
        else:
            raise ValueError("Invalid phone number format. Use a 10-digit number.")
        
    def __str__(self):
        return self.value

    @staticmethod
    def is_valid(phone):
        return re.fullmatch(r'\d{10}', phone) is not None

class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, '%d.%m.%Y')
            super().__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def change_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone

    def find_phone(self, phone):
        return next((p for p in self.phones if p.value == phone), None)

    def add_birthday(self, birthday):
        try:
            self.birthday = datetime.strptime(birthday, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Incorrect date format, should be DD.MM.YYYY")

    def __str__(self):
        phones = '; '.join(p.value for p in self.phones)
        birthday = f", birthday: {self.birthday.value}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones}{birthday}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self, days=7):
        upcoming_birthdays = []
        today = datetime.now()
        for record in self.data.values():
            if record.birthday:
                birthday = datetime.strptime(record.birthday.value, '%d.%m.%Y')
                birthday_this_year = birthday.replace(year=today.year)
                if today <= birthday_this_year <= today + timedelta(days=days):
                    upcoming_birthdays.append(record)
        return upcoming_birthdays
    

