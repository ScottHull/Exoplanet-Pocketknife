import os
import pandas as pd


if __name__ == "__main__":


    print("In what directory shall we parse?")
    to_dir = input(">>> ")

    for root, dirs, files in os.walk(os.getcwd() + "/" + to_dir, topdown=False):
        operating_dir = root
        if "fort.58" in str(root):
            if "strip_hefesto_outfile.csv" in os.listdir(operating_dir):
                os.remove(operating_dir + "/strip_hefesto_outfile.csv")
            outfile = open(operating_dir + "/strip_hefesto_outfile.csv", 'a')
            for i in os.listdir(operating_dir):
                f = operating_dir + "/" + i
                if os.path.getsize(f) > 5:
                    if "HeFESTo" in i:
                        star_name = i.replace("fort.58.control.", "").replace("_fort.58", "").replace("_bsp.txt_bsp",
                                                                                                      "").replace(
                            "fort.58_", "").replace("_fort58", "").replace("_BSP_HeFESTo_Output_File", "").replace(
                            "_MORB_HeFESTo_Output_File", "")
                        df = pd.read_fwf(f, colspecs='infer')
                        if 'rho' in df.keys():
                            print("Working on {}".format(i))
                            rho = df['rho'].tolist()
                            # depth = df['depth'].tolist()
                            rho_str = star_name + "," + ",".join(str(z) for z in rho)
                            outfile.write(rho_str + "\n")
                            print("Finished with {}".format(i))
            outfile.close()