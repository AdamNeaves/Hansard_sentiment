# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import requests
import zipfile
import os
url_base = 'http://www.hansard-archive.parliament.uk/'
url_add = ['Parliamentary_Debates_Vol_1_(1803)_to_Vol_41_(Feb_1820)',
           'Parliamentary_Debates,_New_Series_Vol_1_(April_1820)_to_Vol_25_(July_1830)',
           'Parliamentary_Debates_(3rd_Series)_Vol_1_(Oct_1830)_to_Vol_356_(August_1891)',
           'Parliamentary_Debates_(4th_Series)_Vol_1_(February_1892)_to_Vol_199_(December_1908)',
           'Official_Report,_House_of_Commons_(5th_Series)_Vol_1_(Jan_1909)_to_Vol_1000_(March_1981)',
           'The_Official_Report,_House_of_Lords_(5th_Series)_Vol_1_(Jan_1909)_to_2004',
           'The_Official_Report, _House_of_Commons_(6th_Series)_Vol_1_(March_1981)_to_2004']

save_loc = 'F:\Documents\-Uni Documents\Year 3\Final Project\Hansard Dataset\S'
file_name_format = 'S{}CV{:0>4}P{}.zip'

series = 1

# print("FILE NAME FORMAT: {}".format(file_name_format.format(11)))
for i in range(0, 100):  # change depending on how many files it looks like exist
    for j in range(0, 4):  # just to make sure. Not seen any files with P3 at the end but you never know
        temp_url = '{}{}/{}'.format(url_base, url_add[series], file_name_format.format(series, i, j))
        print("Checking: {}".format(file_name_format.format(series, i, j)))
        r = requests.get(temp_url)
        status = r.headers['content-type']
        print("FILE TYPE: {}".format(status))
#        if status.type == 'application/zip':  # if the zip file of that name exists, the type will appear like this
#            print("FILE FOUND")
#            urllib.urlretrieve(temp_url, "{}\{}".format(save_loc, file_name_format.format(i, j)))  # download the file
#            zip_ref = zipfile.ZipFile("{}\{}".format(save_loc, file_name_format.format(i, j)), 'r')
#            zip_ref.extractall(save_loc)  # extract the file
#            zip_ref.close()
#            # delete the zip file now we have extracted it's data
#            os.remove("{}\{}".format(save_loc, file_name_format.format(i, j)))
            
#        else:       # if the zip file doesn't exist it'll have a type of "text/html", because it generates an error page
#            print("FILE NOT FOUND")
