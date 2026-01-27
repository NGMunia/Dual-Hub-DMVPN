

from getpass import getpass

Username = input('Username: ')
password = getpass('password: ')
enable_password = getpass('enable password: ')

while True:
    if Username == "Automation"  and password == "cisco123" and enable_password == "cisco123":
        print('Login successful!!')
        break
    else:
        print("incorrect username and/or password!!")
        sername = input('Username: ')
        password = getpass('password: ')
        enable_password = getpass('enable password: ')

