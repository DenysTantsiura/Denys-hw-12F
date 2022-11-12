""" rearch...
NEXT line ... 15, 47, 644 , 880...! MAP_ALL
"""
from collections import UserDict
from datetime import datetime, timedelta
import os
import pickle
import re
import sys
from typing import List, NoReturn, Union

AMBUSH = 'AMBUSH!'
TO_NEXT_FILE_NAME = 'new_one_'
DEFAULT_FILE_ADDRESS_BOOK = 'ABook.data'
DISPLAY_LIMIT_RECORDS = 10  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

PREFORMATING_PHONE = r'^\+[0-9)(-]{12,16}$'
PREFORMATING_EMAIL1 = r'\b[a-zA-z][\w_.]+@[a-zA-z]+\.[a-zA-z]{2,}[ ]'
PREFORMATING_EMAIL2 = r'\b[a-zA-z][\w_.]+@[a-zA-z]+\.[a-zA-z]+\.[a-zA-z]{2,}'

ERROR_MESSAGE = {
    'UnpicklingError':['The File',' is corrupted, my apologies.',],
    'UnpicklingOthers':['Is the File',' corrupted? ',],
    'OpenFile':['No access to File',', system error: ',],
    'WriteFile':['No access to write File',', error: ',],
    'PicklingError':['Can\'t save object in file',', my apologies.',],
    'PicklingOthers':['Something was wrong. File',' is not updated. ',],
    'UnknownCommand':['Unknown command ...',],
    '':['',],
    '':['',],
    '':['',],
    '':['',],
    '':['',],}

WARNING_MESSAGE = {
    'name':'At the beginning there can be only a Latin letter!',
    'birthday':'Incorrect or nonexistent date, entry must be in year-month-day format (YYYY-MM-DD).',
    'phone':'The number is obviously incorrect, the value should start with "+" and have 12 digits.',
    'email':'The e-mail is obviously incorrect.',
    'main':'Something happened. Will you try again?',
    'name is omitted':'Give me name OR name and phone please.\n',
    'the contact exists':'Such an entry is already in the book. Add or change a number.',
    'invalid name':'A name cannot begin with a number and can only begin with Latin characters!\n',
    'invalid phone':'There are no valid phone numbers.\nThe number must be in the following format with 12 digits(d): +dd(ddd)ddd-dddd .\n',
    'empty record to add':'There were no new entries to add.\n',
    'unsuccessful save':'Failed to save file.',
    'name and phone omitted':'Give me name and new phone(s) please.\n',
    'unknown name':'"The user unknown. No records avaible for this name yet. At first create it.', #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    'no address book':'No contact records available.\n',
    'name and birthday omitted':'Give me a name and birthday, please.\n',
    'invalid birthday entry':'The year of birth is not correct! A person too old or too young.\n',
    'invalid birthday':'The calendar date is not possible!\n',
    'name and 2 phones omitted':'Give me name and 2 phones please (current and new)\n',
    'no search query':'There is no search query\n',
    'name is missing':'Give me a name too, please.\n',
    '':'',
    '':'',}

# OTHER_MESSAGE
OTHER_MESSAGE = {
    'Record': ['\n\nRecord(Name: ', '; Phones: ', '; Birthday: ', ';\n\te-mail: ', ';\n\t details: ', ':\n\t related information: ',],
    'RBirthday':['Birthday already recorded for ','. You can change it.','Birthday not specified for ','. You can add it.',],
    'RPhone':[' already recorded for ',' already recorded for ',' not specified in the contact ',],
    'ABook':['AddressBook(Records:',],
    'next_page':['Press Enter for next Volume... ',],
    'Bye':['Good bye!',],
    'START':['Can I help you?\n',],
    'Unknown':['It is unclear. Unknown command...',],
    'Hello':['Hello! How can I help you?\n',],
    'successful addition':['A record(s) have been added.\n',],
    'update successful':['A record have been added. Address book file has been saved.',],
    'no changes':['No changes have been made.\n',],
    'deleting successful':['Record successfully deleted. Results saved.',],
    'deleting field':['Field record deleted successfully. Results saved.',],
    'no new entries':['There were no entries to add.\n',],
    'found':['Entries found in your contact book:',', birthday: ','(days to next birthday: ','. Will be ',' yrs. old)\n-> phone(s): ',', birthday: unknown\n-> phone(s): ','','',],
    '':['',],
    '':['',],
    '':['',],
    '':['',],}



class AddressBook(UserDict):
    """A class of Address book."""

    def __str__(self) -> str:
        ABOOK0 = OTHER_MESSAGE.get('ABook',[AMBUSH])[0]
        return f'{ABOOK0}{self.data})'

    def add_record(self, record) -> None:  # record: Record
        """Adds a new record to the address book dictionary."""
        self.data[record.name.value] = record

    def iterator(self, n_count: int) -> list:
        """Return(yield) of n_count records of all AddressBook."""
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

    def remove_record(self, name: str) -> None:
        """Remove a record from the address book dictionary."""
        self.data.pop(name)


class Field:  # superclass for all base fields
    """A base class with a simple field."""

    def __init__(self):
        self.__value = None
        self.__bloke = None

    def __str__(self):
        return f"{self.value}"

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value: str):
        self.__value = new_value
    
    @property
    def bloke(self):
        return self.__bloke

    @bloke.setter
    def bloke(self, new_bloke: str):
        self.__bloke = new_bloke


class Name(Field):
    """Class of user name."""
    @Field.value.setter
    def value(self, new_value: str):

        if new_value[0].isalpha():  # not in 'ьъыЫЬЪ\'"[]_0123456789!@$%^&*()-+?<>~`|\\/'
            self._Field__value = new_value

        else:
            print(WARNING_MESSAGE.get('name', AMBUSH))


