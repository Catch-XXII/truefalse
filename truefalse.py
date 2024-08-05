from const import RE_EMAIL, RE_PHONE, DB_NAME
import datetime
from player import Player
from colorama import Fore
import os.path
import random
import time
import re
from db_operations import (
    create_sqlite_database,
    create_table,
    insert_into_table,
    fetch_score_board,
)


def is_valid_email() -> str:
    while True:
        email = input("Enter your email: ")
        match = re.match(RE_EMAIL, email)
        if match is None:
            print("Not a valid E-mail address")
        else:
            return email


def is_valid_phone() -> str:
    while True:
        phone = input("Enter your phone number: ")
        match = re.match(RE_PHONE, phone)
        if match is None:
            print("Not a valid phone number")
        else:
            return phone


def create() -> Player:
    score = 0
    with open(os.path.join("intro.txt"), "r") as file:
        lines = file.read()
        for line in lines:
            print(line, end="")
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
    return Player(name, email, age, phone, score, date)


player = create()
start = time.time()  # game starts here
sign_list = ["<", "=", ">"]
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
    if sign_list.index(sign) == 0 and (
        answer == "T" and left < right or answer == "F" and left > right
    ):
        player.score += 5
        print(f"Correct :) {alert}{player.score}")
    elif sign_list.index(sign) == 1 and (
        answer == "T" and left == right or answer == "F" and left != right
    ):
        player.score += 5
        print(f"Correct :) {alert}{player.score}")
    elif sign_list.index(sign) == 2 and (
        answer == "T" and left > right or answer == "F" and left < right
    ):
        player.score += 5
        print(f"Correct :) {alert}{player.score}")
    else:
        player.score -= 5
        print(f"Wrong :( {alert}{player.score}")
if player.score == 45:
    print(
        Fore.GREEN
        + "Well Done !!! "
        + player.name
        + " You have reached the next level"
        + "\nYour Score is: "
        + str(player.score)
    )
    level += 1

else:
    print(
        Fore.RED
        + "Sorry :( "
        + player.name
        + " you could not reach the maximum score"
        + " Focus (■_■¬) !!!"
        + "\nYour Score is: "
        + str(player.score)
    )
    level -= 1
end = time.time()  # game ends here
hours, rem = divmod(end - start, 3600)
minutes, seconds = divmod(rem, 60)
delta_time = end - start
print(
    "This round was completed in: "
    + "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds)
)

conn = create_sqlite_database(DB_NAME)
insert_into_table(conn, player, delta_time)
fetch_score_board(conn)
