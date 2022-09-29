"""Task 12...
Add the functionality of saving the address book to disk and restoring it from disk. 
To do this, you can choose any data serialization/deserialization protocol that is convenient 
for you and implement methods that will save all data to a file and load it from a file.
File: "ABook.data"

Add the ability to search the contents of the contact book to the user, so that all 
information about one or more users can be found by a few digits of the phone number 
or letters of the name, etc.
Command:
find ...
(where ... is a string(s) query? for examples: 
find 063
find 044 e_7 Dou 1988)
"""

from collections import UserDict
from datetime import datetime, timedelta
import os
import pickle
import re


def helper_try_open_file(path_file: str) -> str:
    """Checks if the database file exists and checks if the filename is free if not
    incoming: path_file is name of file
    return: name of file"""
    if os.path.isdir(path_file):
        while os.path.isdir(path_file):
            path_file = "new_one_" + path_file

    return path_file


class AddressBook(UserDict):

    def __str__(self):
        return f"AddressBook(Records:{self.data})"

    def add_record(self, record):
        self.data[record.name.value] = record

    def iterator(self, n_count: int):

        current_value = 0
        dictionary_iterator = iter(self.data)
        while current_value < len(self.data):
            volume = []
            for i in range(n_count):
                try:
                    volume.append(self.data[next(dictionary_iterator)])
                except StopIteration:
                    current_value = len(self.data)
            yield volume
            current_value += n_count


class Field:  # super for all base fields

    def __init__(self, value):
        self._value = None
        self.value = value

    def __str__(self):
        return f"{self.value}"

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value


class Name(Field):

    @Field.value.setter
    def value(self, new_value):
        if new_value[0] not in "_0123456789!@$%^&*()-+?<>~`|\\/":
            self._value = new_value
        else:
            print("At the beginning there can be only a Latin letter")


class Phone(Field):

    @Field.value.setter
    def value(self, new_value):
        if re.search(r'^\+[0-9)(-]{12,16}$', new_value):
            self._value = self.__preformating(new_value)
        else:
            print("Incorrect phone...")

    @staticmethod
    def __preformating(value: str) -> str:

        value = value.replace("-", "")
        if value[3] != "(":
            value = "(".join((value[: 3], value[3:]))
        if value[7] != ")":
            value = ")".join((value[: 7], value[7:]))

        return value


class Birthday(Field):

    @Field.value.setter
    def value(self, new_value):
        birthday_data = datetime.strptime(new_value, "%Y-%m-%d")
        if birthday_data:
            self._value = birthday_data
        else:
            print("Incorrect birthday...")

    def __str__(self):
        return f"{self.value.date()}"


class Record:

    def __init__(self, name, *phones):

        self.name = Name(name)
        self.phones = []
        self.birthday = None
        if phones:
            for phone in phones:
                self.add_phone(phone)

    def __str__(self):
        return f"Record(Name:{self.name}; Phones: {self.phones}; Birthday: {self.birthday})"

    def add_birthday(self, birthday):

        if not self.birthday:
            self.birthday = Birthday(birthday)
            return True,
        else:
            return False, f"Birthday already recorded for {self.name.value}. You can change it."

    def add_phone(self, phone_new):

        phone_new = Phone(phone_new)
        for phone in self.phones:
            if phone_new == phone.value:
                print(f"{phone_new} already recorded for {self.name.value}")
                return False

        self.phones.append(phone_new)

        return True

    def change_birthday(self, birthday):

        if not self.birthday:
            return False, f"Birthday not specified for {self.name.value}. You can add it."
        else:
            self.birthday = Birthday(birthday)

            return True,

    def change_phone(self, phone_to_change, phone_new):

        phone_to_change = Phone(phone_to_change).value
        phone_new = Phone(phone_new).value
        verdict = False

        for phone in self.phones:

            if phone.value == phone_new:
                return False, f"{phone_new} already recorded for {self.name.value}"

            if phone.value == phone_to_change:
                verdict = True

        if not verdict:
            return verdict, f"{phone_to_change} not specified in the contact {self.name.value}"

        for index, phone in enumerate(self.phones):
            if phone.value == phone_to_change:
                self.phones.remove(phone)
                self.phones.insert(index, Phone(phone_new))

                return True,

    def days_to_birthday(self):

        if self.birthday:
            user_day = datetime(year=datetime.now().date(
            ).year, month=self.birthday.value.month, day=self.birthday.value.day)
            days_left = user_day.date() - datetime.now().date()
            if days_left.days <= 0:
                user_day = datetime(year=datetime.now().date(
                ).year + 1, month=self.birthday.value.month, day=self.birthday.value.day)
                return (user_day.date() - datetime.now().date()).days
            return days_left.days

    def remove_phone(self, phone_to_remove):

        phone_to_remove = Phone(phone_to_remove).value
        for phone in self.phones:
            if phone.value == phone_to_remove:
                self.phones.remove(phone)
                return True

    def years_old(self):

        if self.birthday:
            full_years_old = datetime.now().date(
            ) + timedelta(days=self.days_to_birthday()) - self.birthday.value.date()
            return full_years_old.days//365


