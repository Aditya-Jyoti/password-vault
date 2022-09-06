import random
import re 
import sys
import json
from typing import Optional, List
from string import ascii_lowercase, digits, punctuation

COLLECTION = ascii_lowercase + ascii_lowercase.upper() + digits + punctuation
OPTIONS = [
    "\t1) Generate and save a new password to database",
    "\t2) Save an existing password to the databse",
    "\t3) Edit information about a database entry",
    "\t4) Delete a database entry",
    "\t5) View database in tabular form"
]

# Minimum password requirements
#   1) minimum 8 characters
#   2) atleast 1 lowercase character 
#   3) atleast 1 uppercase character 
#   4) atleast 1 special character 
#   5) atleast 1 number 
#   6) no whitespace charaters 
#
# Database entry format
# {
#   website_name1: {password1: username1},
#   website_name2: {password2: username2},
# }

def read_content() -> dict:
    try:
        with open(r"PasswordVault.txt", "r") as file:
            obj = json.load(file)
            return obj 
    except json.decoder.JSONDecodeError:
        with open(r"PasswordVault.txt", "w") as file:
            obj = json.dumps({}, indent=4)
            file.write(obj)
        return read_content()

def write_content(data: dict) -> Optional[bool]:
    try:
        with open(r"PasswordVault.txt", "w") as file:
            obj = json.dumps(data, indent= 4)
            file.write(obj)
            return True

    except FileNotFoundError:
        return

def convert_dict_to_list(data: dict) -> List[List[str]]:
    main_list = [["S.NO", "WEBSITE", "USERNAME", "PASSWORD"]]

    for idx, entry in enumerate(data, start=1):
        sub_list = []
        sub_key = list(data[entry].keys())[0]
        
        sub_list.append(str(idx))
        sub_list.append(entry)
        sub_list.append(data[entry][sub_key])
        sub_list.append(sub_key)
        
        main_list.append(sub_list)

    return main_list

def printer(data: dict) -> int:
    table = convert_dict_to_list(data)

    width = [max([len(x[i]) for x in table]) for i in range(len(table[0]))]
    header = table.pop(0)
    
    for i in width:
        print("+-" + "-".center(i, "-"), end = "-+")
    print()
    
    for i, elem in enumerate(header):
        print("| " + elem.center(width[i], " "), end = " |")
    print()
    
    for i in width:
        print("+-" + "-".center(i, "-"), end = "-+")
    print()

    for row in table:
        for i, elem in enumerate(row):
            print("| " + elem.center(width[i], " "), end = " |")
        print()

    for i in width:
        print("+-" + "-".center(i, "-"), end = "-+")
    print()

    return len(width)

def generate_password(length: int) -> Optional[str]:
    if length < 8:
        return 
    
    password = "".join(random.sample(COLLECTION, length))
    if re.match(r"[a-zA-Z0-9!\"#$%&\'()*+,\-.\/:;<=>?@\[\\\]^_`\{|\}~\']", password):
        return password
    else: return generate_password(length)

def ask_starting_choice() -> int:
    print("Valid options and their purposes")
    for option in OPTIONS:
        print(option)
    
    print("Please enter the number corresponding to your choice")
    user_input = int(input(">>> "))

    if not 1 <= user_input <= len(OPTIONS):
        print("Please select a number from the provided list of choices only\n")
        return ask_starting_choice()

    return user_input

def ask_pass_length() -> int:
    pass_length = int(input("Please enter in ur length of password (min 8 char)\n>>> "))
    if 8 >= pass_length:
        return ask_pass_length()
    return pass_length

def ask_website_name() -> str:
    return input("Please enter the name of the website\n>>> ")

def ask_username() -> str:
    return input("Please enter your username for the website\n>>> ")

def ask_old_password() -> str:
    return input("Please enter your pre-existing password\n>>> ")

def ask_rerun_program() -> bool:
    choice = input("Would you like to rerun the program? [yes/no]\n>>> ")
    if "y" not in choice.lower():
        print("EXITING THE PROGRAM")
        sys.exit(0)

    print("\nRERUNNING THE PROGRAM\n")
    return True

def choice_one_two(starting_choice: int):
    if starting_choice == 1:
        pass_length = ask_pass_length()
        password = generate_password(pass_length)
    else:
        password = ask_old_password()

    website_name = ask_website_name()
    username = ask_username()
    
    print()
    print(f"Generated password:  {password}")
    print(f"Website name:        {website_name}")
    print(f"Username:            {username}")
    print()

    choice = input("Are you satisfied with the above entries? [yes/no]\n>>> ")
    if "y" not in choice.lower():
        print("\nRERUNNING THE PROGRAM\n")
        main(1)

    data = read_content()
    if website_name in data.keys():
        print(f"There is already a database entry for the given website {website_name}")
        choice = input("Do you wish to continue? [yes/no]\n>>> ")
        if "y" not in choice.lower():
            print("\nRERUNNING THE PROGRAM\n")
            main(1)
        else:
            print("\nCONTINUING THE PROGRAM\n")

    data[website_name] = {password: username}
    
    if write_content(data) is not True:
        print("Failed to save information to the database\n\nSTOPPING THE PROGRAM\n")
        sys.exit(0)

    else:
        print("Successfully saved the information to the database")

def display_database() -> int:
    data = read_content()
    sno = printer(data)
    return sno
    

def main(user_input: int = -1):
    if user_input == -1:
        user_input = ask_starting_choice()

    if user_input == 1:
        choice_one_two(1)    
    
    if user_input == 2:
        choice_one_two(2)

    if user_input == 3:
        len_table = display_database()
        print()
        sno = int(input("Select the S.NO of the entry to change\n>>> "))
        if not 1 <= sno <= len_table: 
            print("Please select a valid S.NO to edit\n>>> ")
            main(3)
        
        data = read_content()
        key = list(data)[sno - 1]

        print("What would you like to change?")
        print("1) Website name")
        print("2) Password")
        print("3) Username")

        choice = int(input("Please make a choice\n>>> "))
        while not 1 <= choice <= 3:
            choice = int(input("Please make a choice\n>>> "))
        
        if choice == 1:
            new_website = input("Please input the new website name\n>>> ")
            key_list = list(data)
            key_list.insert(sno - 1, new_website)
            key_list.pop(sno)
            
            zipped_data = zip(key_list, data.values())
            new_data = {}
            for k, v in zipped_data:
                new_data[k] = v
            
            write_content(new_data)
            print("Updated the database")
        
        if choice == 2:
            new_password = input("Please input the new password\n>>> ")
            entry = data[key]
            entry_username = list(entry.values())[0]
            entry = {new_password: entry_username}
            data[key] = entry
            
            write_content(data)
            print("Updated the database")

        if choice == 3:
            new_username = input("Please input the new username\n>>> ")
            entry = data[key]
            entry[list(entry)[0]] = new_username
            data[key] = entry

            write_content(data)
            print("Updated the database")

    if user_input == 4:
        len_table = display_database()
        print()
        sno = int(input("Select the S.NO of the entry to delete\n>>> "))
        if not 1 <= sno <= len_table: 
            print("Please select a valid S.NO to delete\n>>> ")
            main(4)
        
        data = read_content()
        key = list(data)[sno - 1]
        
        del data[key]
        write_content(data)
        print("Deleted the entry")

    if user_input == 5:
        display_database()

    if ask_rerun_program():
        main()

if __name__ == "__main__":
    print("password vault")
    main()
