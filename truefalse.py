from colorama import Fore
from Player import Player
import datetime
import sqlite3
import random
import time
import re
import os.path


def is_valid_email() -> str:
    while True:
        email = input('Enter your email: ')
        match = re.match(r'^[a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
        if match is None:
            print('Not a valid E-mail address')
        else:
            return email

def is_valid_phone() -> str:
     while True:
        phone = input("Enter your phone number: ")
        match = re.match(r'^([0-9]( |-)?)?(\(?[0-9]{3}\)?|[0-9]{3})( |-)?([0-9]{3}( |-)?[0-9]{4}|[a-zA-Z0-9]{7})$', phone)
        if match is None:
            print('Not a valid phone number')
        else:
            return phone


def create() -> Player:
    score = 0
    with open(os.path.join("intro.txt"), 'r') as file:
        lines = file.read()
        for line in lines:
            print(line, end='')
            time.sleep(0.00125)
        time.sleep(1)
    
    ask = "\n\nEnter your name: "
    
    for letter in ask: 
        print(letter, end="") 
        time.sleep(0.25)

    name = input("").title()
    email = is_valid_email()
    age = input("Enter your age: ")
    phone = is_valid_phone()
    date = datetime.datetime.now()
    print(f"Hello {name.title()} DateTime: {date:%Y/%m/%d %H:%M:%S}")
    player = Player(name, email, age, phone, score, date)
    return player


player = create()
start = time.time()  # game starts here
sign_list = ['<', '=', '>']
alert = "Your score is: "
level = 9
i = 0
while i < level:
    left = random.randint(1, 1001)
    sign = random.choice(sign_list)
    right = random.randint(1, 1001)
    print(f"{left}{sign}{right}")
    i += 1
    answer = input("True or False: ").upper()
    if sign_list.index(sign) == 0 and (answer == "T" and left < right or answer == "F" and left > right):
        player.score += 5
        print(f"Correct :) {alert}{player.score}")
    elif sign_list.index(sign) == 1 and (answer == "T" and left == right or answer == "F" and left != right):
        player.score += 5
        print(f"Correct :) {alert}{player.score}")
    elif sign_list.index(sign) == 2 and (answer == "T" and left > right or answer == "F" and left < right):
        player.score += 5
        print(f"Correct :) {alert}{player.score}")
    else:
        player.score -= 5
        print(f"Wrong :( {alert}{player.score}")
if player.score == 45:
    print(Fore.GREEN + "Well Done !!! " + player.name + " You have reached the next level" + "\nYour Score is: " + str(player.score))
    level += 1

else:
    print(Fore.RED + "Sorry :( " + player.name + " you could not reach the maximum score" + " Focus (■_■¬) !!!" + "\nYour Score is: " + str(player.score))
    level -= 1
end = time.time()  # game ends here
hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)
elapsed_time = end - start
print("This round was completed in: " + "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))
try:
    
    connection = sqlite3.connect('playerdb.db')
    cursor = connection.cursor()

    # cursor.execute('''create table player(id integer primary key, 
    # name text not null, 
    # email text unique not null, 
    # age integer not null, 
    # phone text unique not null, 
    # score integer not null,
    # duration real not null, 
    # date datetime not null);''')
    
    cursor.execute('insert into player (name, email, age, phone, score, duration, date) values(?, ?, ?, ?, ?, ?, ?)', (player.name, 
                                                                                                                       player.email, 
                                                                                                                       player.age, 
                                                                                                                       player.phone, 
                                                                                                                       player.score, 
                                                                                                                       elapsed_time, 
                                                                                                                       player.date))

    cursor.execute('select * from player order by duration asc')
    rows = cursor.fetchall()
    print("{:-^4s}{:_^30s}{:@^30s}{:-^7s}{:#^12s}{:-^9s}{:*^12s}{:~^26s}".format('No', 'Name', 'E-mail', 'Age', 'Number', 'Score', 'Duration', 'Date'))
    for row in rows:
        print("{:^4d}{:<30s}{:<30s}{:^7d}{:<12s}{:^9d}{:^12.2f}{:^26s}".format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

    connection.commit()

except Exception as e: 
    connection.rollback()
    raise e
finally: 
    connection.close()
