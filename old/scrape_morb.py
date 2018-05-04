import os, csv


if "scrapeMORB_output.csv" in os.listdir(os.getcwd()):
    os.remove("scrapeMORB_output.csv")
outfile = open("scapeMORB_output.csv", 'a')
for i in os.listdir(os.getcwd()):
    if "MORB_OUTPUT.csv" in i and enumerate(i, 1) >= 100:
        with open(i, 'r') as infile:
            reader = csv.reader(infile)
            header = next(reader)
            star_name = header[1]
            for num, line in enumerate(reader, 1):
                if "liquid_0" in line:
                    next(reader)
                    capture = list(next(reader))
                    string = star_name + "," + ",".join(i for i in capture)
                    outfile.write(string + "\n")
                    break
        infile.close()
outfile.close()
