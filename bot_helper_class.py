import click
# import json
from collections import UserDict
from typing import List
import pickle


class Field:
    def __init__(self, value) -> None:
        self.value = value.title()

    def __str__(self) -> str:
        return f'{self.value}'


class Name(Field):
    pass

class Phone(Field):
    pass

class Record:
    def __init__(self, name: Name, phone:Phone = None) -> None:
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)

    def add_phone(self, phone) -> None:
        self.phones.append(phone)

    def change_command(self, phone, new_phone) -> None:
        self.phones.remove(phone)
        self.phones.append(new_phone)

    def del_phone(self, phone) -> None:
        self.phones.remove(phone)

    def __str__(self) -> str:
        return f'Contact {self.name}: Phones {self.phones}'


class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    # отсутствует файл
    @classmethod
    def read_file(self):
        try:
            with open("contacts.bin", "rb") as file:
                return pickle.load(file)
        except FileNotFoundError:
            return AddressBook()


    def write_file(self):
        with open('contacts.bin', 'wb') as file:
            pickle.dump(self, file)

# ошибка ввода
def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return """If you write command 'add' please write 'add name number'\nIf you write command 'change' please write 'change name number'\nIf you write command 'phone' please write 'phone name'"""
        except KeyError:
            return "..."

    return wrapper


@input_error
def help_command():
    help_list = [
        'help - output command, that help find command',
        'hello - output command "How can I help you?"',
        'add - add contact, use "add" "name" "number"',
        'change - change your contact, use "change" "name" "number"',
        'phone - use "phone" "name" that see number this contact',
        'show all - show all your contacts',
    ]
    return '\n'.join(help_list)


@input_error
def bye_command(*args):
    return "Good bye, see you soon"


@input_error
def hello_command(*args):
    return "How can I help You?\nIf you want to know what I can do write Help "


#создание контакта
@input_error
def add_phone(*args):
    name = Name(args[0])
    phone = Phone(args[1])
    contacts = AddressBook.read_file()

    if contacts.get(Name(args[0])):
        return 'This contact already exist'
    else:
        rec = Record(name, phone)
        contacts.add_record(rec)

    contacts.write_file()
    return f'Contact "{name}" add successfully'


#изменение контакта
@input_error
def change_command(*args):
    name = Name(args[0])
    phone = Phone(args[1])
    contacts = AddressBook.read_file()
    if contacts.get(name):
        contacts[name] = phone
    else:
        return f'No contact "{name}"'
    Record.write_file(contacts)
    return f"Contact '{name}' change successfully"

@input_error
def del_number(*args):
    name, phone = Name(args[0]), Phone(args[1])
    contacts = AddressBook.read_file()
    contacts[name.value].del_phone(phone.value)
    return f"Contact {name.value} has deleted successfully."

@input_error
def add_phone_command(*args):
    name = Name(args[0])
    contacts = AddressBook.read_file()
    if contacts.get(name):
        return '\t{:>20} : {:<12} '.format(name, contacts.get(name))
    else:
        return f'No contact "{name}"'

#отобразить все
def show_all(*args):
    contacts = AddressBook.read_file()
    result = []
    for name, record in contacts.items():
        result.append('\t{:>20} : {:<12} '.format(name, ','.join([str(p) for p in record.phones])))
    return '\n'.join(result)

#работа по командам
commands = {
    hello_command: ["hello", "hi"],
    add_phone: ["add", "new", "+"],
    add_phone_command: ["phone", "number"],
    show_all: ["show all", "show"],
    change_command: ["change"],
    bye_command: ["good bye", "bye", ".", "close", "exit"],
    help_command: ["help"],
    del_number: ["del", "delete", "-"]
    }

def command_parser(user_input):
    data = []
    command = ""
    for k, v in commands.items():
        if any([user_input.lower().startswith(i) for i in v]):
            command = k
            data = " ".join([user_input.replace(i, "") for i in v]).split()
    return command, data

def start_hello():
    return f"Hello, I'm a bot assistent.\nTo get started, write Hello"

@click.command()
def main():

    #начало программы
    while True:
        user_input = input(">>> ")
        command, data = command_parser(user_input)
        if command:
            print(command(*data))
            if command == bye_command:
                break
        else:
            print("Sorry, unknown command. Try again.")


if __name__ == "__main__":
    print(start_hello())
    main()