def validation_add(user_command, number_format, name):

    if not name:  # len(user_command) < 2:
        return "Give me name OR name and phone please\n"

    if name in contact_dictionary:
        return "Such an entry is already in the book. Add or change a number."

    if name[0].isdigit():
        return "A name cannot begin with a number!\n"

    elif not name[0].isalpha():
        return "The name can only begin with Latin characters!\n"

    if len(user_command) >= 2:
        for phone_candidate in user_command[2:]:
            if not re.search(number_format, phone_candidate):
                return "The number(s) is invalid.\nThe number must be in the following format with 12 digits(d): \
                +dd(ddd)ddd-dddd\n"


def validation_add_phone(user_command, number_format, name):

    if len(user_command) < 3:  # or not name:
        return "Give me name and new phone(s) please\n"

    if name[0].isdigit():
        return "A name cannot begin with a number!\n"

    elif not name[0].isalpha():
        return "The name can only begin with Latin characters!\n"

    for phone_candidate in user_command[2:]:
        if not re.search(number_format, phone_candidate):
            return "The number(s) is invalid.\nThe number must be in the following format with 12 digits(d):\
             +dd(ddd)ddd-dddd\n"


def validation_change(user_command, number_format, name):

    if not contact_dictionary:
        return "No contact records available. You can add records\n"

    if len(user_command) < 4:  # or not name:
        return "Give me name and 2 phones please (current and new)\n"

    if name[0].isdigit():
        return "A name cannot begin with a number!\n"

    elif not name[0].isalpha():
        return "The name can only begin with Latin characters!\n"

    if not re.search(number_format, user_command[2]):
        return "The number(s) is invalid: contains invalid characters or incorrect length\n \
        The number must be in the following format with 12 digits(d): +dd(ddd)ddd-dddd\n"


def validation_phone(_, name):

    if not contact_dictionary:
        return "No contact records available\n"

    if not name:  # len(user_command) < 2 or not name:
        return "Give me a name too, please\n"

    if name[0].isdigit():
        return "A name cannot begin with a number!\n"

    elif not name[0].isalpha():
        return "The name can only begin with Latin characters!\n"


def validation_show(user_command):

    if not contact_dictionary:
        return "No contact records available\n"

    if len(user_command) < 2:
        return "Give me a name, please\n"

    if user_command[1][0].isdigit():
        return "A name cannot begin with a number!\n"

    elif not user_command[1][0].isalpha():
        return "The name can only begin with Latin characters!\n"


