# Author Muhammad Faheem Khan
# Date: 12/12/2017
# File name: ca.py
# Description: This program allow the user to create timetable for any number of days.

# Importing Modules
from prettytable import PrettyTable
import datetime
import sys
import os
import send_mail as sm # I made this one

# Ptabe Object
ptable = PrettyTable()

# this function get the hours from the user and makes sure they are error free
def get_hour():
    t = input("Enter Hour in 24 hour format \nBetween 0 and 23\nPress enter key to set minutes to 00 \nHour: ")
    if len(t) == 0:
        t = 0
        return t
    else:
        try:
            t = int(t)
            if 0 <= t <= 23:
                return t
            else:
                print("Enter a number between 0 and 24")
                return get_hour()
        except ValueError:
            print("Enter a valid input")
            return get_hour()

# this function get the minutes from the user and makes sure they are error free
def get_mins():
    m = input("Enter Minutes \nPress enter key to set the minutes to 00 \nMinutes: ")
    if len(m) == 0:
        m = 00
        return m
    else:
        try:
            m = int(m)
            if 0 <= m <= 59:
                return m
            else:
                print("Enter a number between 0 and 59")
                return get_mins()
        except ValueError:
            print("Enter a valid number")
            return get_mins()

# this function checks if the year entered is a leap year or not
# depending on the year returns a list containing number of days per month
def calc_leap_year(year):
    normal = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if (year % 400 == 0):
        leap = normal.copy()
        leap[1] == 28
        return leap
    else:
        return normal

# this function gets the year from the user
def get_year():
    ui = input("Enter year, Exmaple 2017\nYear: ")
    if (ui.isdigit() and len(ui)==4):
        ui = int(ui)
        if (ui >= 2017):
            return ui
        else:
            print("Enter a valid year")
            return get_year()
    else:
        print("Enter a valid year")
        return get_year()

# this function get the month from the user in numbers
def get_month():
    ui = input("Enter the month you want to add tasks to. \nExample = 1 or 5 \nMonth: ")
    if (ui.isdigit() and 1<=len(ui)<=2):
        ui = int(ui)
        if (1<=ui<=12):
            ui = "0" + str(ui)
            return ui
        else:
            print("Enter a valid month")
            return get_month()
    else:
        print("Enter a valid month")
        return get_month()

# this function gets the day from the user
def get_day(month):
    ui = input("Enter the day you want to add tasks to. Example 1 or 23\nDay:")
    if (ui.isdigit() and 1<=len(ui)<=2):
        ui = int(ui)
        if 0 <= ui <= month:
            if 1<=ui<=9:
                ui = "0" + str(ui)
                return ui
            else:
                return ui
        else:
            print("Invalid Day")
            return get_day(month)
    else:
        print("Enter a valid day")
        return get_day(month)

# this function calls get_year(), get_month(), get_day(), calc_leap_year() functions
# generates a date DAY/MONTH/YEAR format
def get_date():
    year = get_year()
    leap_year = calc_leap_year(year)
    month = int(get_month())
    day = get_day(leap_year[month-1])
    date = str(day) + "-" + str(month) + "-" + str(year)
    return date

# this function get what activity the user will be doing
def get_activity():
    ui = input("Enter a brief summary of what you will be doing. \n: ")
    return ui

# this function asks the user if they want to continue adding tasks to the list
# based on the option returns True or False
def add_more():
    ui = input("Do you want to add more? \n1) Yes \n2) No \n:")
    if ui == "1":
        return True
    elif ui == "2":
        return False
    else:
        print("Enter a valid option")
        return add_more()

# this function just gets the email address from the user
def get_email():
    email = input("Please enter your email for me to email you a copy of you schedule for today\nNOTE: If you have a microsoft account email will not be sent\n:")
    flag = True
    while flag:
        if len(email) >= 5:
            if email.find("@") == -1:
                flag = True
            else:
                return email
        else:
            flag = True
            print("Enter a working email!!")

# this function write the tasks to the file in format Date/Time/Task
def write_to_file(data):
    fname = str(min(data[0])) + " - " + str(max(data[0])) + ".txt" # getting the starting and ending days
    with open(fname, "w") as f:
        for i in range(len(data[2])):
            content = str(data[0][i]) + "/" + str(data[1][i]) + "/" + data[2][i] + "\n"
            f.write(content)
    # sending the mail
    sm.send_mail(get_email(), fname) # calling the send mail function
    print("email sent")
    menu() # going to the main function