class Birthday(Field):
    """Class of Birthday data."""
    @Field.value.setter
    def value(self, new_value: str):
        birthday_data = datetime.strptime(new_value, "%Y-%m-%d")

        if birthday_data:
            self._Field__value = birthday_data

        else:
            print(WARNING_MESSAGE.get('birthday', AMBUSH))

    def __str__(self) -> str:
        return f"{self.value.date()}"


class Phone(Field):
    """Class of phone number."""
    @Field.value.setter
    def value(self, new_value: str):

        if re.search(PREFORMATING_PHONE, new_value):
            self._Field__value = self.__preformating(new_value)

        else:
            print(WARNING_MESSAGE.get('phone', AMBUSH))
    
    @Field.bloke.setter
    def bloke(self, new_bloke: str):
        self._Field__bloke = new_bloke

    @staticmethod
    def __preformating(value: str) -> str:
        """Preformating of phone string into the form +dd(ddd)ddddddd."""
        value = value.replace('-', '').replace('(', '').replace(')', '')

        value = "(".join((value[: 3], value[3:]))
        value = ")".join((value[: 7], value[7:]))
 
        return value


class Details(Field):
    """Details information of user."""
    @Field.value.setter
    def value(self, new_value: str):
        self._Field__value = new_value
    
    @Field.bloke.setter
    def bloke(self, new_bloke: str):
        self._Field__bloke = new_bloke


class Email(Field):
    """Class of user Email."""
    @Field.value.setter
    def value(self, new_value: str):

        if re.search(PREFORMATING_EMAIL1, new_value) or\
             re.search(PREFORMATING_EMAIL2, new_value):
            self._Field__value = self.new_value.strip()

        else:
            print(WARNING_MESSAGE.get('email', AMBUSH))
    
    @Field.bloke.setter
    def bloke(self, new_bloke: str):
        self._Field__bloke = new_bloke


class RelatedInformation(Field):
    """Related information of user."""
    @Field.value.setter
    def value(self, new_value: str):
        self._Field__value = new_value

    @Field.bloke.setter
    def bloke(self, new_bloke: str):
        self._Field__bloke = new_bloke


class Record:
    """Record class of users information."""

    def __init__(self, name: str, *phones: str):
        self.name = Name()
        self.name.value = name
        self.phones = []
        self.birthday = None
        self.emails = []
        self.details = None
        self.related_info = None

        if phones:

            for phone in phones:
                self.add_phone(phone)

    def __str__(self) -> str:
        NAME = OTHER_MESSAGE.get('Record',[AMBUSH])[0]
        PHONES = OTHER_MESSAGE.get('Record',[AMBUSH]*2)[1]
        BIRTHDAY = OTHER_MESSAGE.get('Record',[AMBUSH]*3)[2]
        EMAIL = OTHER_MESSAGE.get('Record',[AMBUSH]*4)[3]
        DETAILS = OTHER_MESSAGE.get('Record',[AMBUSH]*5)[4]
        RELATED = OTHER_MESSAGE.get('Record',[AMBUSH]*6)[5]

        return f'{NAME}{self.name}{PHONES}{self.phones}{BIRTHDAY}'\
            f'{self.birthday}{EMAIL}{self.emails}{DETAILS}{self.details}'\
            f'{RELATED}{self.related_info})'

    def add_birthday(self, birthday: str) -> tuple:
        """Adds a new entry for the user's birthday to the address book."""
        if not self.birthday:

            self.birthday = Birthday()
            self.birthday.value = birthday

            return True,

        else:
            BIRTHDAY0 = OTHER_MESSAGE.get('RBirthday',[AMBUSH])[0]
            BIRTHDAY1 = OTHER_MESSAGE.get('RBirthday',[AMBUSH]*2)[1]
            return False, f'{BIRTHDAY0}{self.name.value}{BIRTHDAY1}'

    def add_phone(self, phone_new: str) -> bool:
        """Adds a new entry for the user's phone to the address book."""
        phone_new1 = Phone()
        phone_new1.value = phone_new

        for phone in self.phones:

            if phone_new1 == phone.value:
                
                PHONE0 = OTHER_MESSAGE.get('RPhone',[AMBUSH])[0]
                print(f'{phone_new1}{PHONE0}{self.name.value}')

                return False

        self.phones.append(phone_new1)

        return True

    def change_birthday(self, birthday: str) -> tuple:
        """Modify an existing user's birthday entry in the address book."""
        if not self.birthday:
            
            BIRTHDAY2 = OTHER_MESSAGE.get('RBirthday',[AMBUSH]*3)[2]
            BIRTHDAY3 = OTHER_MESSAGE.get('RBirthday',[AMBUSH]*4)[3]
            return False, f'{BIRTHDAY2}{self.name.value}{BIRTHDAY3}'

        else:

            self.birthday = Birthday()
            self.birthday.value = birthday

            return True,

    def change_phone(self, phone_to_change: str, phone_new: str) -> tuple:
        """Modify an existing user's phone entry in the address book."""
        phone_to_change = Phone._Phone__preformating(phone_to_change)
        phone_new = Phone._Phone__preformating(phone_new)
        verdict = False

        for phone in self.phones:

            if phone.value == phone_new:  # new number already in record
                PHONE1 = OTHER_MESSAGE.get('RPhone',[AMBUSH]*2)[1]
                return False, f'{phone_new}{PHONE1}{self.name.value}'

            if phone.value == phone_to_change:  # old number not exist in record
                verdict = True

        if not verdict:
            PHONE2 = OTHER_MESSAGE.get('RPhone',[AMBUSH]*3)[2]
            return verdict, f'{phone_to_change}{PHONE2}{self.name.value}'

        for index, phone in enumerate(self.phones):

            if phone.value == phone_to_change:
                phone_new_to = Phone()
                phone_new_to.value = phone_new
                self.phones.remove(phone)
                self.phones.insert(index, phone_new_to)

                return True,

    def days_to_birthday(self) -> int:
        """Count the number of days until the next birthday of the user."""
        if self.birthday:

            user_day = datetime(year=datetime.now().date().year, \
                month=self.birthday.value.month, day=self.birthday.value.day)

            days_left = user_day.date() - datetime.now().date()

            if days_left.days <= 0:

                user_day = datetime(year=datetime.now().date().year + 1, \
                    month=self.birthday.value.month, day=self.birthday.value.day)

                return (user_day.date() - datetime.now().date()).days

            return days_left.days

    def remove_birthday(self) -> Union[bool, None]:
        """Deleting a birthday entry from a user entry in the address book."""
        if self.birthday:
            self.birthday = None
            return True

    def remove_phone(self, phone_to_remove: str) -> Union[bool, None]:
        """Deleting a phone entry from a user entry in the address book."""
        phone_to_remove = Phone._Phone__preformating(phone_to_remove)

        for phone in self.phones:

            if phone.value == phone_to_remove:
                self.phones.remove(phone)

                return True

        PHONE2 = OTHER_MESSAGE.get('RPhone',[AMBUSH]*3)[2]      
        print(f'{phone_to_remove}{PHONE2}{self.name.value}')

    def years_old(self) -> int:
        """Calculate the number of full years of the user on the next birthday."""
        if self.birthday:
           
            user_day = datetime(year=datetime.now().date().year, \
                month=self.birthday.value.month, day=self.birthday.value.day)

            return datetime.now().year - 1 - self.birthday.value.year \
                if user_day.date() - datetime.now().date() >= 0 \
                else datetime.now().year - self.birthday.value.year


