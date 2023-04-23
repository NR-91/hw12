from collections import UserDict
import re
from datetime import datetime
import pickle

class Field:
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return str(self.value)
    

class Name(Field):
    ...

class Phone(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, phone):
        for p in phone:
            if re.match('\+380\d{9}', p):
                self.__value = phone
            else:
                print('Number is wrong! Try again)')
    
    def __repr__(self):
        return ', '.join(str(p) for p in self.__value)
                         

class Birthday(Field):
    
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, birthday):

        if re.match('\d{2}\.\d{2}\.\d{4}', birthday):
            self.__value = birthday
        else:
            print('Date is wrong! Try again)')

        
class Record:
    def __init__(self, name: Name, phone: Phone=None, birthday: Birthday=None):
        self.name = name
        self.phones = [phone] if phone else []
        self.birthday = birthday

    def add_phone(self, phone):
        self.phones.append(phone)
        
    def change_phone(self, index, phone):
        self.phones[index] = phone
        
    def delete_phone(self, phone):
        self.phones.remove(phone)
           
    def days_to_birthday(self,birthday):

        current_datetime = datetime.today()
        d = str(birthday).split('.')
        user_date = datetime(year = current_datetime.year, month = int(d[1]), day = int(d[0]))
        s_w = user_date - current_datetime
        return s_w.days 
        
        
    
class AddressBook(UserDict):
    
    page_index = 0
      
    def add_record(self, record):
        self.data[record.name.value] = record
        
    def __getitem__(self, name):
        if not name in self.data.keys():
            raise Exception("This user isn't in the Book")
        return self.data[name]
    
    def iterator(self, n = 5):
        if len(self.data) > self.page_index:
            yield from [self.data[name] for name in sorted(self.data.keys())[self.page_index:self.page_index + n]]
            self.page_index += n
        else:
            self.page_index = 0
            raise StopIteration
    
    def save_book(self, f):
        with open(f, 'wb') as file:
            pickle.dump(self.data, file)
            
    @classmethod
    def load_book(cls, f):
        with open(f, 'rb') as file:
            data = pickle.load(file)
        load_data = cls()
        load_data.data = data
        return load_data