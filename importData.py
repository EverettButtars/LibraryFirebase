import pandas as pd
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json

cred = credentials.Certificate("library-project-firebase-adminsdk.json")
libApp = firebase_admin.initialize_app(cred, {
	'databaseURL':'https://library-project-9b912-default-rtdb.firebaseio.com/'
	})

ref = db.reference("/")

#conect to database

# #read data in using pandas
data = pd.read_csv('data\\data.csv', encoding='latin-1')
dataframe = pd.DataFrame(data)
 
dataframe.drop(['Index', 'Position', 'Publisher Group', 'Imprint', 'Value', 'RRP', 'ASP', 'Product Class'], axis = 1, inplace = True)

#removing quotes and commas
columns = dataframe.columns

for book in dataframe.index:
	for col in columns:
		dataframe.loc[book, col] = str(dataframe.loc[book, col]).strip().replace("\"", "").replace(",", "")
	




#form volume to be an integer
dataframe['Volume'] = pd.to_numeric(dataframe['Volume'])
dataframe['ISBN'] = pd.to_numeric(dataframe['ISBN'])

#make all columns lowercase
data.columns = [x.lower() for x in data.columns]

# #Write to test file
# readyData = dataframe.to_json(orient='records')
# with open('readyData.json', 'w') as f:
#     f.write(readyData)

#Send data!
#Create correct subsection
ref.set({
	"Books":
	{

	}
})
#move our reference there
ref = db.reference("/Books")

#submit data
readyData = dataframe.to_json(orient='records')
readyData = json.loads(readyData)

print(readyData)

for dat in readyData:
	try:
		ref.push().set(dat)
	except: 
		print(str(dat))


print("Complete!")
