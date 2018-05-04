import os
import shutil

if "cp" in os.listdir(os.getcwd()):
    shutil.rmtree(os.getcwd() + "/cp")
os.mkdir('cp')

for i in os.listdir(os.getcwd()):
    if 'HeFESTo_Infile' in i:
        print(i)
        with open(i, 'r') as infile, open(os.getcwd() + "/cp/{}".format(i), 'w') as outfile:
            for line in infile:
                line = line.replace(',1600,', ',1800,')
                outfile.write(line)
        infile.close()
        outfile.close()

