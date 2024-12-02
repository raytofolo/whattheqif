import csv
import argparse
from datetime import datetime

#define the columns being read from the input CSV file.  Each col value is listed here.
def print_row(rowNr, date, account, type, symbol, description, status, quantity, price, amount):
    print(
        f"{str(rowNr):<3} | "
        f"{str(date):<10}    | "
        f"{str(account):>10} | "
        f"{str(type):>22} | "
        f"{str(symbol):>10} | "
        f"{description:<35} | "
        f"{str(status):<9} | "
        f"{str(quantity):>10} | "
        f"{str(price):>7} | "
        f"{str(amount):>13} | "
    )


def csv2qif(input_file='input.csv', output_file='output.qif'):
    #qif_acct_header = ["!Account"]
    #qif_data = ["!Account", "lookup acct", "TInvst", "^", "!Type:Invst"]
    qif_data = ["\n!Type:Invst"]
    with open(input_file, 'r') as csv_file:
        #iterate through CSV file
        rows = list(csv.reader(csv_file, delimiter=','))
        
        #print to screen
        print(f"Number of data rows in the csv file: {len(rows) - 1}")
        rowNr = 1
        print("")
        print_row("Row", "Date", "Account", "Type", "Symbol", "Description", "Status", "Quantity", "Price", "Amount")
        print("-"*160)
        
        #format and write row to output file
        for row in rows[1:]:
            print_row(rowNr, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
            rowNr += 1
            date = datetime.strptime(row[0], "%m/%d/%Y")
            qif_data.extend([
                f"D{date.strftime('%m/%d\'%Y')}",
                #f"{row[1]}",
                f"N{row[2]}",
                f"Y{row[3]}",
                f"M{row[4]}",
                f"C{row[5]}",
                f"Q{row[6]}",
                f"I{row[7]}",
                f"T{row[8]}",                
                "^"
            ])

    with open(output_file, 'w') as qif_file:
        qif_file.write("!Account")
        qif_file.write("\nNAME OF ACCT")
        qif_file.write("\nTInvst") 
        qif_file.write('\n'.join(qif_data))
    print("\nQIF file created successfully")


parser = argparse.ArgumentParser()
parser.add_argument('files', nargs='*', default=['input.csv', 'output.qif'])
args = parser.parse_args()

if len(args.files) == 1:
    csv2qif(input_file=args.files[0])
else:
    csv2qif(*args.files);