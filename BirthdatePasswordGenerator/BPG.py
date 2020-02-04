import itertools
import os

months = ["january", "february", "march", "april", "may", "june",
          "july", "august", "september", "october", "november", "december"]


def display_only(info):
    for data in info:
        print(data)


def save_file(info):
    directory = input('\nWhere do you want to write the file (Example: C:\\Users\John\Desktop): ')
    while not os.path.exists(directory):
        print('\nPath does not exist, please enter a valid path to a directory\n')
        directory = input("\nWhere do you want to write the file ")
    else:
        file = open(directory + '\\' + "bpg_password_list.txt", 'w')

        for password in info:
            file.write(password + '\n')
        file.close()


def display_save(info):  # Displays the output and saves it in a file
    display_only(info)
    save_file(info)


def display_save_options(info):
    print("How would you like the passwords to be outputted?"
          "\n1.Display on screen only"
          "\n2.Display on screen and save in file"
          "\n3.Save in file only")

    while True:
        try:
            chosen_output_type = int(input('\nChoice: '))
            if chosen_output_type == 1:
                display_only(info)
                break
            elif chosen_output_type == 2:
                display_save(info)
                break
            elif chosen_output_type == 3:
                save_file(info)
                break
            else:
                print("Please choose from the given options [1/2/3]")
        except:
            print("Invalid Input, Please only enter numbers")


def format_dates(info):
    day = info[0]
    if int(day) < 10:
        day_one_digit = day[1]
    else:
        day_one_digit = day
    month = info[1]
    month_capitalized = month.capitalize()
    month_uppercase = month.upper()
    month_shortcut = month[0:3]  # Converts month to a shorter form (Example: February --> Feb)
    month_shortcut_capitalized = month_shortcut.capitalize()
    month_shortcut_uppercase = month_shortcut.upper()
    year = info[2]
    year_two_digits = year[2:4]  # Converts year from 4 digits to 2 (Example: 2017 --> 17)
    if months.index(month) < 10:
        month_number = '0' + str(months.index(month) + 1)  # Gets the number of the month (Example: April --> 04)
        month_one_digit = str(month.index(month))  # Example: April --> 4
    else:
        month_number = str(months.index(month) + 1)  # Example: December --> 12
        month_one_digit = str(months.index(month))

    return [[day, day_one_digit], [month, month_capitalized, month_uppercase, month_shortcut, month_shortcut_uppercase,
                                   month_shortcut_capitalized, month_one_digit, month_number], [year, year_two_digits]]


def find_all_permutations(info):
    output = []
    dates_combination = list(itertools.product(*info))
    for date in dates_combination:
        for d in itertools.permutations(date):
            if d not in output:
                output.append(d)

    return output


def format_names(info):
    output = []
    for name in info:
        output.append([name, name.upper(), name.capitalize()])
    return output


def convert_password_to_string(output, pass_list):
    for password in pass_list:  # "password" represents the list of the possible combination of the given date
        password_string = password[0] + password[1] + password[2]
        if password_string not in output:
            output.append(password_string)


def generate_password_no_name(info):
    output = []
    dates = format_dates(info)
    data = find_all_permutations(dates)  # List containing lists of all possible passwords of the given date
    convert_password_to_string(output, data)
    return output


def generate_password(date_info, name_info):
    output = []
    data = []  # contains information needed for generating the passwords
    dates = format_dates(date_info)
    names = format_names(name_info)
    data += names
    data += dates
    passwords = find_all_permutations(data)
    convert_password_to_string(output, passwords)
    return output


def password_with_name():
    names = []
    birth_date = password_with_bd(True)
    while True:
        first_name = input("\nFirst Name: ")
        last_name = input("Last Name or Family name (Leave empty if you do not want to use a last name): ")

        if (first_name.isspace() or first_name == '') and (last_name.isspace() or last_name == ''):
            print("\nPlease provide at least one name\n")
            continue
        all_names = [first_name.lower(), last_name.lower()]
        print('\nAre you sure of the following information:')
        counter = 0
        for name in all_names:
            if not name.isspace() and name != '':
                counter += 1
                names.append(name)
                print(str(counter) + '. ' + name)
        confirmation = input('\nChoice: ')
        if confirmation.lower() == 'yes':
            pass
        elif confirmation.lower() == 'no':
            print('\n Discarding previous information\n')
        else:
            print('\n Please either enter Yes or No only and try again\n')
            continue

        print("\n\n\tGENERATING...\nTHIS MAY TAKE A WHILE\n\t")
        display_save_options(generate_password(birth_date, names))
        print("\n\n\tDONE\n\n\t")
        break


def password_with_bd(name_given):  # bd stands for birth date
    while True:
        print("\nPlease Provide the following birth date information:")
        chosen_year = input("Year: ")
        chosen_month = input("Name of month: ")
        chosen_day = input("Day (Example: 01, 10, 28 ...):  ")

        print("\nAre you sure of the following information:"
              "\nDay: " + chosen_day +
              "\nMonth: " + chosen_month +
              "\nYear: " + chosen_year)

        confirmation = input('\nChoice: ')
        if confirmation.upper() == 'NO':
            print("Discarding previous information")
        elif confirmation.upper() == 'YES':
            try:
                if int(chosen_day) > 31 or len(chosen_day) != 2:
                    print('\nPlease enter a valid day (Examples: 13, 02, 08, 28)')
                elif chosen_month.lower() not in months:
                    print('\nPlease enter a valid name of a month')
                elif len(chosen_year) != 4:
                    print('\nPlease enter a valid year (Example: 1989)')
                else:
                    info = [chosen_day, chosen_month, chosen_year]
                    if name_given:
                        return info
                    else:
                        print("\n\n\tGENERATING...\n\n\t")
                        info = [chosen_day, chosen_month, chosen_year]
                        display_save_options(generate_password_no_name(info))
                        print("\n\n\tDONE\n\n\t")
                        break
            except:
                print('\nAn Error Occurred, Please make sure that you have entered valid inputs')
        else:
            print('\nInvalid Input, Please only enter Yes or No')


def main_func():
    print("Birthday Password Generator v 1.0\n\n"
          "Please Select one of the following Options:"
          "\n1.Generate passwords with name and birth date"
          "\n2.Generate passwords with only birth date")
    while True:
        try:
            user_choice_password = int(input("\nChoice: "))
            if user_choice_password == 1:
                password_with_name()
                break
            elif user_choice_password == 2:
                password_with_bd(False)
                break
            else:
                print("Please choose from the given options [1/2]")
        except TypeError:
            print("Invalid Input, Please only enter numbers")


try:
    main_func()
except:
    print('\nAn Error has occurred, please restart the program and try again')