def helper_try_open_file(path_file: str) -> str:
    """Checks if the database file exists and checks if the filename is free if not.
    If exist folder with path_file file name, then return new free file name. 
    Return unoccupied name of file (string).

        Parameters:
            path_file (str): Is proposed name of file.

        Returns:
            path_file (str): Unoccupied name of file.
    """
    if os.path.isdir(path_file):

        while os.path.isdir(path_file):

            path_file = os.path.join(path_file.parent, TO_NEXT_FILE_NAME + path_file.name)

    return path_file


def helper_try_load_file(path_file: str) -> tuple(str, AddressBook):
    """Create empty address book (AddressBook) if no file on path_file.
    Or, try to load address book database (read) from file. 
    Return loaded address book (AddressBook) and path for address book file.

        Parameters:
            path_file (str): Is existed file (name or name with path).

        Returns:
            contact_dictionary (AddressBook): Loaded from file or new empty class.
            path_file (str): The file name to save the address book in the following steps..
                Unoccupied name of file, if an exception occurred.
    """
    if not os.path.exists(path_file):
        contact_dictionary = AddressBook()
        address_book_saver(contact_dictionary, path_file) #  False if can't save file!
        return contact_dictionary, path_file

    try:
        with open(path_file, "rb") as fh:
            try:
                contact_dictionary = pickle.load(fh)
                return contact_dictionary, path_file
            except pickle.UnpicklingError:
                ERROR_LOAD0 = ERROR_MESSAGE.get('UnpicklingError',[AMBUSH])[0]
                ERROR_LOAD1 = ERROR_MESSAGE.get('UnpicklingError',[AMBUSH]*2)[1]
                print(f'{ERROR_LOAD0}({path_file}){ERROR_LOAD1}')
                contact_dictionary = AddressBook()

            except Exception as error_: # pickle.PickleError inherits Exception.
                ERROR_LOAD0 = ERROR_MESSAGE.get('UnpicklingOthers',[AMBUSH])[0]
                ERROR_LOAD1 = ERROR_MESSAGE.get('UnpicklingOthers',[AMBUSH]*2)[1]
                print(f'{ERROR_LOAD0}({path_file}){ERROR_LOAD1}\n{repr(error_)}')
                contact_dictionary = AddressBook()

    except OSError as error_:
        ERROR_LOAD0 = ERROR_MESSAGE.get('OpenFile',[AMBUSH])[0]
        ERROR_LOAD1 = ERROR_MESSAGE.get('OpenFile',[AMBUSH]*2)[1]
        print(f'{ERROR_LOAD0}({path_file}){ERROR_LOAD1}\n{type(error_)}: {error_}')
        contact_dictionary = AddressBook()

    except Exception as error_:
        ERROR_LOAD0 = ERROR_MESSAGE.get('OpenFile',[AMBUSH])[0]
        ERROR_LOAD1 = ERROR_MESSAGE.get('OpenFile',[AMBUSH]*2)[1]
        print(f'{ERROR_LOAD0}({path_file}){ERROR_LOAD1}\n{repr(error_)}')
        contact_dictionary = AddressBook()

    while os.path.exists(path_file):
        path_file = os.path.join(path_file.parent, TO_NEXT_FILE_NAME + path_file.name)

    return contact_dictionary, path_file


