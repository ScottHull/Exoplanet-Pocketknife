import os
import pandas as pd

if "strip_hefesto_outfile.csv" in os.listdir(os.getcwd()):
    os.remove("strip_hefesto_outfile.csv")
outfile = open("strip_hefesto_outfile.csv", 'a')

for i in os.listdir(os.getcwd()):
    if "fort" in i:
        df = pd.read_fwf(i, colspecs='infer')
        depth = df['depth'].tolist()
        depth_header = "Star," + ",".join(str(z) for z in depth)
        outfile.write(depth_header + "\n")
        break

for i in os.listdir(os.getcwd()):
    if "fort" in i:
        star_name = i.replace("fort.58.control.", "").replace("_fort.58", "").replace("_bsp.txt_bsp", "").replace(
            "fort.58_", "").replace("_fort58", "")
        df = pd.read_fwf(i, colspecs='infer')
        rho = df['rho'].tolist()
        depth = df['depth'].tolist()
        rho_str = star_name + "," + ",".join(str(z) for z in rho)
        outfile.write(rho_str + "\n")
        print("Finished with {}".format(i))
