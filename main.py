from classes import AddressBook, Record
import pickle


def input_error(func):
    """Error handling."""

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Enter correct data."
        except IndexError:
            return "Enter correct data."

    return inner


@input_error
def add_birthday(args, book: AddressBook):
    """Adding a birthday."""
    name, birthday = args
    record = book.find(name)
    if not record:
        record = Record(name)
        book.add_record(record)
    record.add_birthday(birthday)
    return f"Birthday {name} - {birthday} added."


@input_error
def add_contact(args, book: AddressBook):
    """Adding a contact."""
    name, phone = args
    record = book.find(name)
    if not record:
        record = Record(name)
        book.add_record(record)
    record.add_phone(phone)
    return f"Contact {name} with phone - {phone} added."


@input_error
def birthdays(book: AddressBook):
    """Bringing birthdays forward by 7 days."""
    return book.get_upcoming_birthdays()


@input_error
def change_contact(args, book: AddressBook) -> str:
    """Overwriting a contact"""
    name, old_phone, new_phone = args
    record = book.find(name)
    if not record:
        return f"{name} not found."
    else:
        record.edit_phone(old_phone, new_phone)
        return f"Contact {name} changed his old number {old_phone} to {new_phone} new number."


def load_data(filename="addressbook.pkl"):
    """Downloading from a file."""
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


def parse_input(user_input: str) -> tuple:
    """Command recognition"""
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def save_data(book, filename="addressbook.pkl"):
    """Writing to a file."""
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def show_all(book: AddressBook) -> str:
    """Output of all contacts!"""
    if book:
        return book
    else:
        return "There is no contact!"


@input_error
def show_birthday(args, book: AddressBook):
    """Date of birth by contact."""
    name = args[0]
    record = book.find(name)
    if not record:
        return f"Contact {name} not found."
    else:
        return record.birthday


@input_error
def show_phone(args, book) -> str:
    """Contact output by given name."""
    name = args[0]
    record = book.find(name)
    if not record:
        return f"Contact {name} not found."
    else:
        return ", ".join(str(phone) for phone in record.phones)


def main():
    """'The main program."""
    book = load_data()
    print("""Welcome to the assistant bot!""")
    while True:
        while True:
            user_input = input("Enter a command: ")
            if user_input:
                break
            else:
                
                print("You have not provided a command!")
        command, *args = parse_input(user_input)

        if command in ("close", "exit"):
            save_data(book)
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