def address_book_saver(contact_dictionary: AddressBook, path_file: str) -> bool:
    """Save a class AddressBook to a file (path_file).

        Parameters:
            contact_dictionary (AddressBook): Instance of AddressBook.
            path_file (str): Is there path and filename of address book.

        Returns:
            File save success marker (bool).
    """
    try:

        with open(path_file, "wb") as db_file:

            try:

                pickle.dump(contact_dictionary, db_file)

            except pickle.PicklingError:
                ERROR_SAVE0 = ERROR_MESSAGE.get('PicklingError',[AMBUSH])[0]
                ERROR_SAVE1 = ERROR_MESSAGE.get('PicklingError',[AMBUSH]*2)[1]
                print(f'{ERROR_SAVE0}({path_file}){ERROR_SAVE1}')
                return False
                # contact_dictionary = AddressBook()

            except Exception as error_: # pickle.PickleError inherits Exception.
                ERROR_SAVE0 = ERROR_MESSAGE.get('PicklingOthers',[AMBUSH])[0]
                ERROR_SAVE1 = ERROR_MESSAGE.get('PicklingOthers',[AMBUSH]*2)[1]
                print(f'{ERROR_SAVE0}({path_file}){ERROR_SAVE1}\n{repr(error_)}')
                return False
                # contact_dictionary = AddressBook()

    except OSError as error_:
        ERROR_WRITE0 = ERROR_MESSAGE.get('WriteFile',[AMBUSH])[0]
        ERROR_WRITE1 = ERROR_MESSAGE.get('WriteFile',[AMBUSH]*2)[1]
        print(f'{ERROR_WRITE0}({path_file}){ERROR_WRITE1}\n{type(error_)}: {error_}')
        return False

    except Exception as error_:
        ERROR_WRITE0 = ERROR_MESSAGE.get('WriteFile',[AMBUSH])[0]
        ERROR_WRITE1 = ERROR_MESSAGE.get('WriteFile',[AMBUSH]*2)[1]
        print(f'{ERROR_WRITE0}({path_file}){ERROR_WRITE1}\n{repr(error_)}')
        return False

    return True


def find_users(search_strings: List[str], record: Record) -> bool:
    """Check a record for matching the search strings.

        Parameters:
            search_strings (List[str]): The data in the list rows in the user's search query.
            record (Record): Record - User account card.

        Returns:
            True or False (bool): Search result (Search success rate).
    """
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


class TheNameIsOmitted(Exception):
    pass

class TheContactIsExist(Exception):
    pass

class TheNameIsIncorrect(Exception):
    pass

class ThePhoneIsIncorrect(Exception):
    pass

class TheNameAndPhoneAreMissing(Exception):
    pass

class TheContactIsNotExist(Exception):
    pass

class NoAddressBook(Exception):
    pass

class TheNameAndBirthdayAreMissing(Exception):
    pass

class InvalidBirthdayEntry(Exception):
    pass

class InvalidBirthday(Exception):
    pass

class TheNameAnd2PhonesAreMissing(Exception):
    pass

class NoSearchQuery(Exception):
    pass

class TheNameIsMissing(Exception):
    pass



# --------------------------------------------------------------------------------

def input_error(handler):
    """User error handler (decorator).

        Parameters:
            handler (function): Incoming function.

        Returns:
            exception_function(function): Exception function for handler functions.

    """
    def exception_function(user_command: list, contact_dictionary: AddressBook, path_file: str) -> Union[str, list]:
        """Exception function for handler functions."""
        try:
            VALIDATION_FUNCTIONS[handler.__name__](user_command,\
                 contact_dictionary)
        except KeyError:
            return ERROR_MESSAGE.get('UnknownCommand', AMBUSH)
        except TheNameIsOmitted:
            return WARNING_MESSAGE.get('name is omitted', AMBUSH)
        except TheContactIsExist:
            return WARNING_MESSAGE.get('the contact exists', AMBUSH)
        except TheNameIsIncorrect:
            return WARNING_MESSAGE.get('invalid name', AMBUSH)
        except ThePhoneIsIncorrect:
            return WARNING_MESSAGE.get('invalid phone', AMBUSH)
        except TheNameAndPhoneAreMissing:
            return WARNING_MESSAGE.get('name and phone omitted', AMBUSH)
        except TheContactIsNotExist:
            return WARNING_MESSAGE.get('unknown name', AMBUSH)
        except NoAddressBook:
            return WARNING_MESSAGE.get('no address book', AMBUSH)
        except TheNameAndBirthdayAreMissing:
            return WARNING_MESSAGE.get('name and birthday omitted', AMBUSH)
        except InvalidBirthdayEntry:
            return WARNING_MESSAGE.get('invalid birthday entry', AMBUSH)
        except InvalidBirthday:
            return WARNING_MESSAGE.get('invalid birthday', AMBUSH)
        except TheNameAnd2PhonesAreMissing:
            return WARNING_MESSAGE.get('name and 2 phones omitted', AMBUSH)
        except NoSearchQuery:
            return WARNING_MESSAGE.get('no search query', AMBUSH)
        except TheNameIsMissing:
            return WARNING_MESSAGE.get('name is missing', AMBUSH)

        try:
            result = handler(user_command, contact_dictionary, path_file)

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

'''
def record_update_controller():
    """......."""
    if verdict[0]:
        if address_book_saver(contact_dictionary, path_file):
            return OTHER_MESSAGE.get('update successful', AMBUSH)[0]
        else:
            return WARNING_MESSAGE.get('unsuccessful save', AMBUSH)
    else:
        no_changes = OTHER_MESSAGE.get('no changes', AMBUSH)[0]
        return f'{no_changes}{verdict[1]}'
'''

@ input_error
def handler_add(user_command: List[str], contact_dictionary: AddressBook, path_file: str) -> str:
    """"add ...": The bot saves a new contact in contact dictionary 
    and save it in file(path_file). Instead of ... the user enters 
    the name and phone number(s), necessarily with a space.

        Parameters:
            user_command (List[str]): List of user command (name of user [and phone(s)]).
            contact_dictionary (AddressBook): Instance of AddressBook .
            path_file (str): Is there path and filename of address book.

        Returns:
            string(str): Answer for the user.
    """
    name = user_command[1]
    new_record = Record(name)
    contact_dictionary.add_record(new_record)

    if len(user_command) > 2:

        phones = user_command[2:]
        verdict = False

        for new_phone in phones:
            verdict = contact_dictionary[name].add_phone(new_phone) or verdict

        if not verdict:
            return WARNING_MESSAGE.get('empty record to add', AMBUSH)

    if address_book_saver(contact_dictionary, path_file):
        return OTHER_MESSAGE.get('successful addition', AMBUSH)[0]
    else:
        return WARNING_MESSAGE.get('unsuccessful save', AMBUSH)


