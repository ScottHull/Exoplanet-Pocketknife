import os






def replace_temp(inputfile_folder):
    os.chdir(inputfile_folder)
    home_dir = os.getcwd()
    for i in os.listdir(os.getcwd()):
        if os.path.isdir(i):
            os.chdir(i)
            print("In folder: {}".format(os.getcwd()))
            for z in os.listdir(os.getcwd()):
                if '.txt' in z:
                    with open(z, 'r') as infile:
                        with open("temp.txt", 'w') as outfile:
                            print("\nChanging string in file: {}".format(z))
                            infile_text = infile.read()
                            s = infile_text.replace(",20,80,1200,0,-2,0", "0,20,80,1600,0,-2,0")
                            outfile.write(s)
                            os.remove(z)
                            os.rename("temp.txt", z)
                    infile.close()
                    print("Success! Replaced string in file: {}".format(z))
            os.chdir(home_dir)






def initialization():
    print("\n\n\n\nPlease specify your HeFESTo input file folder (in Exoplanet Pocketknife format):")
    in1 = input("\n>>> ")
    if in1 in os.listdir(os.getcwd()):
        replace_temp(inputfile_folder=in1)
    else:
        initialization()




initialization()