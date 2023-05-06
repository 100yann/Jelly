import os
import datetime as dt

# os.getcwd() - get current directory
# os.chdir() - change directory to specified path
# os.listdir() - list all files and subdirectories
# os.remove(file) - removes file in current directory

filename = 'C://Users/Stoyan/CodingProjects/Jelly/jelly.txt'
creation_date = os.path.getctime(filename)
readable_date = dt.datetime.fromtimestamp(creation_date).strftime('%Y-%m-%d')
