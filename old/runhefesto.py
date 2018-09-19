import os
import subprocess
import shutil
import pandas as pd
from threading import Timer


def cleanup():
    if "fort.58" in os.listdir(os.getcwd()):
        os.remove("fort.58")
    if "fort.59" in os.listdir(os.getcwd()):
        os.remove("fort.59")
    if "fort.66" in os.listdir(os.getcwd()):
        os.remove("fort.66")
    if "control" in os.listdir(os.getcwd()):
        os.remove("control")


if __name__ == "__main__":

    dirname = None
    print("\n\n\nWhat do you want this run to be called?")
    runname = raw_input(">>> ")

    if os.path.exists(os.getcwd() + "/{}_HeFESTo_Output_Files/".format(runname)):
        shutil.rmtree(os.getcwd() + "/{}_HeFESTo_Output_Files/".format(runname))
    os.mkdir(os.getcwd() + "/{}_HeFESTo_Output_Files/".format(runname))

    print("What is the directory name where input directories are located?")
    while True:
        inp = raw_input(">>> ")
        if os.path.exists(os.getcwd() + "/" + inp):
            dirname = inp
            print("Found directory: " + os.getcwd() + "/" + dirname)
            break
        else:
            print(os.getcwd() + "/" + inp + " not found!")
    for root, dirs, files in os.walk(os.getcwd() + "/" + dirname, topdown=False):
        for dir in dirs:
            os.mkdir(os.getcwd() + "/{}_HeFESTo_Output_Files/".format(runname) + dir)
            os.mkdir(os.getcwd() + "/{}_HeFESTo_Output_Files/".format(runname) + dir + "/fort.58")
            os.mkdir(os.getcwd() + "/{}_HeFESTo_Output_Files/".format(runname) + dir + "/fort.59")
            os.mkdir(os.getcwd() + "/{}_HeFESTo_Output_Files/".format(runname) + dir + "/fort.66")

            for rs, ss, fs in os.walk(os.getcwd() + "/" + dirname + "/" + dir):
                for f in fs:
                    component = None
                    if "BSP" in f:
                        component = "BSP"
                    elif "MORB" in f:
                        component = "MORB"
                    cleanup()
                    shutil.copy(os.getcwd() + "/" + dirname + "/" + dir + "/" + f, os.getcwd() + "/" + "control")
                    starcomponent = f.replace("HeFESTo_Infile.txt", "").replace("HeFESTo_Infile.txt", "")
                    p = subprocess.Popen(os.getcwd() + "/main", stdin=None, stdout=None)
                    t = Timer(800, p.kill)
                    t.start()
                    p.communicate()
                    t.cancel()
                    if "fort.58" in os.listdir(os.getcwd()):
                        shutil.move(os.getcwd() + "/fort.58",
                                    os.getcwd() + "/{}_HeFESTo_Output_Files/".format(runname) + dir + "/fort.58/" + "{}.txt".format(
                                        starcomponent + "HeFESTo_Output_File"))
                    if "fort.59" in os.listdir(os.getcwd()):
                        shutil.move(os.getcwd() + "/fort.59",
                                    os.getcwd() + "/{}_HeFESTo_Output_Files/".format(runname) + dir + "/fort.59/" + "{}.txt".format(
                                        starcomponent + "HeFESTo_Output_File"))
                    if "fort.66" in os.listdir(os.getcwd()):
                        shutil.move(os.getcwd() + "/fort.66",
                                    os.getcwd() + "/{}_HeFESTo_Output_Files/".format(runname) + dir + "/fort.66/" + "{}.txt".format(
                                        starcomponent + "HeFESTo_Output_File"))