@ input_error
def handler_add_birthday(user_command: List[str], contact_dictionary: AddressBook, path_file: str) -> str:
    """"add birthday...": The bot saves new information about user 
    in contact dictionary and save it in file(path_file). 
    Instead of ... the user enters the name and birthday (in format YYYY-MM-DD), 
    necessarily with a space.

        Parameters:
            user_command (List[str]): List of user command (name of user and birthday).
            contact_dictionary (AddressBook): Instance of AddressBook .
            path_file (str): Is there path and filename of address book.

        Returns:
            string(str): Answer for the user.
    """
    name = user_command[1]
    verdict = contact_dictionary[name].add_birthday(user_command[2])

    if verdict[0]:

        if address_book_saver(contact_dictionary, path_file):
            return OTHER_MESSAGE.get('update successful', AMBUSH)[0]
        else:
            return WARNING_MESSAGE.get('unsuccessful save', AMBUSH)

    else:
        no_changes = OTHER_MESSAGE.get('no changes', AMBUSH)[0]
        return f'{no_changes}{verdict[1]}'


@ input_error
def handler_add_phone(user_command: List[str], contact_dictionary: AddressBook, path_file: str) -> str:
    """"add ...": The bot saves a new phones to contact in contact dictionary 
    and save it in file(path_file). Instead of ... the user enters the name
    and phone number(s), necessarily with a space.

        Parameters:
            user_command (List[str]): List of user command (name of user and phone(s)).
            contact_dictionary (AddressBook): Instance of AddressBook .
            path_file (str): Is there path and filename of address book.

        Returns:
            string(str): Answer for the user.
    """
    name = user_command[1]
    phones = user_command[2:]
    verdict = False
    write_count = 0

    for new_phone in phones:
        verdict = contact_dictionary[name].add_phone(new_phone) or verdict
        write_count += 1 if verdict else 0

    if not write_count:
        return OTHER_MESSAGE.get('no new entries', AMBUSH)[0]

    if address_book_saver(contact_dictionary, path_file):
        return OTHER_MESSAGE.get('update successful', AMBUSH)[0]
    else:
        return WARNING_MESSAGE.get('unsuccessful save', AMBUSH)


@ input_error
def handler_change(user_command: List[str], contact_dictionary: AddressBook, path_file: str) -> str:
    """"change ...": The bot stores the new phone number of the existing 
    ontact in contact dictionary and save it in file(path_file). 
    Instead of ... the user enters the name and phone numbers (current and new), 
    necessarily with a space.

        Parameters:
            user_command (List[str]): List of user command (name of user and phones).
            contact_dictionary (AddressBook): Instance of AddressBook .
            path_file (str): Is there path and filename of address book.

        Returns:
            string(str): Answer for the user.
    """
    name = user_command[1]
    current_phone = user_command[2]
    new_phone = user_command[3]
    verdict = contact_dictionary[name].change_phone(current_phone, new_phone)

    if verdict[0]:

        if address_book_saver(contact_dictionary, path_file):
            return OTHER_MESSAGE.get('update successful', AMBUSH)[0]
        else:
            return WARNING_MESSAGE.get('unsuccessful save', AMBUSH)

    else:
        no_changes = OTHER_MESSAGE.get('no changes', AMBUSH)[0]
        return f'{no_changes}{verdict[1]}'


@ input_error
def handler_change_birthday(user_command: List[str], contact_dictionary: AddressBook, path_file: str) -> str:
    """"change birthday ...": The bot stores the
    "new birthday" (if the previous one was wrong)
    of the existing contact in contact dictionary and save it in file(path_file). 
    Instead of ... the user enters the name and birthday (in format YYYY-MM-DD), 
    necessarily with a space.

        Parameters:
            user_command (List[str]): List of user command (name of user, and birthday).
            contact_dictionary (AddressBook): Instance of AddressBook .
            path_file (str): Is there path and filename of address book.

        Returns:
            string(str): Answer for the user.
    """
    name = user_command[1]
    user_birthday = user_command[2]
    verdict = contact_dictionary[name].change_birthday(user_birthday)

    if verdict[0]:

        if address_book_saver(contact_dictionary, path_file):
            return OTHER_MESSAGE.get('update successful', AMBUSH)[0]
        else:
            return WARNING_MESSAGE.get('unsuccessful save', AMBUSH)

    else:
        no_changes = OTHER_MESSAGE.get('no changes', AMBUSH)[0]
        return f'{no_changes}{verdict[1]}'


@ input_error
def handler_find(user_command: List[str], contact_dictionary: AddressBook, _=None) -> list:
    """"Find ...": The bot outputs a list of users whose name or phone number 
    matches the entered one or more(with an OR setting) string without space(" ").

        Parameters:
            user_command (List[str]): List of user command (strimg(s) for searching).
            contact_dictionary (AddressBook): Instance of AddressBook .
            path_file (str): Is there path and filename of address book.

        Returns:
            found_list (list): Answer for the user - list of string of found users.
    """ 
    found_list = [OTHER_MESSAGE.get('found', AMBUSH)[0]]
    found_p1 = OTHER_MESSAGE.get('found', AMBUSH)[1]
    found_p2 = OTHER_MESSAGE.get('found', AMBUSH)[2]
    found_p3 = OTHER_MESSAGE.get('found', AMBUSH)[3]
    found_p4 = OTHER_MESSAGE.get('found', AMBUSH)[4]
    found_p5 = OTHER_MESSAGE.get('found', AMBUSH)[5]
 
    for records in contact_dictionary.iterator(DISPLAY_LIMIT_RECORDS): 
        volume = ""

        for record in records:

            if find_users(user_command[1:], record):

                if record.birthday:
                    volume += f'\n\n{record.name}{found_p1}{record.birthday}' \
                    f'{found_p2}{record.days_to_birthday()}'\
                    f'{found_p3}{record.years_old()}{found_p4}'

                else:
                    volume += f'\n\n{record.name}{found_p5}'

                for phone in record.phones:
                    volume += f'{phone.value}; '

        found_list.append(volume)

    return found_list


