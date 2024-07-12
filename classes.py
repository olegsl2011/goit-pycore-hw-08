from collections import UserDict
from datetime import datetime, timedelta


class Field:
    """Base class for record fields."""

    def __init__(self, value: str):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    """Class for storing a contact name."""

    def __init__(self, value: str):
        if not value:
            raise ValueError
        else:
            super().__init__(value)


class Phone(Field):
    """Class for storing a phone number."""

    def __init__(self, value: str):
        if len(value) == 10 and value.isdigit():
            super().__init__(value)
        else:
            raise ValueError


class Birthday(Field):
    """Creating a birthday class"""

    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError


class Record:
    """Class for storing information about a contact, including name and phone list."""

    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    def find_phone(self, phone: str):
        for ph in self.phones:
            if ph.value == phone:
                return ph
        return None

    def remove_phone(self, phone: str) -> bool:
        ph = self.find_phone(phone)
        if ph:
            self.phones.remove(ph)
            return True
        else:
            return False

    def edit_phone(self, old_phone: str, new_phone: str) -> bool:
        if self.find_phone(old_phone):
            self.remove_phone(old_phone)
            self.add_phone(new_phone)
            return True
        else:
            raise ValueError

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value.capitalize()}, phones: {'; '.join(p.value for p in self.phones)}, Birthday: {self.birthday}"


class AddressBook(UserDict):
    """Class for storing and managing records."""

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str) -> Record:
        return self.data.get(name)

    def delete(self, name: str) -> bool:
        if name in self.data:
            del self.data[name]
            return True
        else:
            return False

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming_birthdays = []
        for name, record in self.data.items():
            if record.birthday:
                birthday_this_year = record.birthday.value.replace(year=today.year)
                if today <= birthday_this_year <= today + timedelta(days=7):
                    if birthday_this_year.isoweekday() == 6:
                        birthday_this_year += timedelta(days=2)
                    elif birthday_this_year.isoweekday() == 7:
                        birthday_this_year += timedelta(days=1)
                    upcoming_birthdays.append((name, birthday_this_year))
        if upcoming_birthdays:
            return '\n'.join(f'{name}: {datetime.strftime(birthday, '%d-%m-%Y')}' for name, birthday in upcoming_birthdays)
        else:
            return 'No upcoming birthdays next 7 days.'

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())


if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_birthday("25.02.2024")

    # Додавання запису John до адресної книги
    book.add_record(john_record)
    print(book.get_upcoming_birthdays())

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")
