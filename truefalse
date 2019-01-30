from colorama import Fore
import datetime
import sqlite3
import random
import time
import re

with open('.../PycharmProjects/TrueFalse/intro.txt', 'r') as f:  # don't forget to change the path !!! to your file path
    line = f.read()
    for i in range(len(line)): print(line[i], end=''); time.sleep(0.00125); i += 1
time.sleep(1)
ask = list("\n\nEnter your name: ")
for i in range(len(ask)): print(ask[i], end=''); time.sleep(0.25); i += 1
name = input("").title()
while True:
    email = input('Enter your email: ')
    address_to_verify = email
    match = re.match(r'^[a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', address_to_verify)
    if match is None:
        print('Not a valid E-mail address')
    else:
        break
age = input("Enter your age: ")
while True:
    phone = input("Enter your phone number: ")
    phone_to_verify = phone
    match = re.match(r'^([0-9]( |-)?)?(\(?[0-9]{3}\)?|[0-9]{3})( |-)?([0-9]{3}( |-)?[0-9]{4}|[a-zA-Z0-9]{7})$', phone_to_verify)
    if match is None:
        print('Not a valid phone number')
    else:
        break
date = datetime.datetime.now()
print("Hello " + " {} \nDateTime: {:%Y/%m/%d %H:%M:%S}".format(name.upper(), date))
sign_list = ['<', '=', '>']
alert = "Your score is: "
score = 0
level = 9
i = 0
start = time.time()  # game starts here
while i < level:
    left = random.randint(1, 1001)
    sign = random.choice(sign_list)
    right = random.randint(1, 1001)
    print('{0}{1}{2}'.format(left, sign, right))
    i += 1
    answer = input("True or False: ").upper()
    if sign_list.index(sign) == 0 and (answer == "T" and left < right or answer == "F" and left > right):
        score += 5
        print("Correct :) {0}{1}".format(alert, score))
    elif sign_list.index(sign) == 1 and (answer == "T" and left == right or answer == "F" and left != right):
        score += 5
        print("Correct :) {0}{1}".format(alert, score))
    elif sign_list.index(sign) == 2 and (answer == "T" and left > right or answer == "F" and left < right):
        score += 5
        print("Correct :) {0}{1}".format(alert, score))
    else:
        score -= 5
        print("Wrong   :( {0}{1}".format(alert, score))
if score == 45:
    print(Fore.GREEN + "Well Done !!! " + name + " You have reached the next level" + "\nYour Score is: " + str(score))
    level += 1

else:
    print(Fore.RED + "Sorry :( " + name + " you could not reach the maximum score" + " Focus on (■_■¬) !!!" + "\nYour Score is: " + str(score))
    level -= 1
end = time.time()  # game ends here
hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)
elapsed_time = end - start
print("This round was completed in: " + "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))
try:
    connection = sqlite3.connect('playerdb.db')
    cursor = connection.cursor()
    cursor.execute('insert into player (name, email, age, phone, score, duration, date) values(?, ?, ?, ?, ?, ?, ?)', (name, email, age, phone, score, elapsed_time, date))
    # cursor.execute('''create table player(id integer primary key, name text not null, email text unique not null, age integer not null, phone text unique not null, score integer not null,
    # duration real not null, date datetime not null);''')
    cursor.execute('select * from player order by duration asc')
    rows = cursor.fetchall()
    print("{:-^4s}{:_^30s}{:@^30s}{:-^7s}{:#^12s}{:-^9s}{:*^12s}{:~^26s}".format('No', 'Name', 'E-mail', 'Age', 'Number', 'Score', 'Duration', 'Date'))
    for row in rows:
        print("{:^4d}{:<30s}{:<30s}{:^7d}{:<12s}{:^9d}{:^12.2f}{:^26s}".format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

    connection.commit()
except Exception as e: connection.rollback(); raise e
finally: connection.close()

