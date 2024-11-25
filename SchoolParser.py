from fileinput import filename
from logging import exception
import pandas as pd
import os
import csv
from csv import reader
 
# Your current directory (including python script & all excel files)
mydir = (os.getcwd()).replace('\\','/') + '/'
 
#Get all excel files include subdir
filelist=[]
fileNameList=[]
for path, subdirs, files in os.walk(mydir):
   for file in files:
       if (file.endswith('.xlsx') or file.endswith('.xls') or file.endswith('.XLS')):
           filelist.append(os.path.join(path, file))
           fileNameList.append(file)
number_of_files=len(filelist)
 
# Read all excel files and save to dataframe (df[0] - df[x]),
# x is the number of excel files that have been read - 1
dfUrban=[]
for i in range(number_of_files):
   try:
       dfUrban.append(pd.read_excel(filelist[i], sheet_name=0))
   except exception:
       print(exception)
 
dfRural=[]
for i in range(number_of_files):
   try:
       dfRural.append(pd.read_excel(filelist[i], sheet_name=1))
   except exception:
       print(exception)
 
def writeFileWithConditions(df, outputName, currentFileIndex):
    currentFileName = fileNameList[currentFileIndex].split(".")[0]
    dfRelated = []
    # Checking conditions and writing row
    for row in df[currentFileIndex].itertuples(index=False, name=None):
        for nextRow in df[currentFileIndex].itertuples(index=False, name=None):
            # Check if school isn't the same
            if row[0] != nextRow[0]:
                # Same SubGrupo or same IDEB
                if row[8] == nextRow[8] or row[9] == nextRow[9]:
                    # Removing empty IDEB rows
                    if row[9] != '-' and row[9] != '#N/A':
                        dfRelated.append([row[1], nextRow[1]])
                        
    with open('output/'+currentFileName+" - "+ outputName+ '.csv', 'w', newline='') as myfile:
        # Writing header
        fields=["Soude","Target"]
        wr=csv.DictWriter(myfile,fieldnames=fields)
        wr.writeheader()
        dfRelatedConverted = pd.DataFrame(dfRelated)
        dfRelatedConverted = dfRelatedConverted[~dfRelatedConverted.apply(sorted, 1).duplicated()]
        
        dfRelatedConverted.to_csv(myfile, header=False, index=False)


 
for i in range(number_of_files):
   writeFileWithConditions(dfUrban, "Urbano", i)
 
for i in range(number_of_files):
   writeFileWithConditions(dfRural, "Rural", i)