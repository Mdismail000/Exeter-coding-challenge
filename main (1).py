import csv
import os
import psutil
import re
import time

start_time = time.time()

find_words_list = []
with open('find_words.txt', 'r') as find_words_file:
    for find_words_line in find_words_file:
        for words in find_words_line.split():
            find_words_list.append(words)
find_words_file.close()

meanings_list = []
with open("french_dictionary.csv", "r") as f:
    reader = csv.reader(f)
    for i in range(0, len(find_words_list)-1):
        for row in reader:
            if row[0] == find_words_list[i]:
                meanings_list.append(row[1])
                break
f.close()

translated_output_file = open("t8.shakespeare.translated.txt", "wt")
word_with_count = {}
with open('t8.shakespeare.txt', 'r') as shakespeare_file:
    for shakespeare_line in shakespeare_file:
        for shakespeare_word in re.split('[ *-_<,()>/:;.?"!\n]', shakespeare_line):
            for i in range(0, len(find_words_list)-1):
                if str(shakespeare_word.upper()) == str(find_words_list[i].upper()):
                    temp_dict = {}
                    if shakespeare_word.lower() in word_with_count.keys():
                        a = int(word_with_count[shakespeare_word.lower()])
                        temp_dict = {find_words_list[i]: a+1}
                    else:
                        temp_dict = {find_words_list[i]: 1}
                    word_with_count.update(temp_dict)
                    if shakespeare_word.isupper():
                        shakespeare_line = shakespeare_line.replace(shakespeare_word, meanings_list[i].upper())
                    else:
                        shakespeare_line = shakespeare_line.replace(shakespeare_word, meanings_list[i])
                    break
        translated_output_file.write(shakespeare_line)
shakespeare_file.close()
translated_output_file.close()

f=open("frequency.csv","w")
f.write("English word,French word,Frequency")
for item in word_with_count.items():
   for i in range(0,len(find_words_list)-1):
       if(item[0]==find_words_list[i]):
            f.write("\n"+str(item[0])+","+str(meanings_list[i])+","+str(item[1]))
f.close()

end_time = time.time()
seconds = int(end_time-start_time)

f = (open("performance.txt", "w"))
line1 = str("Time to process: "+str(int(seconds/60))+" minutes "+ str(int(seconds % 60))+ " seconds")
line2 = str("Memory used: "+ str(psutil.Process(os.getpid()).memory_info().rss/1024**2)+ " MB")
f.write(line1+"\n")
f.write(line2)
f.close()
