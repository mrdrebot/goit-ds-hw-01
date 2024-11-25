from functools import wraps
from typing import Callable
from classes_library import AddressBook, Record
import pickle

def parse_input(user_input: str) -> tuple:
    cmd, *args = user_input.split()
    cmd: str = cmd.strip().lower()
    return cmd, *args

def input_error(func: Callable[[tuple], Callable[[tuple], tuple]]) -> Callable[[tuple], Callable[[tuple], tuple]]:
    @wraps(func)
    def inner(*args: tuple) ->  Callable[[tuple], Callable[[tuple], tuple]]:
        try:
            return func(*args)
        except ValueError as e:
            return f"Error: { e }"
        except KeyError as e:
            return f"Error: { e }"
        except IndexError as e:
            return f"Error: { e }"

    return inner

@input_error
def add_contact(args: list, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)

    if record and record.find_phone(phone):
        raise KeyError("Entered name and number are already exists. Change name or check entered phone number!")

    if record is None:
        record = Record(name)
        book.add_record(record)
        record.add_phone(phone)
        message: str = "Contact added."
    else:
        record.add_phone(phone)
        message: str = "Contact updated."

    return message

@input_error
def change_contact(args: list, book: AddressBook):
    name, old_phone, new_phone, *_  = args
    record = book.find(name)

    if record is None:
        raise KeyError("Entered name hasn't find in base!")
    else:
        record.edit_phone(old_phone, new_phone)
        return "Contact changed."

@input_error
def show_phone(args: list, book: AddressBook):  
    name, *_ = args
    record = book.find(name)

    if record is None:
        raise KeyError("Entered name hasn't find in base!")
    else:
        return ';\n'.join(phone.value for phone in record.phones)

@input_error
def show_all(book: AddressBook):
    if not book:
        raise ValueError("The base is empty!")

    return book

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday, *_ = args
    record = book.find(name)

    if record is None:
        raise KeyError("Entered name hasn't find in base!")
    elif record.birthday:
        raise KeyError("The data in field birthday is already exist. Use another command to change birthday date!")
    else:
        record.add_birthday(birthday)
        return "Birthday added." 

@input_error
def show_birthday(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)

    if record is None:
        raise KeyError("Entered name hasn't find in base!")
    else:
        return record.birthday

@input_error
def birthdays(book: AddressBook):
    return book.get_upcoming_birthdays()
    
filename = "book_database.pkl"

def read_book_from_file(filename):
    try:
        with open(filename, "rb") as base:
            return pickle.load(base)
    except FileNotFoundError  as e:
        print(f"{ e }\nThe base has not found! Create the new base.")
        return AddressBook()

def write_book_to_file(filename, book: AddressBook):
    with open(filename, "wb") as base:
        pickle.dump(book, base)
      
def main():
    book = read_book_from_file(filename)
    print("Welcome to the assistant bot!")

    while True:
        try:
            user_input: str = input("Enter a command: ")
            command, *args = parse_input(user_input)

            match command:
                case "close" | "exit":
                    write_book_to_file(filename, book)
                    print("Good bye!")
                    break
                case "hello":
                    print("How can I help you?")
                case "add":
                    print(add_contact(args, book))
                case "change":
                    print(change_contact(args, book))
                case "phone":
                    print(show_phone(args, book))
                case "add-birthday":
                    print(add_birthday(args, book))
                case "show-birthday":
                    print(show_birthday(args, book))
                case "birthdays":
                    print(birthdays(book))
                case "all":
                    print(show_all(book))
                case _:
                    print("Invalid command. You can use this command: add, change, phone, all, close or exit!")
        except ValueError:
            print("Please, enter a command!")

if __name__ == "__main__":
    main()