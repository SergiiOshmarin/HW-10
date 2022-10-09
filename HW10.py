from collections import UserDict

class AdressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record


class Record():
    def __init__(self, name, phone = None):
        self.name = Name(name)
        if phone:
            self.phones = [Phone(phone)]
        else:
            self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))
    
    def delete_phone(self, phone):
        phone_obj = Phone(phone)    
        if phone_obj in self.phones:
            self.phone.remove(phone_obj)

    def change_phone(self, old_phone, new_phone):
        some_list=[phone.value for phone in self.phones]
        self.phones[some_list.index(old_phone)] = Phone(new_phone)

class Field():
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    pass

contacts_dictionary = AdressBook()

def format_phone_number(func):
    def inner(x):
        result = func(x)
        if len(result)<10:
            return sanitize_phone_number(input("Looks like you type wrong number.Please try again.Type only number\n"))
        elif len(result)<12:
            new_result="+38"+result
            return new_result
        elif len(result)<13:
            new_result="+"+result
            return new_result
        elif len(result)>=13:
            return sanitize_phone_number(input("Looks like you type wrong number.Please try again.Type only number\n"))
        else:
            return result      
    return inner

@format_phone_number
def sanitize_phone_number(phone):
    new_phone = (
        phone.strip()
            .removeprefix("+")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace(" ", "")
    )
    return new_phone

def format_name(list):
    if type(list)==str:
        list=list.strip().split()
    new_name=[]
    for i in list:
        if i.isalpha():
            name=i.lower().capitalize()
            new_name.append(name)
        else:
            return format_name(input("Looks like you type wrong name.Please try again.Type only first and second name\n"))
    return " ".join(new_name) 
            

def parser_command(string):
    modified_list1=string.strip().split()
    return modified_list1

def name_search(some_list):
    name_list=list(contacts_dictionary.data.keys())
    if type(some_list)==str:
        some_list=some_list.strip().split()
    result=[]
    if len(some_list)==1:
        if some_list[0].lower()=="cancel":
            return
        for i in name_list:
            if some_list[0].lower().capitalize() in i:
                result.append(i)
            else:
                pass
    elif len(some_list)==2:
        new_name=" ".join([some_list[0].lower().capitalize(),some_list[1].lower().capitalize()])
        another_name =" ".join([some_list[1].lower().capitalize(),some_list[0].lower().capitalize()])
        if new_name in name_list:
            record = contacts_dictionary.data[new_name]
            return ', '.join([phone.value for phone in record.phones])
        elif another_name in name_list:
            record = contacts_dictionary.data[another_name]
            return ', '.join([phone.value for phone in record.phones])
        for i in name_list:
            if some_list[0].lower().capitalize() in i:
                result.append(f"{i}")
            elif some_list[1].lower().capitalize() in i:
                result.append(f"{i}") 
            else:
                pass
    if len(result)>=1:
        return name_search(input(f'{result} These are the best match what I found for you. Type one of this names to see number you need\n'))
    else:
        return name_search(input('No results were found with such name.Try another name or type "cancel"\n'))
    