# this function is where everything happens
def main(date, time, activity):
    flag = True # flag
    while flag:
        d = get_date() # getting date
        date.append(d) # appending date to date array
        hour = get_hour() # getting hour from user
        mins = get_mins() # getting minutes from user
        hours_mins = str(hour) + ":" + str(mins) # putting the hours and mins together Hours:Minutes format
        time.append(hours_mins) # appending hours and minutes to time array
        activity.append(get_activity()) # asking the user for their task and appending to the activity array
        flag = add_more() # asking if the user want to add more task or not
        if flag == True:
            main(date, time, activity) # if the user wants to add more tasks calling the main function and passing date, time, activity array
        else:
            data = [] # creating a array data
            # appending date, time and activity to data to create a 3d Array
            data.append(date)
            data.append(time)
            data.append(activity)
            write_to_file(data) # calling the write_to_file() and passing data
            menu() # calling the menu function

def get_filename(files):
    for i in range(len(files)):
        print(str(i) + " - " + files[i])
    ui = input("Enter the number beside the file you wish to open\n:")
    try:
        ui = int(ui)
        flag = True
        while flag:
            if ui > len(files):
                print("Invalid input")
                return get_filename(files)
            else:
                return ui

    except ValueError:
        print("Invalid input")
        return get_filename(files)

def sort_file_data():
    try:
        f_cwd = os.listdir()
        possible_files = []
        for i in f_cwd:
            if ".txt" in i:
                if i[0].isdigit():
                    possible_files.append(i)
                else:
                    pass
            else:
                pass
        fname = possible_files[get_filename(possible_files)]
        f_content = []
        with open(fname, "r+") as f:
            content = f.readlines()
            for i in content:
                # print(i)
                i = i.replace("\n", "")
                i = i.split("/")
                f_content.append(i)
        flag = True
        while flag:
            ui = input("Sort Data by \n1) Date \n2) Time \n3) Activity \n:")
            if ui == "1":
                print("Sorted by Time")
                f_content = sorted(f_content, key=lambda x: x[0]) # sorting based on the first array [[x][]] of 2d array
                content_copy = f_content.copy() # making a copy of the content file
                ptable.field_names = ["Date", "Time","Activity"]
                for i in range(len(content_copy)):
                    ptable.add_row(content_copy[i])
                    # print(str(content_copy[i][0]) + " - " + str(content_copy[i][1]) + " - " + str(content_copy[i][2]))
                print(ptable)
                ptable.clear_rows()
                menu()
            elif ui == "2":
                print("Sorted by Time")
                f_content = sorted(f_content, key=lambda x: x[1]) # sorting based on the second array [[][x]] of the 2d array
                content_copy = f_content.copy()
                ptable.field_names = ["Date", "Time","Activity"]
                for i in range(len(content_copy)):
                    ptable.add_row(content_copy[i])
                    # print(str(content_copy[i][0]) + " - " + str(content_copy[i][1]) + " - " + str(content_copy[i][2]))
                print(ptable)
                ptable.clear_rows()
                menu()
            elif ui == "3":
                print("Sorted by Activity")
                f_content = sorted(f_content, key=lambda x: x[2]) # sorting based on the second array [[][x]] of the 2d array
                content_copy = f_content.copy()
                ptable.field_names = ["Date", "Time","Activity"]
                for i in range(len(content_copy)):
                    ptable.add_row(content_copy[i])
                    # print(str(content_copy[i][0]) + " - " + str(content_copy[i][1]) + " - " + str(content_copy[i][2]))
                print(ptable)
                ptable.clear_rows()
                menu()
            else:
                print("Enter a valid input")
    except OSError:
        print("No Data Found")

# menu function from where everything is called from
def menu():
    # declaring arrays
    date = []
    time = []
    activity = []
    # asking the user for what option they want to pikc
    ui = input("Menu \n1) Create Timetable for tommorrow \n2) Help \n3) View Data Sorted by Time \n4) Exit \n:")
    if ui == "1":
        main(date, time, activity) # calling the main function and passing data, time, acts
        menu()
    elif ui == "2": # help function
        print("This timetable allows the user to their timetable for the any number of days. Follow the instructions, Use the option number beside the option to navigate.")
        menu()
    elif ui == "3": # sorting file data
        sort_file_data()
        menu()
    elif ui == "4": # exiting the program
        sys.exit(0)
    else: # if the user enter invalid option
        print("Enter a valid option")
        menu()
menu()
