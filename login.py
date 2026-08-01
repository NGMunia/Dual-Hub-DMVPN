

# Login credentials used to access the network devices via SSH
# Netmiko uses these credentials to log in into the devices remotely

from getpass import getpass

Username = input('Username: ')
password = getpass('password: ')
enable_password = getpass('enable password: ')

while True:
    if Username == "Automation"  and password == "cisco123" and enable_password == "cisco123":
        print('Login successful!!')
        break
    else:
        print("Incorrect username and/or password!!")
        Username = input('Username: ')
        password = getpass('password: ')
        enable_password = getpass('enable password: ')

