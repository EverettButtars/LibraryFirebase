def main():
    import mysql.connector
    from sqlalchemy import create_engine
    import pandas as pd

    #conect to database
    library = mysql.connector.connect(
    host = "localhost",
    user = "Admin",
    password = "Library",
    database = "Library"
    )
    cursor = library.cursor()

    #bundle connection info for easier transport
    conInfo = [library, cursor]

    #Initialize Function Dictionary
    functions = {"search": search,
                 "remove": remove,
                 "add": add,
                 "changeBook": changeBook,
                 "numberOf": numberOf,
                 "numberOfTypes": numberOfTypes,
                 "totalBooks": totalBooks,
                 "Help": getHelp}

    print("Welcome to the Library Database!")
    print("To get help, type, \"Help\" ")
    while True:
        inp = input(':')
        (functions[inp])(conInfo)


    library.close()

def getHelp(conInfo):
    print("commands: search, remove, add, changeBook, numberOf, numberOfTypes, totalBooks")

def getBookInfo():
    while True:
        print("input data type followed by the data and then a comma: ex. Title Harry Potter, Author J.K. Rowling")
        
        #gets the input and parses into list according to commas
        bookInfo = input("input: ").split(", ")
        #Then splits each elements string further on their first space.
        bookInfo = [i.split(" ", 1) for i in bookInfo]
        #Flattens list and returns it!
        bookInfo = [item for sublist in bookInfo for item in sublist]

        if len(bookInfo) < 2:
            print("Not enough arguments")
            continue
        #check if there are an even number of args
        if len(bookInfo) % 2 != 0:
            print("Odd number of arguments: missing an entry")
            continue
        print(bookInfo)
        return bookInfo
    
        
def search(conInfo):
    searchInfo = getBookInfo()

    print("Attempting to search...")

    #format odd elements for wild card
    odds = searchInfo[1::2]
    for i in range(0, len(odds)):
        odds[i] = "'%"+odds[i]+"%'"
    
    query = "SELECT * FROM books WHERE "

    #break search info into tuples
    searchInfo = list(zip(searchInfo[0::2], odds))
    print(searchInfo)
    #join tuples using the like attribute, and join each liked argument with and
    query += " AND ".join([" LIKE ".join(i) for i in searchInfo])
    print(query)
    #execute and retrive results
    conInfo[1].execute(query)
    result = conInfo[1].fetchall()

    #prints all results
    print("Search results:")
    for i in result:
        print(i)


def remove(conInfo):
    #Retrive ISBN
    isbn = input("What is the isbn of the book?: ")
    #format
    query = "DELETE FROM books WHERE ISBN = %s"
    #attempt
    conInfo[1].execute(query, list(isbn))
    conInfo[0].commit()

    

def add(conInfo):
    #retrive book info
    newBook = getBookInfo()

    print("Attempting to add...")

    #format string for query, and establish values
    query = ("INSERT INTO books (%s) " % ', '.join(newBook[0::2]) + "VALUES (%s)" % ', '.join(["%s"] * (int(len(newBook)/2))))

    #slice and store odd elements from the list
    values = newBook[1::2]

    #execute and commit
    conInfo[1].execute(query, values)
    conInfo[0].commit()
    print("Success!")



def changeBook(conInfo):
    #Retrive Book details
    isbn = input("What is the isbn of the book?: ")
    changes = getBookInfo()

    #format each identifier to have the = %s after it
    odds = changes[0::2]
    for i in range(0, len(odds)):
        odds[i] += " = %s"
    
    #create query 
    query = "UPDATE books SET {}".format(", ".join(odds)) + " WHERE ISBN = %s"
    print(query)
    changes = changes[1::2]
    changes.append(isbn)
    print(changes)
    #attempt
    conInfo[1].execute(query, changes)
    conInfo[0].commit()
    print("Success!")



def numberOf(conInfo):
    #gather data
    column = input("What category? ex. Author: ")
    key = input("Search term? ex. Rowling: ")
    #format for wildcard
    key = "'%"+key+"%'"

    query = "SELECT COUNT(%s) FROM books WHERE %s LIKE %s"

    conInfo[1].execute(query, (column, column, key))
    data = conInfo[1].fetchall()
    print("The number of books matching input: ")
    print(data[0][0])
    



def numberOfTypes(conInfo):
    #gather data
    column = input("What category? ex. Author: ")

    query = "SELECT COUNT(%s) FROM books GROUP BY (%s)"

    conInfo[1].execute(query, (column, column))
    data = conInfo[1].fetchall()
    print(data[0][0])



def totalBooks(conInfo):
    #total copies of the books in library printed worldwide
    query = "SELECT SUM(Volume) FROM books"

    conInfo[1].execute(query)
    data = conInfo[1].fetchall()
    print("total copies of the books in library printed worldwide: " + str(int(data[0][0])))

if __name__ == "__main__":
    main()