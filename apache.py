import os
import json

def read_file(filename):
    results = []
    obj = {} 
    with open(filename, 'r') as file:
        for line in file.readlines():
            lineSplit = line.split(' ')
            requesturl = lineSplit[6]
            
            if requesturl not in obj:
                obj[requesturl] = {}

            requeststatus = lineSplit[8]
            obj[requesturl][requeststatus] = obj[requesturl].get(requeststatus, 0) + 1

    return obj

def saveDict(dict, fileName):
    with open(fileName, 'w', encoding='utf-8') as myfile:
        myfile.write(json.dumps(dict, indent=1))


def process_folder(input_folder_paths, output_foldedr_path):
    for input_folder_path in input_folder_paths:
        for filename in os.listdir(input_folder_path):
            print("Processing filename",filename)
            input_filepath = os.path.join(input_folder_path, filename)
            obj1={}
            if os.path.isfile(input_filepath):
                obj1=read_file(input_filepath)
            output_filename = f"summary-{filename}.json"
            output_filepath_summary = os.path.join(output_folder_path, output_filename)
            saveDict(obj1, output_filepath_summary)


input_folder_paths = ["files/December 2022", "files/Feb - Mar 2023"]
output_folder_path = "summary/"
access_folder_path = "access/"

process_folder(input_folder_paths, output_folder_path)



# input_folder_paths = 
# # input_folder_path = "files/"
# output_folder_path = "summary/"
# process_folders()
