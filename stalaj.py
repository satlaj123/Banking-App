from datetime import date, datetime
import json
from math import ceil
import random
import re
from logging import *


userData = {}
AccountNumberList = []
Log_Format = "%(levelname)s %(asctime)s - %(message)s"
basicConfig(filename = '/Users/300074956/Satlaj/LogFile/logs.txt', filemode = "a", format = Log_Format, level = DEBUG)

class Account :
   def createAccount(self):
       accNo = ceil(random.random()*10000)
       firstName = input('\tEnter your first name : ')
       lastname = input('\tEnter your last name : ')
       birthday = input('\tEnter your date of birth [YYYY-MM-DD]: ')
       match = re.search(r'\d{4}-\d{2}-\d{2}', birthday)
       bday = datetime.strptime(match.group(), '%Y-%m-%d').date()
       age = calculateAge(date(bday.year, bday.month, bday.day))
       balance = 1000
       userData[accNo] = dict({"First Name": firstName, "Last Name": lastname, "DOB": str(bday), "Deposit": balance, "Last withdrawl Amount":'0', "Age": age})
       AccountNumberList.append(accNo)
       print('\nAccount Created Successfully. Your account number is '+str(accNo))
       info('\nAccount Created Successfully. Your account number is '+str(accNo))
       return accNo

def intro():
    info("BANK MANAGEMENT SYSTEM is Activated.")
    readDataFromAccountsFile()
    readAllUserData()
    print()
    print('\t\t\t\tBANK MANAGEMENT SYSTEM')
    print()


def writeAccount():
    account = Account()
    accNo = account.createAccount()
    writeDataInFile(accNo)
    writeDataInAccountsFile(accNo)


def checkIfExist(num):
    for i in AccountNumberList:
        if num == i:
            return True
    warning("Account does not exist.")
    return False


def depositAndWithdraw(num1,num2): 

    for i in userData:
    #    print(userData[i])
       if i == num1:
           if num2 == 1 : 
                amount = int(input('Enter the amount to deposit : ')) 
                userData[i]['Deposit'] += amount 
                print('\nAmount '+ str(amount) +' Deposited Successfully for Account No.- ' +str(i)) 
                writeDataInFile(i)
                info('\nAmount '+ str(amount) +' Deposited Successfully for Account No.- ' +str(i))

           elif num2 == 2 : 
                amount = int(input('Enter the amount to withdraw : ')) 
                if amount <= userData[i]['Deposit'] : 
                    userData[i]['Deposit'] -= amount  
                    userData[i]['Last withdrawl Amount'] = str(amount)
                    writeDataInFile(i)
                    print('\nAmount '+ str(amount) +' Withdrawn Successfully for Account No.- '+str(i))
                    info('\nAmount '+ str(amount) +' Withdrawn Successfully for Account No.- '+str(i))
                else : 
                    print('You cannot withdraw larger amount')
                    warning('You cannot withdraw larger amount')


def calculateAge(birthDate):
    today = date.today()
    age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
    return age


def writeDataInFile(num):
    filePath = '/Users/300074956/Satlaj/AccountsData/'+ str(num) +'.txt'
    with open(filePath,'w') as f:
        f.write(str(json.dumps(userData[num])))


def readDataFromFile(num):
    filePath = '/Users/300074956/Satlaj/AccountsData/'+ str(num) +'.txt'
    with open(filePath,'r') as f:
        for line in f:
            print(line,end='')
            variable = str(line)
            res = json.loads(variable)
            userData[num] = dict(res)


def writeDataInAccountsFile(num):
    filePath = '/Users/300074956/Satlaj/AccountsData/AccountsList.txt'
    with open(filePath,'a') as f:
        f.write(str(json.dumps(num))+'\n')


def readDataFromAccountsFile():
    filePath = '/Users/300074956/Satlaj/AccountsData/AccountsList.txt'
    try:
        with open(filePath,'r') as f:
            for line in f:
                print(line,end='')
                variable = str(line)
                res = json.loads(variable)
                AccountNumberList.append(int(res))
    except FileNotFoundError:
        print("No Previous Data Found")
        error("No Previous Data Found")
        return


def readAllUserData():
    for i in AccountNumberList:
        readDataFromFile(i)


# start of the program 
ch='' 
num=0 
intro() 
print(AccountNumberList)
while ch != 8: 
    print('\t\t\t\tMAIN MENU') 
    print('\t\t\t\t1. NEW ACCOUNT') 
    print('\t\t\t\t2. DEPOSIT AMOUNT') 
    print('\t\t\t\t3. WITHDRAW AMOUNT') 
    print('\t\t\t\t4. BALANCE ENQUIRY') 
    print('\t\t\t\t5. EXIT') 
    print('\t\t\t\tSelect Your Option (1-5) ') 
    ch = input('Enter your choice : ')

    if ch == '1': 
        writeAccount() 
    elif ch =='2': 
        num = int(input('\tEnter The account No. : ')) 
        depositAndWithdraw(num, 1) if checkIfExist(num) else print('Account Number doesn"t exist')
    elif ch == '3':
        num = int(input('\tEnter The account No. : ')) 
        depositAndWithdraw(num, 2) if checkIfExist(num) else print('Account Number doesn"t exist')
    elif ch == '4': 
        num = int(input('\tEnter The account No. to fetch data : ')) 
        info("User requested his account details.")
        readDataFromFile(num) if checkIfExist(num) else print('Account Number doesn"t exist')
    else : 
        print('\tThanks for using bank management system') 
        break  
    print()