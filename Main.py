#import csv
#uploadFile = open('upload.csv')
#uploadReader = csv.reader(uploadFile)


import csv
#from collections import defaultdict

#columns = defaultdict(list) # each value in each column is appended to a list

fields = ['Date', 'Acct', 'Type', 'Symbol', 'Description', 'Status', 'Quantity', 'Price', 'Amount']

with open('file.csv', 'r') as csvfile:
    # for line in csv.DictReader(csvfile,):
     csv_reader = csv.reader(csvfile, delimiter = ',')
     list_of_column_names = []
     #for row in csvfile:
        # adding the first row
      #  list_of_column_names.append(row)
 
        # breaking the loop after the
        # first iteration itself
       # break
 
# printing the result
print(fields)
