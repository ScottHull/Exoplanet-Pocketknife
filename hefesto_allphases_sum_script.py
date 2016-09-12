import os, pandas


# header_structure = ["Star","plg","sp","opx","c2c","cpx","gt","cpv","ol","wa","ri","il","pv","ppv","cf","mw","qtz","coes","st","apbo","ky","neph"] #21 phases

hefesto_stars_pass = []
hefesto_stars_fail = []

def __init__():
    print("\n_____________________________________\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print("Make sure that this file exists within a directory containing HeFESTo fort.66 files for parsing.\n")
    print("Please type 'b' to begin...")
    in1 = input(">>> ")
    if in1 == "b" or in1 == "begin":
        fort66_fileparse()
    else:
        print("\nOops!  That's not a valid command!\n")
        __init__()



def fort66_fileparse():
    if "HeFESTo_Phase_Sums.csv" in os.listdir(os.getcwd()):
        os.remove("HeFESTo_Phase_Sums.csv")
    else:
        pass
    outputfile = open("HeFESTo_Phase_Sums.csv", 'a') #this output file will be created in working directory and will contain all sums with their respective star
    outputfile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format("Star","HeFESTo Pass/Fail?","plg","sp","opx","c2c","cpx","gt","cpv","ol","wa","ri","il","pv","ppv","cf","mw","qtz","coes","st","apbo","ky","neph"))
    for f in os.listdir(os.getcwd()):
        starname = f[16:-12]
        try:
            print("\nAnalyzing fort.66 output for star: " + starname)
            plg_list = []
            sp_list = []
            opx_list = []
            ctc_list = []
            gt_list = []
            cpv_list = []
            cpx_list = []
            ol_list = []
            wa_list = []
            ri_list = []
            il_list = []
            pv_list = []
            ppv_list = []
            cf_list = []
            mw_list = []
            qtz_list = []
            coes_list = []
            st_list = []
            apbo_list = []
            ky_list = []
            neph_list = []
            # all_sum = []
            with open(f, 'r') as infile:
                readthefile = pandas.read_fwf(infile, colspecs='infer')
                df = readthefile.iloc[:, [3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]]
                hefesto_stars_pass.append(starname)
                for i in df['plg']:
                    plg_list.append(i)
                for i in df['sp']:
                    sp_list.append(i)
                for i in df['opx']:
                    opx_list.append(i)
                for i in df['c2c']:
                    ctc_list.append(i)
                for i in df['gt']:
                    gt_list.append(i)
                for i in df['cpv']:
                    cpv_list.append(i)
                for i in df['cpx']:
                    cpx_list.append(i)
                for i in df['ol']:
                    ol_list.append(i)
                for i in df['wa']:
                    wa_list.append(i)
                for i in df['ri']:
                    ri_list.append(i)
                for i in df['il']:
                    il_list.append(i)
                for i in df['pv']:
                    pv_list.append(i)
                for i in df['ppv']:
                    ppv_list.append(i)
                for i in df['cf']:
                    cf_list.append(i)
                for i in df['mw']:
                    mw_list.append(i)
                for i in df['qtz']:
                    qtz_list.append(i)
                for i in df['coes']:
                    coes_list.append(i)
                for i in df['st']:
                    st_list.append(i)
                for i in df['apbo']:
                    apbo_list.append(i)
                for i in df['ky']:
                    ky_list.append(i)
                for i in df['neph']:
                    neph_list.append(i)
            print("PHASE 'PLG' FRACTION AT 409.72km: " + str(plg_list[55]))
            print("PHASE 'SP' FRACTION AT 409.72km: " + str(sp_list[55]))
            print("PHASE 'OPX' FRACTION AT 409.72km: " + str(opx_list[55]))
            print("PHASE 'C2C' FRACTION AT 409.72km: " + str(ctc_list[55]))
            print("PHASE 'CPX' FRACTION AT 409.72km: " + str(cpx_list[55]))
            print("PHASE 'GT' FRACTION AT 409.72km: " + str(gt_list[55]))
            print("PHASE 'CPV' FRACTION AT 409.72km: " + str(cpv_list[55]))
            print("PHASE 'OL' FRACTION AT 409.72km: " + str(ol_list[55]))
            print("PHASE 'WA' FRACTION AT 409.72km: " + str(wa_list[55]))
            print("PHASE 'RI' FRACTION AT 409.72km: " + str(ri_list[55]))
            print("PHASE 'IL' FRACTION AT 409.72km: " + str(il_list[55]))
            print("PHASE 'PV' FRACTION AT 409.72km: " + str(pv_list[55]))
            print("PHASE 'PPV' FRACTION AT 409.72km: " + str(ppv_list[55]))
            print("PHASE 'CF' FRACTION AT 409.72km: " + str(cf_list[55]))
            print("PHASE 'MW' FRACTION AT 409.72km: " + str(mw_list[55]))
            print("PHASE 'QTZ' FRACTION AT 409.72km: " + str(qtz_list[55]))
            print("PHASE 'COES' FRACTION AT 409.72km: " + str(coes_list[55]))
            print("PHASE 'ST' FRACTION AT 409.72km: " + str(st_list[55]))
            print("PHASE 'APBO' FRACTION AT 409.72km: " + str(apbo_list[55]))
            print("PHASE 'KY' FRACTION AT 409.72km: " + str(ky_list[55]))
            print("PHASE 'NEPH' FRACTION AT 409.72km: " + str(neph_list[55]) + "\n")


            outputfile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(starname, "PASS", str(plg_list[55]), str(sp_list[55]),
                str(opx_list[55]), str(ctc_list[55]), str(cpx_list[55]), str(gt_list[55]), str(cpv_list[55]), str(ol_list[55]), str(wa_list[55]), str(ri_list[55]), str(il_list[55])
                , str(pv_list[55]), str(ppv_list[55]), str(cf_list[55]), str(mw_list[55]), str(qtz_list[55]), str(coes_list[55]), str(st_list[55])
                , str(apbo_list[55]), str(ky_list[55]), str(neph_list[55])))

        except:
            hefesto_stars_fail.append(starname)
            outputfile.write("{},{}\n".format(starname, "FAIL"))
            pass

    outputfile.close()




__init__()