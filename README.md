# whattheqif

I created this python program to enable detailed position and transaction tracking within brokerage and retirement accounts, 
when your investment broker does not have that type of feature available for Quicken.

This python program creates an investment .qif file from an instition's .csv containing investment activity, with the input
schema being: 
    Date
    Account
    Type
    Symbol
    Description
    Status
    Quantity
    Price
    Amount

There are 3 files that require your specific information for the program to run correctly:

    account_map.txt maps the institutions account to that of your Quicken file.  Update this file 1:1 for each of yours.
    In this file, there is no need for " marks.  List the institution account from their download end with a colon (:) plus
    a space, and then list the exact corresponding account name from Quicken.

    config.txt contains values, which may be expanded over time.  This is where you set your default transfer in/out account
    used to fund your investments, and a default payee that will appear in that tranfer accounts register, and serve as a 
    check/reminder to make sure the account transfer went to the correct place. Make sure you use the quote marks to create the
    correct text output back to Quicken.

    security_map.txt is used to map the investment ticker symbol to the exact name of the security in your Quicken file.
    The way the import process works, the ticker alone will not land the transactions in the correct place, so this 
    overcomes that issue.

There are comments in the code to explain what is happening programatically.  There may be a need to edit some of the
transaction mapping, based on nuances from your financial institution.  Also note that for every transaction, I define the
target account in Quicken.  I did not want to rely on any order or structure in the institution's input file.  This may not
be the most efficient, but it works reliably.

Good Luck!

