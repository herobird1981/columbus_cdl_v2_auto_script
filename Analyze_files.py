import sys
import os
import csv
from time import strftime
sys.dont_write_bytecode=True
def GetFileNameAndExt(filename):
    (filepath, tempfilename) = os.path.split(filename)
    (shotname, extension) = os.path.splitext(tempfilename)
    return filepath, shotname, extension
crt.Sleep(1000)
filePath = crt.Dialog.FileOpenDialog(title="Please select any file in a Folder which you want analyze!")
dir_path = GetFileNameAndExt(filePath)[0]
a_path=os.path.join(dir_path + '\\'+strftime('analysis_%Y%m%d-%H%M%S') + '.csv')
a_file=open(a_path,'wb')
writer=csv.writer(a_file,delimiter=',')
count=0
for filename in os.listdir(dir_path):
    if filename.endswith(".csv"):
        if filename.startswith('analysis_'):
            continue
#        crt.Dialog.MessageBox(os.path.join(dir_path, filename))
        
        filepath=os.path.join(dir_path,filename)
        csv_file = open(filepath,'rb')
        reader=csv.reader(csv_file,delimiter=',')
        for row in reader:
            if row[0] != 'PASS':
                writer.writerow([filename]+row)
                count=count+1
       
        csv_file.close()
        continue
a_file.close()
crt.Dialog.MessageBox('Operation Completed, %d Entries found, Saved file path:' %(count) +a_path )
