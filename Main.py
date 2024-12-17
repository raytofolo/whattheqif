import os
import csv
import argparse
from datetime import datetime

#set filepath to where input and output files live
absolute_path = os.path.dirname(__file__)
relative_path = "data"
full_path = os.path.join(absolute_path, relative_path)

config_file ="config.txt"
config_path = os.path.join(relative_path, config_file)

acct_file ="account_map.txt"
acct_path = os.path.join(relative_path, acct_file)

securities_file ="security_map.txt"
securities_path = os.path.join(relative_path, securities_file)

#declare dictionary of lookup strings used for various values mapped in Quicken
with open(config_path, 'r') as file:
    lines = file.readlines()
    variables = {}
    for line in lines:
        line = line.strip()
        if line:
            variable_name, value = line.split(" = ")
            variables[variable_name] = eval(value)
print('Configuration file successfully loaded.')

#declare dictionary of lookup strings used to map accounts referenced in the institutions download file to those accounts in Quicken
with open(acct_path, 'r') as file:
    lines = file.readlines()
    lookup_acct = {}
    for line in lines:
        key, value = line.strip().split(':')
        lookup_acct[key.strip()] = value.strip()
    print('Account mapping successfully created.')

#declare dictionary of lookup strings used to map accounts or actions in CSV to accounts or actions used by Quicken
with open(securities_path, 'r') as file:
    lines = file.readlines()
    lookup_security = {}
    for line in lines:
        key, value = line.strip().split(':')
        lookup_security[key.strip()] = value.strip()
    print('Securities mapping successfully created.')

#declare variables used as lists which will define how transactions are "handled", meaning how to accomodate different 
#Quicken data requirements based on the transaction type
handle_dividend = ["Div"]
handle_transfer = ["XIn", "XOut"]
handle_interest = ["IntInc"]
handle_shares = ["Buy", "Sell"]
handle_investment_fees = ["MiscExp"]

#This dictionary is Altruist-specific.  It maps the action codes from the Altruist download to the action codes Quicken understands.
lookup_action = {
    "Dividend": "Div",
    "Buy": "Buy",
    "Sell": "Sell",
    "Interest": "IntInc",
    "Fee": "MiscExp",
    "Deposit": "XIn",
    "Withdrawl": "XOut" 
}



#define the columns being read from the input CSV file.  Each col value is listed here.
def print_row(rowNr, date, account, type, symbol, description, status, quantity, price, amount):
    print(
        f"{str(rowNr):<3} | "
        f"{str(date):<10}    | "
        f"{str(account):>55} | "
        f"{str(type):>22} | "
        f"{str(symbol):>10} | "
        f"{description:<35} | "
        f"{str(status):<9} | "
        f"{str(quantity):>10} | "
        f"{str(price):>7} | "
        f"{str(amount):>13} | "
    )

#define the function to take the input CSV and create the output QIF
def csv2qif(input_file='input.csv', output_file='output.qif'):
    qif_data = [""]

     #iterate through CSV file
    with open(input_file, 'r') as csv_file:
        rows = list(csv.reader(csv_file, delimiter=','))
        
        #print to screen
        print(f"Number of data rows in the csv file: {len(rows) - 1}")
        rowNr = 1
        print("")
        print_row("Row", "Date", "Account", "Action", "Symbol", "Description", "Status", "Quantity", "Price", "Amount")
        print("-"*160)
        
        #format and write row to output file.  first iterate through values used in all "handled" cases
        for row in rows[1:]:
            print_row(rowNr, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
            rowNr += 1
            date = datetime.strptime(row[0], "%m/%d/%Y")
            csvacct = (row[1])
            quickenacct = lookup_acct[csvacct]
            csvaction = (row[2])
            quickenaction = lookup_action[csvaction]
            csvsecurity = (row[3])
            
            #handling dividends - no quantity but attributable to a specific security, posts to cash in brokerage acct
            if quickenaction in handle_dividend:
                qif_data.extend([
                    f"!Account",
                    f"N{quickenacct}",
                    f"TInvest",
                    f"^",
                    f"!Type:Invst",
                    f"D{date.strftime('%m/%d\'%Y')}",
                    f"N{quickenaction}",
                    f"Y{lookup_security[csvsecurity]}",
                    f"U{row[8]}",
                    f"T{row[8]}",
                    f"M{row[4]}",
                    "^"
                ])

            #handling transfers - no quantity, no specific security, linked to a to/from transfer account in Quicken
            #includes a "reminder" as the Payee to make sure the transfer account was correct
            if quickenaction in handle_transfer:
                qif_data.extend([
                    f"!Account",
                    f"N{quickenacct}",
                    f"TInvest",
                    f"^",
                    f"!Type:Invst",
                    f"D{date.strftime('%m/%d\'%Y')}",
                    f"N{quickenaction}",
                    f"P{variables["default_payee"]}",
                    f"U{row[8]}",
                    f"T{row[8]}",
                    f"L{variables["default_transfer_acct"]}",
                    f"{row[8]}",
                    f"M{row[4]}",
                    "^"
            ])
                
            #handling interest - no quantity, no specific security, posts to cash in brokerage acct    
            if quickenaction in handle_interest:
                qif_data.extend([
                    f"!Account",
                    f"N{quickenacct}",
                    f"TInvest",
                    f"^",
                    f"!Type:Invst",
                    f"D{date.strftime('%m/%d\'%Y')}",
                    f"N{quickenaction}",
                    f"U{row[8]}",
                    f"T{row[8]}",
                    f"M{row[4]}",
                    "^"
                ])

            #handling shares - buy or sell a specific security within the same brokerage acct    
            if quickenaction in handle_shares:
                qif_data.extend([
                    f"!Account",
                    f"N{quickenacct}",
                    f"TInvest",
                    f"^",
                    f"!Type:Invst",
                    f"D{date.strftime('%m/%d\'%Y')}",
                    f"N{quickenaction}",
                    f"Y{lookup_security[csvsecurity]}",
                    f"T{row[8]}",
                    f"Q{row[6]}",
                    f"M{row[4]}",
                    #f"C{row[5]}",
                    "^"
            ])

    #iteratively write the account and transaction data to the output file per the QIF specs
    with open(output_file, 'w') as qif_file:
        qif_file.write('\n'.join(qif_data))
    print("\nQIF file created successfully")


parser = argparse.ArgumentParser()
parser.add_argument('files', nargs='*', default=['input.csv', 'output.qif'])
args = parser.parse_args()

if len(args.files) == 1:
    csv2qif(input_file=args.files[0])
else:
    csv2qif(*args.files);