def handler_hello(*_) -> str:
    """Reply to the greeting."""
    return OTHER_MESSAGE.get('Hello',[AMBUSH])[0]


@ input_error
def handler_phone(user_command: List[str], contact_dictionary: AddressBook, _=None) -> str:
    """"phone ....": The bot outputs the phone number for the specified
    contact. Instead of ... the user enters the name of the contact
    whose number should be displayed.

        Parameters:
            user_command (List[str]): List of user command (name of user [and phone(s)]).
            contact_dictionary (AddressBook): Instance of AddressBook .
            path_file (str): Is there path and filename of address book.

        Returns:
            string(str): Answer for the user.

    :incoming: 
    :user_command -- list of user command (name of user)
    :contact_dictionary -- instance of AddressBook 
    :_ -- not_matter: None 
    :return: 
    :string -- answer (phone number(s) of user)
    """
    phones = ""
    name = user_command[1]

    for phone in (contact_dictionary[name]).phones:
        phones += f"{phone.value}; "

    return phones


@ input_error
def handler_remove(user_command: List[str], contact_dictionary: AddressBook, path_file: str) -> str:
    """"remove ...": The bot remove a record contact in contact dictionary 
    and save it in file(path_file). Instead of ... the user enters the name.

        Parameters:
            user_command (List[str]): List of user command (name of user [and phone(s)]).
            contact_dictionary (AddressBook): Instance of AddressBook .
            path_file (str): Is there path and filename of address book.

        Returns:
            string(str): Answer for the user.

    :incoming: 
    :user_command -- list of user command (name of user)
    :contact_dictionary -- instance of AddressBook 
    :path_file -- is there path and filename of address book (in str) 
    :return: 
    :string -- answer
    """
    if contact_dictionary.get(user_command[1], None):

        contact_dictionary.remove_record(user_command[1])

        if address_book_saver(contact_dictionary, path_file):
            return OTHER_MESSAGE.get('deleting successful', AMBUSH)[0]
        else:
            return WARNING_MESSAGE.get('unsuccessful save', AMBUSH)

    else:
        return f"Record '{user_command[1]}' not found.\n"


@ input_error
def handler_remove_birthday(user_command: List[str], contact_dictionary: AddressBook, path_file: str) -> str:
    """"remove birthday ...": The bot remove a birthday record from contact in contact dictionary 
    and save it in file(path_file). Instead of ... the user enters the name.

        Parameters:
            user_command (List[str]): List of user command (name of user [and phone(s)]).
            contact_dictionary (AddressBook): Instance of AddressBook .
            path_file (str): Is there path and filename of address book.

        Returns:
            string(str): Answer for the user.

    :incoming: 
    :user_command -- list of user command (name of user)
    :contact_dictionary -- instance of AddressBook 
    :path_file -- is there path and filename of address book (in str) 
    :return: 
    :string -- answer
    """
    name = user_command[1]
    if contact_dictionary.get(name, None):

        if contact_dictionary[name].birthday:

            contact_dictionary[name].remove_birthday()

            if address_book_saver(contact_dictionary, path_file):
                return OTHER_MESSAGE.get('deleting field', AMBUSH)[0]
            else:
                return WARNING_MESSAGE.get('unsuccessful save', AMBUSH)

        else:
            return f"Birthday entry in record '{name}' not found.\n"

    else:
        return f"Record '{name}' not found.\n"


@ input_error
def handler_remove_phone(user_command: List[str], contact_dictionary: AddressBook, path_file: str) -> str:
    """"remove phone ...": The bot remove a phone record from contact in contact dictionary 
    and save it in file(path_file). Instead of ... the user enters the name and phone 
    number(s), necessarily with a space.

        Parameters:
            user_command (List[str]): List of user command (name of user [and phone(s)]).
            contact_dictionary (AddressBook): Instance of AddressBook .
            path_file (str): Is there path and filename of address book.

        Returns:
            string(str): Answer for the user.

    :incoming: 
    :user_command -- list of user command (name of user)
    :contact_dictionary -- instance of AddressBook 
    :path_file -- is there path and filename of address book (in str) 
    :return: 
    :string -- answer
    """
    name = user_command[1]
    if contact_dictionary.get(name, None):

        if contact_dictionary[name].phones:

            phone = user_command[2]
            verdict = contact_dictionary[name].remove_phone(phone)

            if verdict:

                if address_book_saver(contact_dictionary, path_file):
                    return OTHER_MESSAGE.get('deleting field', AMBUSH)[0]
                else:
                    return WARNING_MESSAGE.get('unsuccessful save', AMBUSH)

            else:
                return f"Phone entry '{phone}' in record '{name}' not found.\n"

        else:
            return f"Phone(s) entry in record '{name}' not found.\n"

    else:
        return f"Record '{name}' not found.\n"


