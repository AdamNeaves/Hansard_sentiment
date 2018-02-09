# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import urllib
import zipfile
import os
url = 'http://www.hansard-archive.parliament.uk/The_Official_Report,_House_of_Commons_(6th_Series)_Vol_1_(March_1981)_to_2004/{}'
save_loc = 'F:\Documents\-Uni Documents\Year 3\Final Project\Hansard Dataset\S6'
file_name_format = 'S6CV{:0>4}P{}.zip' 


#print("FILE NAME FORMAT: {}".format(file_name_format.format(11)))
for i in range (0, 500): #change depending on how many files it looks like exist
    for j in range (0, 4): #just to make sure. Not seen any files with P3 at the end but you never know
        temp_url = url.format(file_name_format.format(i, j))
        print("Checking: {}".format(file_name_format.format(i, j)))
        status = urllib.urlopen(temp_url).info() #get info about the file at that location
        print("FILE TYPE: {}".format(status.type))
        if(status.type == 'application/zip'): #if the zip file of that name exists, the type will appear like this
            print("FILE FOUND")
            urllib.urlretrieve(temp_url, "{}\{}".format(save_loc, file_name_format.format(i, j))) #download the file
            zip_ref = zipfile.ZipFile("{}\{}".format(save_loc, file_name_format.format(i, j)), 'r')
            zip_ref.extractall(save_loc) #extract the file
            zip_ref.close()
            os.remove("{}\{}".format(save_loc, file_name_format.format(i, j))) #delete the zip file now we have extracted it's data
            
        else:                #if the zip file doesn't exist it'll have a type of "text/html", because it generates an error page
            print("FILE NOT FOUND")