def handler(string):
    exit_list=['good bye','close','exit']
    while string.lower() not in exit_list:
        x=parser_command(string)
        if len(x)==1:
            if x[0].lower()=="hello":
                x=input("Hello.How can I help you?:\n")
                return handler(x)
            else:
                return handler(input("Looks like you type something wrong.Please try again,don't forget space between words and use correct commands\n"))
        elif len(x)>1:
            if x[0].lower()=="add":
                if len(x)==4:
                    list2=[]
                    list2.extend(x[1:-1])
                    clean_name=format_name(list2)
                    if clean_name in contacts_dictionary:
                        record = contacts_dictionary.data[clean_name]
                        record.add_phone(sanitize_phone_number(x[-1]))
                    else:
                        record = Record(clean_name, sanitize_phone_number(x[-1]))
                        contacts_dictionary.add_record(record)
                    print(f'Contact dictionary successfully updated with such contact {clean_name}:{sanitize_phone_number(x[-1])}')
                    return handler(input("Would you like to do something else?\n"))
                else:
                    return handler(input('Function "add" accept only such sequence: first name,second name and phone number.Please try again\n'))
            elif x[0].lower()=="phone":
                if len(x)<2 or len(x)>4:
                    return handler(input('Function "change" accept only such sequence: first name and second name.Please try again\n'))
                elif len(x) in [2,3]:
                    list2=[]
                    list2.extend(x[1:])
                    phone_number=name_search(list2)
                    if phone_number==None:
                        return handler(input("Would you like to do something else?\n"))
                    else:
                        print(f'Contact has such number(s):{phone_number}')
                        return handler(input("Would you like to do something else?\n"))
            
            elif x[0].lower()=="change":
                if len(x)==4:
                    list2=[]
                    list2.extend(x[1:3])
                    clean_name=format_name(list2)
                    clean_name2=format_name(" ".join([list2[1],list2[0]]))
                    if clean_name in contacts_dictionary.data.keys():
                        old_phone=contacts_dictionary.data[clean_name]#list
                        if len(old_phone.phones)>=2:
                            old_telephone=input(f"There are few phones for {clean_name}.{[phone.value for phone in old_phone.phones]}.Type one you want to change.")
                            old_phone.change_phone(sanitize_phone_number(old_telephone), sanitize_phone_number(x[-1]))
                            print(f'Contact dictionary successfully updated. {old_telephone} replaced with {sanitize_phone_number(x[-1])}')
                            return handler(input("Would you like to do something else?\n"))
                        else:
                            old_phone.change_phone(old_phone.phones[0].value, sanitize_phone_number(x[-1]))
                            print(f'Contact dictionary successfully updated. Old phone replaced with {sanitize_phone_number(x[-1])}')
                            return handler(input("Would you like to do something else?\n"))
                    elif clean_name2 in contacts_dictionary.data.keys():
                        old_phone=contacts_dictionary.data[clean_name2]#list
                        if len(old_phone.phones)>=2:
                            old_telephone=input(f"There are few phones for {clean_name2}.{[phone.value for phone in old_phone.phones]}.Type one you want to change.")
                            old_phone.change_phone(sanitize_phone_number(old_telephone), sanitize_phone_number(x[-1]))
                            print(f'Contact dictionary successfully updated. {old_telephone} replaced with {sanitize_phone_number(x[-1])}')
                            return handler(input("Would you like to do something else?\n"))
                        else:
                            old_phone.change_phone(old_phone.phones[0].value, sanitize_phone_number(x[-1]))
                            print(f'Contact dictionary successfully updated. Old phone replaced with {sanitize_phone_number(x[-1])}')
                            return handler(input("Would you like to do something else?\n"))
                    else:
                        return handler(input('There are no match for your input. Type "show all" to see all contacts\n'))
                else:
                    return handler(input('Function "change" accept only such sequence: first name,second name and phone number.Please try again\n'))
            elif string.lower() =="show all":
                text_phones = ''
                for name, record in contacts_dictionary.items():
                    text_phones += name + ' ' + ', '.join([phone.value for phone in record.phones]) + '\n'
                print(text_phones)
                return handler(input("Would you like to do something else?\n"))
        else:
            return handler(input("Looks like you type something wrong.Please try again,don't forget space between words\n"))
def main():
    print('Hello. I am bot which works with your phone book.')
    print('[1] Enter "hello" and receive answer "How can I help you?"')
    print('[2] Enter "add ...". With this command I will save in memory new contact(Only Ukraininan Numbers).')
    print('[3] Enter "change ...". With this command I will change number in existing contact.Excepting first or second name')
    print('[4] Enter "phone ....". With this command I will show number of contact that you enter.')
    print('[5] Enter "show all". With this command I will show all numbers existing in your contact list.')
    print('[6] Enter "good bye","close" or "exit" to quit.')
    y = input('How can I help you today?:\n')
    handler(y)
    print("Good bye!")
if __name__ == '__main__':
    main()