def validation_birthday(user_command, name):

    if not contact_dictionary:
        return "No contact records available\n"

    if len(user_command) < 3:  # or not name:
        return "Give me a name and birthday, please\n"

    if name[0].isdigit():
        return "A name cannot begin with a number!\n"

    elif not name[0].isalpha():
        return "The name can only begin with Latin characters!\n"

    if 1900 > int(user_command[2].split("-")[0]) > datetime.now().year - 16:
        return "The year of birth is not correct!\n"
    else:
        try:
            datetime.strptime(user_command[2], "%Y-%m-%d")
        except ValueError:
            return "The calendar date is not possible!\n"


def input_error(handler):
    """User error handler
    incoming: handler (function)
    return: result(str) or exception_function(handler(user_command))"""
    # => user input command items in the list
    def exception_function(user_command):

        number_format = r'^\+[0-9)(-]{12,16}$'
        validation = None
        if len(user_command) > 1:
            name = user_command[1]
        else:
            name = None

        if handler.__name__ == "handler_showall" or handler.__name__ == "handler_find":
            if not contact_dictionary:
                return "No contact records available\n"
            if handler.__name__ == "handler_find" and not name:
                return "There is no search query\n"

        elif handler.__name__ == "handler_show":
            validation = validation_show(user_command)

        elif handler.__name__ == "handler_phone":
            validation = validation_phone(user_command, name)

        elif handler.__name__ == "handler_add_phone":
            validation = validation_add_phone(
                user_command, number_format, name)

        elif handler.__name__ == "handler_add_birthday":
            validation = validation_birthday(user_command, name)

        elif handler.__name__ == "handler_add":
            validation = validation_add(user_command, number_format, name)

        elif handler.__name__ == "handler_change_birthday":
            validation = validation_birthday(user_command, name)

        elif handler.__name__ == "handler_change":
            validation = validation_change(user_command, number_format, name)

        if validation:
            return validation

        try:
            result = handler(user_command)

        except KeyError as error:
            return f"An incorrect name was entered ({error}), not found in the book"

        except ValueError as error:
            return f"I don't know such commands ({error})"

        except IndexError as error:
            return f"No values in database ({error})"

        except Exception as error:
            return f"Something went wrong ({error})"

        if result is None:
            return "No contact record available..."

        return result

    return exception_function


@ input_error
def handler_phone(user_command: list) -> str:
    """"phone ...." With this command, the bot outputs the phone number for the specified
    contact to the console. Instead of ... the user enters the name of the contact
    whose number should be displayed.
    incoming: list of user command (name of user)
    return: phone number of user"""
    phones = ""
    name = user_command[1]
    for phone in (contact_dictionary[name]).phones:
        phones += f"{phone.value}; "

    return phones


@ input_error
def handler_change(user_command: list) -> str:  # list of str
    """"change ..." With this command, the bot stores the new phone number
    of the existing contact in memory. Instead of ... the user enters
    the name and phone numbers (current and new), necessarily with a space.
    incoming: list of user command (name of user)
    return: string"""
    name = user_command[1]
    current_phone = user_command[2]
    new_phone = user_command[3]
    verdict = contact_dictionary[name].change_phone(current_phone, new_phone)

    if verdict[0]:
        address_book_saver()
        return "The record has been updated\n"
    else:
        return f"No changes have been made\n{verdict[1]}"


@ input_error
def handler_add(user_command: list) -> str:
    """"add ...". With this command, the bot saves
    a new contact in memory (in the dictionary, for
    example). Instead of ... the user enters the name
    and phone number(s), necessarily with a space.
    incoming: list of user command (name of user)
    return: string"""
    name = user_command[1]
    new_record = Record(name)
    contact_dictionary.add_record(new_record)
    if len(user_command) > 2:
        phones = user_command[2:]
        verdict = False
        for new_phone in phones:
            verdict = contact_dictionary[name].add_phone(new_phone) or verdict
        if not verdict:
            return "There were no new entries to add\n"

    address_book_saver()
    return "A record(s) have been added\n"


