def main():
    
    import firebase_admin
    from firebase_admin import credentials
    from firebase_admin import db
    from firebase_admin import auth

    cred = credentials.Certificate("library-project-firebase-adminsdk.json")
    libApp = firebase_admin.initialize_app(cred, {
	    'databaseURL':'https://library-project-9b912-default-rtdb.firebaseio.com/'
	    })

    ref = db.reference("/Books")

    #bundle connection info for easier transport

    #Initialize Function Dictionary
    functions = {"search": search,
                 "remove": remove,
                 "add": add,
                 "changeBook": changeBook,
                 "Help": getHelp}

    print("Welcome to the Library Database!")
    print("To get help, type, \"Help\" ")
    while True:
        inp = input(':')
        (functions[inp])(ref)

    library.close()

def getHelp(ref):
    print("commands: search, remove, add, changeBook")

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
    
        
def search(ref):
    searchInfo = getBookInfo()

    print("Attempting to search...")

    #break search info into tuples
    searchInfo = list(zip(searchInfo[0::2], searchInfo[1::2]))

    #execute and retrive results
    books = ref.get()


    
    for key, value in books.items():
        keep = True
        for searchItem, searchValue in searchInfo:
            try:
                if str(searchValue) not in str(value[searchItem]):
                    keep = False
            except: 
                print("error on book")
                print(value)
                keep = False
        if keep:
            print(value)



def remove(ref):
    #Retrive ISBN
    isbn = input("What is the isbn of the book?: ")
    #format
    books = ref.get()
    for key, value in books.items():
        if value['ISBN'] == isbn:
            ref.child(key).set({})
            break
    

def add(ref):
    #retrive book info
    newBook = getBookInfo()

    print("Attempting to add...")

    #slice and store odd elements from the list
    values = newBook[1::2]
    keys = newBook[0::2]

    newBookDict = dict()

    for i in range(0, len(values)):
        newBookDict[keys[i]] = values[i]

    #execute and commit
    ref.push().set(newBookDict)
    print("Success!")



def changeBook(ref):
    #Retrive Book details
    isbn = input("What is the ISBN of the book?: ")
    info = getBookInfo()

    changes = info[0::2]
    keys = info[1::2]
    books = ref.get()

    for key, value in books.items():
        if value['ISBN'] == isbn:
            for i in range(0, len(keys)):
                print({ str(keys[i]): changes[i]})
                ref.child(key).update({changes[i]:keys[i]})

    print("Success!")

if __name__ == "__main__":
    main()