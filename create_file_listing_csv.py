import sys
import os
import csv
from random import randint
from pydub import AudioSegment


#transcript_dir_prefix is the top level transcript directory
#slices_dir is the directory that contains all the slices folders.
#wav_files_dir is the parent directory that contains all sub-directories for wav files
#file_table_dir is a directory where all filetable2.txt files are places for one-time read
#material is either "train", "dev", or "test". Pass in value from command line and use to create filelisting.csv output
#output_dir is wherever we want the filelisting.csv output file to be saved
#example wav_files_dir - C:/Who Are You Project/fisher_eng_tr_sp_d1_wavs/audio
#example slices_dir - "C:/Who Are You Project/fisher_eng_tr_sp_d1_wavs/slices"

wav_file_names = []
filename_gender_map = {} #maps filename to speaker's gender from filetable2.txt files
material = ""   #this can be train/dev/test and should be passed in from Command Line
output_dir = "" #populate from command line
output_file_name = "filelisting.csv"
corpus = "fisher"

#1)Put all filetable2.txt files from all the folders into just one folder.
#2)Filetable files should be the only things in the folder.
#3)You can rename them as long as only filetable2.txt files are contained in folder
# def read_filetable_files(file_table_dir):   #Call 1
#     line_parts = []
#     for filename in os.listdir(file_table_dir):
#         full_path = file_table_dir + '/' + filename
#         file = open(full_path, "r") 
#         for line in file:
#             line_parts = line.split()
#             #print("line parts 1: ", line_parts[1])
#             fname = line_parts[1].split('.')[0].strip() #take filename element and remove .sph from it
#             gender = line_parts[2].strip()
#             print ("fname: ", fname, " gender: ", gender)
#             filename_gender_map[fname] = gender
#         file.close()

def read_filetable_files(file_table_path):
    file = open(file_table_path)
    for line in file:
        line_parts = line.split()
        #print("line parts 1: ", line_parts[1])
        fname = line_parts[1].split('.')[0].strip() #take filename element and remove .sph from it
        gender = line_parts[2].strip()
        print ("fname: ", fname, " gender: ", gender)
        filename_gender_map[fname] = gender
    file.close()    


def create_wav_list (wav_file_dir):     
    for directory_name in os.listdir(wav_file_dir):        
        print ("directory name: ", directory_name)
        wav_full_path = wav_file_dir + '/' + directory_name
        for wav_filename in os.listdir(wav_full_path):
            print ("file name: ", wav_filename)
            filename_no_filetype = wav_filename.split('.')[0].strip() #remove file type from filename
            wav_file_names.append(filename_no_filetype)

def process_file(wav_files_dir, slices_dir, output_dir):    #Call 2
    create_wav_list(wav_files_dir)
    slice_path = ""
    output_file_path = output_dir + '/' + output_file_name
    csv_line = []
    with open(output_file_path, 'a') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['file', 'material', 'gender', 'corpus'])
    #loop through the wav list, find matching split folder, loop through split folder and obtain file splits
    for filename in wav_file_names:
        for slice_folder_name in os.listdir(slices_dir):
            if filename in slice_folder_name:
                slice_path = slices_dir + '/' + slice_folder_name
                for slices in os.listdir(slice_path):
                    slice_full_path = slices_dir + "/" + slice_folder_name + '/' + slices
                    gender = get_gender(slices, filename)
                    #create fileListing csv entry here, fetch gender from filename_gender_map using filename as key
                    with open(output_file_path, 'a') as csvfile:
                        filewriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
                        #filewriter.writerow(['file', 'material', 'gender', 'corpus'])   --- Put this file header manually!!!
                        csv_line.append(slice_full_path)
                        csv_line.append(get_material())
                        csv_line.append(gender)
                        csv_line.append(corpus)
                        filewriter.writerow(csv_line)
                        print ("writing slice: ", slices, " to filelist.csv")
                        csv_line = []
        
def get_material():
    seed = randint(1, 100)
    if seed <= 70:
        return 'train'
    elif seed <= 85:
        return 'dev'
    else 
        return 'test'


def get_gender(split_filename, filename_without_type):  #return value of 0 is male, 1 is female
    split_prefix = split_filename.split('.')[0]
    file_genders = filename_gender_map[filename_without_type]
    gender = ''
    if file_genders: #if file_genders is not empty       
        if split_prefix[-1] == 'A': #suffix of A means first speaker, so take first one from gender
            gender = file_genders[0]
            if gender == 'm':
                return "male"
            elif gender == 'f':
                return "female"
            else:
                print ("gender: " + gender + " from file isn't an expected gender type")
                sys.exit(2)
        elif split_prefix[-1] == 'B': #suffix of B means second speaker, so take second one from gender
            gender = file_genders[1]
            if gender == 'm':
                return "male"
            elif gender == 'f':
                return "female"
            else:
                print ("gender: " + gender + " from file isn't an expected gender type")
                sys.exit(2)
        else:
            print("split file name: " + split_filename + " isn't the correct format")
            sys.exit(2)
            
    else:
        print("genders for file: " + filename_without_type + " not available in any of the filetable.txt files given")
        sys.exit(2)

def start(file_table_dir, wav_files_dir, slices_dir, output_dir):
    # global material
    # material = the_material
    # print ("material: ", material)
    # if material != "train" and material != "dev" and material != "test":
    #     print("Error! Specify in 2nd argument whether it's a train, dev or test")
    #     sys.exit(2)
    read_filetable_files(file_table_dir)                                           
    process_file(wav_files_dir, slices_dir, output_dir)
        
def main(argv): 
    # make sure there are at least five arguments
    if len(argv) >=4 :
        start(argv[0], argv[1], argv[2], argv[3])
    else:
        print ("Incomplete Arguments...")
        print ("\nUsage: python create_file_listing_csv.py <file_table_dir> <wav_file_dir> <slices_dir> <output_dir>\n")
        #print ("Example: python create_file_listing_csv.py 7 3\n")
        sys.exit(2)
 
 
if __name__ == '__main__':
 
    # exclude script name from the argumemts list and pass it to main()
    main(sys.argv[1:])