@ input_error
def handler_add_phone(user_command: list) -> str:
    """"add ...". With this command, the bot saves
    a new phones to contact in memory (in the dictionary, for
    example). Instead of ... the user enters the name
    and phone number(s), necessarily with a space.
    incoming: list of user command (name of user)
    return: string"""
    name = user_command[1]
    phones = user_command[2:]
    verdict = False
    for new_phone in phones:
        verdict = contact_dictionary[name].add_phone(new_phone) or verdict
    if not verdict:
        return "There were no new entries to add\n"

    address_book_saver()
    return "A record have been added\n"


def handler_exit(_=None) -> str:
    return "Good bye!"


@ input_error
def handler_showall(_=None) -> list:
    """"show all". With this command, the bot outputs all saved
    contacts with phone numbers to the console.
    incoming: not_matter: any
    return: list of string of all users"""

    all_list = ["Entries in your contact book:"]
    for records in contact_dictionary.iterator(10):  # n_count from?
        volume = ""
        for record in records:
            if record.birthday:
                volume += f"\n\n{record.name}, birthday: {record.birthday} ({record.days_to_birthday()} \
                days to next birthday. Will be {record.years_old()} years old)\n-> phone(s): "
            else:
                volume += f"\n\n{record.name}, birthday: {record.birthday}\n-> phone(s): "
            for phone in record.phones:
                volume += f"{phone.value}; "
        all_list.append(volume)

    return all_list


def find_users(search_strings, record):
    """A simple function for to check if a record matches the search strings
    incoming: search_strings (list) strimg(s) for searching
    return: True or False, as a result of the search"""
    name = f"{record.name}"
    for search_string in search_strings:
        if name.find(search_string) >= 0:
            return True
        if record.birthday:
            birthday = f"{record.birthday}"
            if birthday.find(search_string) >= 0:
                return True
        for phone in record.phones:
            candidate = f"{phone.value}"
            candidate = candidate.replace(
                "-", "").replace("+", "").replace("(", "").replace(")", "")
            if candidate.find(search_string.replace("-", "").replace("+", "").replace("(", "").replace(")", "")) >= 0:
                return True
    return False


@ input_error
def handler_find(user_command: list) -> list:
    """"Find ...". With this command, the bot outputs a list 
    of users whose name or phone number matches the entered one or more(with an OR setting) string without space(" ").
    incoming: user_command (list) strimg(s) for searching
    return: list of string of found users"""

    found_list = ["Entries found in your contact book:"]
    for records in contact_dictionary.iterator(10):  # n_count from?
        volume = ""
        for record in records:
            if find_users(user_command[1:], record):
                if record.birthday:
                    volume += f"\n\n{record.name}, birthday: {record.birthday} ({record.days_to_birthday()} \
                    days to next birthday. Will be {record.years_old()} years old)\n-> phone(s): "
                else:
                    volume += f"\n\n{record.name}, birthday: {record.birthday}\n-> phone(s): "
                for phone in record.phones:
                    volume += f"{phone.value}; "
        found_list.append(volume)

    return found_list


@ input_error
def handler_show(user_command: list) -> str:
    """"show information about a specific user". With this command, the bot outputs
    birthday, number of days until next birthday and
    phone numbers to the console.
    incoming: user_command[1] is name of user
    return: string of info about user"""

    name = user_command[1]
    if contact_dictionary[name].birthday:
        user_information = f"\n\n{name}, birthday: {contact_dictionary[name].birthday} \
        ({contact_dictionary[name].days_to_birthday()} days to next birthday. \
        Will be {contact_dictionary[name].years_old()} years old)\n-> phone(s): "
    else:
        user_information = f"\n\n{name}, birthday: {contact_dictionary[name].birthday}\n-> phone(s): "
    for phone in contact_dictionary[name].phones:
        user_information += f"{phone.value}; "

    return user_information


