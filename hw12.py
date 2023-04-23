from adress_book_class import Name, Phone, Birthday, Record, AddressBook

phone_book = AddressBook()


def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except KeyError:
            return 'Contact with that name not found.'
        except ValueError:
            return 'Please enter a valid command.'
        except IndexError:
            return 'Please enter both name and phone number, separated by a space.'
    return wrapper

def decorator_main(func):
    def wrap():
        print('----Phone book Console Bot----\n'
              ' Commands: \n'
              '     hello - start bot\n'
              '     add - add new contact \n'
              '     change - change contact phone \n'
              '     phone - Search by name \n'
              '     show all - Show all list contact\n'
              '     goodbye, close, . - exit')
        print('-'*30)
        func()
    return wrap

def hello():
    return 'How can I help you?'

def good_bye():
    return 'Good bye!'


@input_error
def add_c():
    n_p = input('Enter name, phone +380000000000 and birthday d.m.y :').split(' ')

    name = Name(str(n_p[0]).title())
    
    
    if len(n_p) == 2:
        phone = Phone(n_p[1:])
        birthday = Birthday('01.01.0001')
    if len(n_p) > 2:
        phone = Phone(n_p[1:-1])
        birthday = Birthday(n_p[-1])    
    # if len(n_p) > 2 :    
    #     birthday = Birthday(n_p[-1])
    # else:
    #     birthday = Birthday(None)
    
    record = Record(name,phone,birthday)
    phone_book.add_record(record)

    return f'{name.value} : {phone.value}: {birthday.value} Add successful!'

    
@input_error
def change():
    n_p = input('Enter Name and phone:').split(' ')
    
    name = Name(n_p[0])
    phone = Phone( n_p[1:])
    record = phone_book[name.value]
    record.change_phone(0, phone)
    
    return f'{name.value} : {phone.value} Change successful!'

@input_error
def phones() -> str:
    src_by_name = input('Enter name:')
    
    if src_by_name in phone_book.data:
        for key, val in phone_book.data.items():
            record = phone_book.data[key]
            if src_by_name == key:
                return f"Phone: {', '.join(str(phone) for phone in record.phones)}"
            
    return 'Not find!'       
        
def decor_table(func):
    def wrapper(*words):
        print(' -'*32)
        print("|{:^5}|{:^15}|{:^24}|{:^15}".format('#', 'Name','Birthday HB:', 'Tel:'))
        print(' -'*32)
        func(*words)
        print(' -'*32)
    return wrapper
 
@decor_table        
def show_all():
    if len(phone_book.data) == 0:  
        print("No contacts found")
        
    else:
        i = 1
       
        for k in phone_book.iterator():   
            record = Record(k.name.value, k.phones, k.birthday.value)
            print("|{:^5}|{:^15}|{:^15}HB: {:<5}| {}".format(i, 
                                                    record.name, 
                                                    record.birthday,
                                                    record.days_to_birthday(record.birthday),
                                                    record.phones))
                                                    
            i += 1
            
            
def search_contact():
    src_by_name = input('Find by:')
    
    if len(phone_book.data) == 0:  
        print("No contacts found")
        
    else:
        for key, val in phone_book.data.items():
            record = phone_book.data[key]
            p_str = ', '.join(str(p) for p in record.phones)
            if src_by_name in p_str or src_by_name in record.name.value:
                print(f'{record.name}: {record.phones}')


                
COMMAND_DICT = {'hello': hello,
                 'add': add_c,
                 'change': change,
                 'phone': phones,
                 'show all': show_all,
                 'search': search_contact,
                 'goodbye': good_bye,
                 'close': good_bye,
                 '.': good_bye}


def get_command(words):
    if words in COMMAND_DICT:
        return COMMAND_DICT[words]
    print("This command doesn't exist")

@decorator_main
def main():
    
    try:
        phone_book.data = AddressBook.load_book('phone_book.bin')
    except FileNotFoundError:
        print('File not found!')
        
    while True:
        input_c = input(">>> ")
        
        func = get_command(input_c)
        try:
            print(func())
        except:
            ...
        
        if input_c in ['goodbye', 'close', '.']:
            phone_book.save_book('phone_book.bin')
            break
        
if __name__ == '__main__':
    main()