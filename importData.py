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

#create nessicary tables
#cursor.execute("CREATE TABLE books (id INT AUTO_INCREMENT PRIMARY KEY, bibliography VARCHAR(255), author VARCHAR(255), title VARCHAR(255), edition VARCHAR(255), number VARCHAR(255))")

#read data in using pandas
data = pd.read_csv('data\\data.csv', encoding='latin-1')
dataframe = pd.DataFrame(data)
 
dataframe.drop(['Index', 'Position', 'Publisher Group', 'Value', 'RRP', 'ASP'], axis = 1, inplace = True)


for book in dataframe.index:
    dataframe.loc[book, 'Volume'] = dataframe.loc[book, 'Volume'].strip().replace("\"", "").replace(",", "")


dataframe['Volume'] = pd.to_numeric(dataframe['Volume'])

#create engine to send via pandas
engine = create_engine('mysql+pymysql://Admin:Library@localhost/Library')
#send dataframe to mySQL server
dataframe.to_sql(con=engine, name='books', if_exists='replace')

print("Complete!")






#THIS IS ALL LEGACY NOW, THE OLD DATA SET WAS TO LARGE, MOVED TO NEW ONE.
#dataframe["Title"].dropna(inplace = True) #remove books with no titles
# dataframe["Author"].dropna(inplace = True) #remove books with no author

# for book in dataframe.index: 
#     #removes anything that doesn't have a string as its title, author, or bib, for error checking
#     if type(dataframe.loc[book, "Author"]) != str or type(dataframe.loc[book, "Title"]) != str or type(dataframe.loc[book, "Bibliography"]) != str:
#         dataframe.drop(book, inplace = True)

#     elif len(dataframe.loc[book, "Title"]) >= 255: #Removes all books with titles longer then 255, which with this data set, is a lot.
#         dataframe.drop(book, inplace = True)

#     elif "880" in dataframe.loc[book, "Title"]: #Books with 880 in their title are some sort of foreign record
#         dataframe.drop(book, inplace = True)

#     elif "  " in dataframe.loc[book, "Title"]: #In the titles, content after the double space is irrelevant. This removes it
#         dataframe.loc[book, "Title"] = dataframe.loc[book, "Title"].split("  ")[0]

#     elif "united states" in dataframe.loc[book, "Author"].lower(): #records with the united states as their author are historical documents
#         dataframe.drop(book, inplace = True)

#     elif any(x in dataframe.loc[book, "Bibliography"].lower() for x in ("video", "dvd", "cd", "ebook", "neig", "mu", "web")):  #removes any videos, ebooks, pictures (neig), music (mu), or website (web)
#        dataframe.drop(book, inplace = True)

#     elif not dataframe.loc[book, "Bibliography"].replace('.', '').isdigit(): #records with only numbers in their bibliography are records, not books
#         dataframe.drop(book, inplace = True)
    
#     print(book)

# print("Sending!")

# dataframe.drop(columns=['Title', 'Author']) #drop everything but titles and authors

