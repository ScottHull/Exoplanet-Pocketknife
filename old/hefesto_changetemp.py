import os
import csv
import shutil


def changetemp(old_temp, new_temp):
    if os.path.exists("temp"):
        shutil.rmtree("temp")
    os.mkdir("temp")
    for i in os.listdir(os.getcwd()):
        if '.txt' in i:
            outfile = open(os.getcwd() + "/temp/{}".format(i), 'w')
            with open(i, 'r') as infile:
                reader = csv.reader(infile)
                for row in reader:
                    if "{}".format(old_temp) in row:
                        tostr = ",".join(str(i) for i in row)
                        r = tostr.replace(",{},".format(old_temp), ",{},".format(new_temp))
                        outfile.write(r + '\n')
                    else:
                        tostr = ",".join(str(i) for i in row)
                        outfile.write(tostr + '\n')
                outfile.close()
            infile.close()
            os.remove(i)
            fdir = os.getcwd() + "/temp/{}".format(i)
            tdir = os.getcwd() + "/{}".format(i)
            shutil.copy(fdir, tdir)
            print("Finished with {}!".format(i))
    shutil.rmtree(os.getcwd() + "/temp")



if __name__ == '__main__':
    print("What is the temperature to replace?")
    oldtemp = input(">>> ")
    print("What is the temperature to replace with?")
    newtemp = input(">>> ")
    changetemp(oldtemp, newtemp)