@ input_error
def handler_show(user_command: List[str], contact_dictionary: AddressBook, _=None) -> str:
    """"show information about a specific user". With this command, the bot outputs
    birthday, number of days until next birthday and phone numbers to the console.

        Parameters:
            user_command (List[str]): List of user command (name of user [and phone(s)]).
            contact_dictionary (AddressBook): Instance of AddressBook .
            path_file (str): Is there path and filename of address book.

        Returns:
            string(str): Answer for the user.

    :incoming: 
    :user_command -- list of user command (where user_command[1] is name of user)
    :contact_dictionary -- instance of AddressBook
    :return: 
    :string of information about user
    """
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
def handler_show_all(_, contact_dictionary: AddressBook, _a) -> list:
    """"show all": The bot outputs all saved contacts.

        Parameters:
            user_command (List[str]): List of user command (name of user [and phone(s)]).
            contact_dictionary (AddressBook): Instance of AddressBook .
            path_file (str): Is there path and filename of address book.

        Returns:
            string(str): Answer for the user.

    :incoming: 
    :_ -- not_matter: Any
    :contact_dictionary -- instance of AddressBook 
    :path_file -- is there path and filename of address book (in str) 
    :return: 
    :list of string of all users
    """
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


def validation_add(user_command: list, contact_dictionary: AddressBook) ->\
        None:
    """Check the input parameters. Raise a mismatch exception if found."""
    name = user_command[1] if len(user_command) > 1 else None

    if not name:  # len(user_command) < 2:
        raise TheNameIsOmitted

    if name in contact_dictionary:
        raise TheContactIsExist

    if name[0].isdigit() or not name[0].isalpha():
        raise TheNameIsIncorrect

    if len(user_command) >= 2:
        phone_count = 0

        for phone_candidate in user_command[2:]:
            phone_matches = re.search(PREFORMATING_PHONE, phone_candidate)

            if phone_matches:
                phone_count += 1

            else:
                print(f'{phone_candidate}', WARNING_MESSAGE.get('phone', AMBUSH))

        if phone_count < len(user_command[2:]):  # not phone_count:
            raise ThePhoneIsIncorrect


def validation_add_phone(user_command: list, contact_dictionary: AddressBook) -> None:
    """Check the input parameters. Return a message (str) about a discrepancy if it is detected."""
    name = user_command[1] if len(user_command) > 1 else None

    if len(user_command) < 3:  # or not name:
        raise TheNameAndPhoneAreMissing

    if name[0].isdigit() or not name[0].isalpha():
        raise TheNameIsIncorrect

    if name not in contact_dictionary:
        raise TheContactIsNotExist

    phone_count = 0

    for phone_candidate in user_command[2:]:
        phone_matches = re.search(PREFORMATING_PHONE, phone_candidate)
        
        if phone_matches:
            phone_count += 1

        else:
            print(f'{phone_candidate}', WARNING_MESSAGE.get('phone', AMBUSH))

    if phone_count < len(user_command[2:]):  # not phone_count:
        raise ThePhoneIsIncorrect


def validation_birthday(user_command: list, contact_dictionary: AddressBook) -> Union[str, None]:
    """Check the input parameters. Return a message (str) about a discrepancy if it is detected."""
    name = user_command[1] if len(user_command) > 1 else None

    if not contact_dictionary:
        raise NoAddressBook 

    if len(user_command) < 3:  # or not name:
        raise TheNameAndBirthdayAreMissing

    if name[0].isdigit() or not name[0].isalpha():
        raise TheNameIsIncorrect

    if datetime.now().year - 122 > int(user_command[2].split("-")[0]) > datetime.now().year - 8:  # 0, 8, 14, 16, 18 ?
        raise InvalidBirthdayEntry

    else:
        try:
            datetime.strptime(user_command[2], "%Y-%m-%d")

        except ValueError:
            raise InvalidBirthday


def validation_change(user_command: list, contact_dictionary: AddressBook) -> \
        None:
    """Check the input parameters. Return a message (str) about a discrepancy if it is detected."""
    name = user_command[1] if len(user_command) > 1 else None

    if not contact_dictionary:
        raise NoAddressBook

    if len(user_command) < 4:  # or not name:
        raise TheNameAnd2PhonesAreMissing

    if name[0].isdigit() or not name[0].isalpha():
        raise TheNameIsIncorrect

    phone_count = 0

    for phone_candidate in user_command[2:]:
        phone_matches = re.search(PREFORMATING_PHONE, phone_candidate)
        
        if phone_matches:
            phone_count += 1

        else:
            print(f'{phone_candidate}', WARNING_MESSAGE.get('phone', AMBUSH))

    if phone_count < len(user_command[2:]):  # not phone_count:
        raise ThePhoneIsIncorrect


def validation_find(user_command: list, contact_dictionary: AddressBook) -> None:
    """Check the input parameters. Return a message (str) about a discrepancy if it is detected."""
    query = user_command[1] if len(user_command) > 1 else None

    if not contact_dictionary:
        raise NoAddressBook

    if not query:
        raise NoSearchQuery


def validation_phone(user_command: list, contact_dictionary: AddressBook) -> None:
    """Check the input parameters. Return a message (str) about a discrepancy if it is detected."""
    name = user_command[1] if len(user_command) > 1 else None

    if not contact_dictionary:
        raise NoAddressBook

    if not name:  # len(user_command) < 2 or not name:
        raise TheNameIsMissing

    if name[0].isdigit() or not name[0].isalpha():
        raise TheNameIsIncorrect


def validation_remove(user_command: list, contact_dictionary: AddressBook) -> None:
    """Check the input parameters. Return a message (str) about a discrepancy if it is detected."""
    name = user_command[1] if len(user_command) > 1 else None

    if not contact_dictionary:
        raise NoAddressBook

    if not name:
        raise TheNameIsMissing

    if name[0].isdigit() or not name[0].isalpha():
        raise TheNameIsIncorrect

    if name not in contact_dictionary:
        raise TheContactIsNotExist


def validation_remove_birthday(user_command: list, contact_dictionary: AddressBook) -> None:
    """Check the input parameters. Return a message (str) about a discrepancy if it is detected."""
    name = user_command[1] if len(user_command) > 1 else None

    if not contact_dictionary:
        raise NoAddressBook

    if not name:  # len(user_command) < 2:
        raise TheNameIsMissing

    if name[0].isdigit() or not name[0].isalpha():
        raise TheNameIsIncorrect

    if name not in contact_dictionary:
        raise TheContactIsNotExist


