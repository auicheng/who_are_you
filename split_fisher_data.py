import sys
import os
from pydub import AudioSegment


#wav_file_dir is the path of immediate directory where wav file resides
#transcript_dir_prefix is the top level transcript directory
#If your wav file in in a folder named "058", you must also create another folder in separate location named "058" and put transcript there
#This is to mimic the current folder structure of the actual dataset
#example path for wav file - C:/Who Are You Project/fe_03_p2_sph1/audio/058
#example transcript full path - C:/Who Are You Project/data/trans/058/fe_03_05806.txt
#example transcript_dir_prefix - C:/Who Are You Project/data/trans
def process_file(wav_file_dir, transcript_dir_prefix, output_dir):
    slices = []
    for filename in os.listdir(wav_file_dir):
        max_length_slice = 0
        print ("filename: ", filename)
        filename_no_filetype = filename.split('.')[0] #remove file type from filename
        print ("filename without file type: ", filename_no_filetype)
        transcript_dir_suffix = wav_file_dir.split('/')[-1] + '/' + filename_no_filetype + '.txt'
        transcipt_full_path = transcript_dir_prefix + '/' + transcript_dir_suffix
        print ("transcript path: ", transcipt_full_path)
        transcript_data = get_split_duration(transcipt_full_path)
        output_file_name_prefix = "split-"
        split = 1
        print ("full wav file path: ", wav_file_dir+"/"+filename)
        print (wav_file_dir+"/"+filename)
        os.mkdir(output_dir+"/"+filename_no_filetype+"_slices")
        audio_input = AudioSegment.from_file(wav_file_dir+"/"+filename, format="wav")
        # audio_input = AudioSegment.from_wav(wav_file_dir+"/"+filename)      #reads the wav file here
        for i in range(len(transcript_data)):
            transcript_data_line = transcript_data[i].split()
            if len(transcript_data_line) == 0 or transcript_data_line[0] == '#':
                continue
            start_time_millisecs = int(float(transcript_data_line[0]) * 1000)       #unit is in microseconds
            end_time_millisecs = int(float(transcript_data_line[1]) * 1000)         #unit is in microseconds
            if(end_time_millisecs - start_time_millisecs > max_length_slice):
                max_length_slice = end_time_millisecs - start_time_millisecs
            print("start in array: ", transcript_data_line[0], "end in array: ", transcript_data_line[1])
            print("start time: ", start_time_millisecs, "end time: ", end_time_millisecs)
            speaker = transcript_data_line[2].split(':')[0]
            chunk_data = audio_input[start_time_millisecs : end_time_millisecs]
            chunk_name = output_file_name_prefix + str(split) + '-' + filename_no_filetype + '_' + speaker + '.wav'
            split += 1
            print ("exporting", chunk_name)
            print ("Output Directroy: ", output_dir)
            chunk_data.export(output_dir+"/"+filename_no_filetype+"_slices"+"/"+chunk_name, format="wav", codec="pcm_mulaw")       #saves each split file to output directory here
        slices.append(max_length_slice)
    return slices
    
#returns an array of all start and end durations and speaker from a transcript txt file
# an element in return array would look like {1.03 2.59 B}
def get_split_duration(transcript_path):
    transcript_details = []
    with open(transcript_path) as t:
            transcript = t.readlines()
    for utterance in transcript:
        field = utterance.split()
        print ("field: ", field)
        if(len(field)> 2):
            element = field[0] + " " + field[1] + " " + field[2]
            transcript_details.append(element)
    return transcript_details

def main(argv):
    lens = []
    # make sure there are at least two arguments
    if len(argv) >= 3:
        lens = process_file(argv[0], argv[1], argv[2])
    else:
        print ("Incomplete Arguments...")
        print ("\nUsage: python sys_argv.py <wav_file_dir> <transcript_dir_prefix> <output_dir>\n")
        print ("Example: python sys_argv.py 7 3\n")
        sys.exit(2)
    print(lens)
 
 
if __name__ == '__main__':
 
    # exclude script name from the argumemts list and pass it to main()
    main(sys.argv[1:])