@ input_error
def handler_add_birthday(user_command: list) -> str:
    """"add birthday...". With this command, the bot saves
    new information about user in memory (in the dictionary, for
    example). Instead of ... the user enters the name
    and birthday (in format YYYY-MM-DD), necessarily with a space.
    incoming: list of user command (name of user and birthday)
    return: string"""
    name = user_command[1]
    verdict = contact_dictionary[name].add_birthday(user_command[2])

    if verdict[0]:
        address_book_saver()
        return f"Information about {name} have been updated\n"
    else:
        return f"No changes have been made\n{verdict[1]}"


@ input_error
def handler_change_birthday(user_command: list) -> str:  # list of str
    """"change birthday ..." With this command, the bot stores the
    "new birthday" (if the previous one was wrong)
    of the existing contact in memory. Instead of ... the user enters
    the name and birthday (in format YYYY-MM-DD), necessarily with a space.
    incoming: list of user command (name of user, and birthday)
    return: string"""
    name = user_command[1]
    user_birthday = user_command[2]
    verdict = contact_dictionary[name].change_birthday(user_birthday)

    if verdict[0]:
        address_book_saver()
        return f"The record {name} has been updated\n"
    else:
        return f"No changes have been made\n{verdict[1]}"


def main_handler(user_command: list):
    """All possible bot commands
    incoming: user command
    return: function according to the command"""
    all_command = {"hello": handler_hello,
                   "add": handler_add,
                   "addphone": handler_add_phone,
                   "change": handler_change,
                   "phone": handler_phone,
                   "showall": handler_showall,
                   "goodbye": handler_exit,
                   "close": handler_exit,
                   "exit": handler_exit,
                   "show": handler_show,
                   "addbirthday": handler_add_birthday,
                   "changebirthday": handler_change_birthday,
                   "find": handler_find, }

    if all_command.get(user_command[0].lower(), "It is unclear") != "It is unclear":
        return all_command.get(user_command[0].lower())(user_command)

    return "It is unclear"


def handler_hello(_=None) -> str:
    return "How can I help you?\n"


def parser(user_input: str) -> list:
    """Command parser. The part responsible for parsing
    strings entered by the user, extracting keywords and
    command modifiers from the string.
    incoming: string from user
    return: list of comands"""
    words = user_input.strip().split(" ")
    if len(words) >= 2 and words[0].lower() == "good" and words[1].lower() == "bye":
        words = ["goodbye"]
    elif len(words) >= 2 and words[1].lower() == "all" and words[0].lower() == "show":
        words = ["showall"]
    elif len(words) >= 2 and words[1].lower() == "phone" and words[0].lower() == "add":
        words = ["addphone"] + words[2:]
    elif len(words) >= 2 and words[0].lower() == "add" and words[1].lower() == "birthday":
        words = ["addbirthday"] + words[2:]
    elif len(words) >= 2 and words[0].lower() == "change" and words[1].lower() == "birthday":
        words = ["changebirthday"] + words[2:]
    words[0] = words[0].lower()

    return words


def address_book_saver() -> None:
    """Save a class AddressBook to a file
    incoming: None
    return: None"""
    path_file = "ABook.data"
    new_path_file = helper_try_open_file(path_file)

    with open(new_path_file, "wb") as db_file:
        pickle.dump(contact_dictionary, db_file)


# contact_dictionary = AddressBook()


def main():
    """A new address book was not generated at the beginning
    ...
    """
    # global contact_dictionary #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
    path_file = "ABook.data"
    new_path_file = helper_try_open_file(path_file)
    if os.path.exists(new_path_file):
        with open(new_path_file, "rb") as fh:
            contact_dictionary = pickle.load(fh)
    else:
        contact_dictionary = AddressBook()
        address_book_saver()

    while True:
        user_command = input()
        user_request = parser(user_command)
        bot_answer = main_handler(user_request)
        if isinstance(bot_answer, str):
            print(bot_answer)
        else:
            for volume in bot_answer:
                if volume:
                    print(volume)
                    input("Press Enter for next Volume... ")
        if bot_answer == "Good bye!":
            break

    exit()


if __name__ == "__main__":
    exit(main())