def validation_remove_phone(user_command: list, contact_dictionary: AddressBook) -> \
        None:
    """Check the input parameters. Return a message (str) about a discrepancy if it is detected."""
    name = user_command[1] if len(user_command) > 1 else None

    if not contact_dictionary:
        raise NoAddressBook

    if not name:
        raise TheNameIsMissing

    if name[0].isdigit() or not name[0].isalpha():
        raise TheNameIsIncorrect

    if name not in contact_dictionary:
        raise TheContactIsNotExist

    phone_count = 0

    for phone_candidate in user_command[2:]:
        phone_matches = re.search(PREFORMATING_PHONE, phone_candidate)
        
        if phone_matches:
            phone_count += 1

        else:
            print(f'{phone_candidate}', WARNING_MESSAGE.get('phone', AMBUSH))

    if phone_count < 2:  # len(user_command[2:])  # not phone_count:
        raise ThePhoneIsIncorrect


def validation_show(user_command: list, contact_dictionary: AddressBook) -> None:
    """Check the input parameters. Return a message (str) about a discrepancy if it is detected."""
    name = user_command[1] if len(user_command) > 1 else None

    if not contact_dictionary:
        raise NoAddressBook

    if not name:
        raise TheNameIsMissing

    if name[0].isdigit() or not name[0].isalpha():
        raise TheNameIsIncorrect


def validation_showall(_, contact_dictionary: AddressBook) -> None:
    """Check the input parameters. Return a message (str) about a discrepancy if it is detected."""
    if not contact_dictionary:
        raise NoAddressBook


def handler_exit(*_) -> str:
    """Reply to the exit command."""
    return OTHER_MESSAGE.get('Bye',[AMBUSH])[0]


ALL_COMMAND = {'hello': handler_hello,
                'add': handler_add,
                'add_phone': handler_add_phone,
                'change': handler_change,
                'phone': handler_phone,
                'show_all': handler_show_all,
                'good_bye': handler_exit,
                'close': handler_exit,
                'exit': handler_exit,
                'show': handler_show,
                'add_birthday': handler_add_birthday,
                'change_birthday': handler_change_birthday,
                'find': handler_find,
                'remove': handler_remove,
                'remove_phone': handler_remove_phone,
                'remove_birthday': handler_remove_birthday, 
                }


VALIDATION_FUNCTIONS = {
            "handler_add": validation_add,
            "handler_add_birthday": validation_birthday,
            "handler_add_phone": validation_add_phone,
            "handler_change": validation_change,
            "handler_change_birthday": validation_birthday,
            "handler_find": validation_find,
            "handler_phone": validation_phone,
            "handler_remove": validation_remove,
            "handler_remove_birthday": validation_remove_birthday,
            "handler_remove_phone": validation_remove_phone,
            "handler_show": validation_show,
            "handler_show_all": validation_showall,
            # "unknown": lambda *_: raise UnknownCommand,  # "Unknown command..."
        }


def main_handler(user_command: List[str], contact_dictionary: AddressBook, path_file: str) -> Union[str, list]:
    """All possible bot commands. Get a list of command and options, 
    a dictionary of contacts, and the path to an address book file. 
    Call a certain function and return a response to a command request.

        Parameters:
            user_command (List[str]): list of user command (list of command and options).
            contact_dictionary (AddressBook): Instance of AddressBook.
            path_file (str): Is there path and filename of address book (in str).

        Returns:
            The result of the corresponding function (list): The result of the\
                 certain function is a string or a list of strings.
    """
    return ALL_COMMAND.get(user_command[0], lambda *args: None)(user_command, \
        contact_dictionary, path_file) \
        or OTHER_MESSAGE.get('Unknown',[AMBUSH])[0]


def parser(user_input: str) -> List[str]:
    """Command parser. Get a user string - separate the command and parameters - 
    return it to the list, where the first element is the command, 
    the others are parameters.

        Parameters:
            user_input (str): String line of user input.

        Returns:
            list command of user input (list): list of comands (list of strings).
    """
    command_line = user_input.strip().replace(' ','~').lower()
    all_commands = sorted([el.replace('_','~') for el in ALL_COMMAND], key=len)[::-1]   
    for command in all_commands:
        if command_line.startswith(command):
            command.replace('~','_')
            return [command.replace('~','_')] + [word for word in user_input[len(command):].split(" ") if word]

    return user_input.strip().split(" ")  #  OTHER_MESSAGE.get('Unknown',[AMBUSH])[0]


def main() -> NoReturn:
    """The main function of launching a helper console bot that 
    recognize the commands entered from the keyboard and respond 
    according to the command entered.
    Enter a command - get an answer.
    """
    try:
        path_file = sys.argv[1]

    except IndexError:
        path_file = DEFAULT_FILE_ADDRESS_BOOK

    new_path_file = helper_try_open_file(path_file)

    contact_dictionary, new_path_file = helper_try_load_file(new_path_file)

    while True:
        user_command = input(OTHER_MESSAGE.get('START',[AMBUSH])[0])
        user_request = parser(user_command)  # ['remove_phone', '+38000001', '+5555578']
        bot_answer = main_handler(
            user_request, contact_dictionary, new_path_file)

        if isinstance(bot_answer, str):
            print(bot_answer)

        elif isinstance(bot_answer, list):

            for volume in bot_answer:

                if volume:

                    print(volume)
                    input(OTHER_MESSAGE.get('next_page',[AMBUSH])[0])

        else:
            print(WARNING_MESSAGE.get('main', AMBUSH))

        if bot_answer == OTHER_MESSAGE.get('Bye',[AMBUSH])[0]:
            break


if __name__ == '__main__':
    main()
