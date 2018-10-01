import os
import sys
import shutil
import pandas as pd


na2o_molwt = 61.9785
mgo_molwt = 40.3040
al2o3_molwt = 101.9601
sio2_molwt = 60.0835
cao_molwt = 56.0770
tio2_molwt = 79.8650
cr2o3_molwt = 151.9892
feo_molwt = 71.8440
nio_molwt = 74.6924
fe2o3_molwt = 159.687

num_na2o_cations = 2
num_mgo_cations = 1
num_al2o3_cations = 2
num_sio2_cations = 1
num_cao_cations = 1
num_tio2_cations = 1
num_cr2o3_cations = 2
num_feo_cations = 1
num_nio_cations = 1
num_fe2o3_cations = 2


def renormalize(sio2, feo, mgo, na2o, al2o3, cao):
    mol_sio2 = (sio2 / sio2_molwt) / num_sio2_cations
    mol_feo = (feo / feo_molwt) / num_feo_cations
    mol_mgo = (mgo / mgo_molwt) / num_mgo_cations
    mol_na2o = (na2o / na2o_molwt) / num_na2o_cations
    mol_al2o3 = (al2o3 / al2o3_molwt) / num_al2o3_cations
    mol_cao = (cao / cao_molwt) / num_cao_cations

    norm_sum = (mol_sio2 + mol_feo + mol_mgo + mol_na2o + mol_al2o3 + mol_cao)

    mol_sio2 = mol_sio2 / norm_sum * 100
    mol_feo = mol_feo / norm_sum * 100
    mol_mgo = mol_mgo / norm_sum * 100
    mol_na2o = mol_na2o / norm_sum * 100
    mol_al2o3 = mol_al2o3 / norm_sum * 100
    mol_cao = mol_cao / norm_sum * 100

    confirm_sum = (mol_sio2 + mol_feo + mol_mgo + mol_na2o + mol_al2o3 + mol_cao)

    if confirm_sum != 100.0:
        print("Normalized sum not 100!")
        sys.exit(1)

    composition = {
        'sio2': mol_sio2,
        'feo': mol_feo,
        'mgo': mol_mgo,
        "na2o": mol_na2o,
        "al2o3": mol_al2o3,
        'cao': mol_cao
    }

    return composition



def templateMORB(temperature, sio2, mgo, feo, cao, al2o3, na2o):
    template = "0,20,80,{},0,-2,0\n6,2,4,2\noxides\nSi           {}     0.0    0\n" \
         "Mg           {}     0.0    0\nFe           {}      0.0    0\n" \
         "Ca           {}     0.0    0\nAl           {}     0.0    0\n" \
         "Na           {}     0.0    0\n1,1,1\ninv251010\n47\nphase plg\n1\nan\nab\nphase sp\n0\nsp\n" \
         "hc\nphase opx\n1\nen\nfs\nmgts\nodi\nphase c2c\n0\nmgc2\nfec2\nphase cpx\n1\ndi\nhe\ncen\ncats\n" \
         "jd\nphase gt\n0\npy\nal\ngr\nmgmj\njdmj\nphase cpv\n0\ncapv\nphase ol\n1\nfo\nfa\nphase wa\n0\n" \
         "mgwa\nfewa\nphase ri\n0\nmgri\nferi\nphase il\n0\nmgil\nfeil\nco\nphase pv\n0\nmgpv\nfepv\nalpv\n" \
         "phase ppv\n0\nmppv\nfppv\nappv\nphase cf\n0\nmgcf\nfecf\nnacf\nphase mw\n0\npe\nwu\nphase qtz\n" \
         "1\nqtz\nphase coes\n0\ncoes\nphase st\n0\nst\nphase apbo\n0\napbo\nphase ky\n0\nky\nphase neph\n" \
         "0\nneph".format(temperature, sio2, mgo, feo, cao, al2o3, na2o)

    return template


def templateBSP(temperature, sio2, mgo, feo, cao, al2o3, na2o):
    template = "0,20,80,{},0,-2,0\n6,2,4,2\noxides\nSi          {}      0.0    0\nMg          {}     0.0    0\n" \
        "Fe          {}      0.0    0\nCa            {}      0.0    0\nAl            {}      0.0    0\n" \
        "Na            {}      0.0    0\n1,1,1\ninv251010\n47\nphase plg\n1\nan\nab\nphase sp\n0\nsp\nhc\n" \
        "phase opx\n1\nen\nfs\nmgts\nodi\nphase c2c\n0\nmgc2\nfec2\nphase cpx\n1\ndi\nhe\ncen\ncats\njd\n" \
        "phase gt\n0\npy\nal\ngr\nmgmj\njdmj\nphase cpv\n0\ncapv\nphase ol\n1\nfo\nfa\nphase wa\n0\nmgwa\nfewa\n" \
        "phase ri\n0\nmgri\nferi\nphase il\n0\nmgil\nfeil\nco\nphase pv\n0\nmgpv\nfepv\nalpv\nphase ppv\n0\nmppv\n" \
        "fppv\nappv\nphase cf\n0\nmgcf\nfecf\nnacf\nphase mw\n0\npe\nwu\nphase qtz\n1\nqtz\nphase coes\n0\ncoes\n" \
        "phase st\n0\nst\nphase apbo\n0\napbo\nphase ky\n0\nky\nphase neph\n0\nneph".format(temperature,
                                                                                            sio2, mgo, feo, cao, al2o3, na2o)
    return template


if __name__ == "__main__":
    temperatures = []
    compfile = None
    modelType = None
    print("\n\n\nEnter temperatures in degK. Enter 'e' when finished.")
    while True:
        inp = input(">>> ")
        if inp.lower() == "e":
            break
        else:
            temperatures.append(inp)

    print("\nEnter the name of the CSV compositional input file in the working directory.")
    while True:
        inp = input(">>> ")
        if inp in os.listdir(os.getcwd()):
            compfile = pd.read_csv(inp)
            break
        else:
            print("That file is not in the working directory. Try again.")

    print("BSP or MORB?")
    while True:
        inp = input(">>> ").lower()
        if inp == "morb" or inp == "bsp":
            modelType = inp.upper()
            if os.path.exists(os.getcwd() + "/" + modelType.upper()):
                shutil.rmtree(os.getcwd() + "/" + modelType.upper())
            os.mkdir(os.getcwd() + "/" + modelType.upper())
            break
        else:
            print("That is not a proper model type. Try again.")

    for temp in temperatures:
        todir = os.getcwd() + "/" + modelType.upper() + "/" + str(temp)
        os.mkdir(todir)
        for row in compfile.index:
            star = compfile['Star'][row]
            feo = compfile['FeO'][row]
            na2o = compfile['Na2O'][row]
            mgo = compfile['MgO'][row]
            al2o3 = compfile['Al2O3'][row]
            sio2 = compfile['SiO2'][row]
            cao = compfile['CaO'][row]
            tio2 = compfile['TiO2'][row]
            cr2o3 = compfile['Cr2O3'][row]

            if not pd.isnull(compfile['SiO2'][row]):

                normComposition = renormalize(sio2=sio2, feo=feo, na2o=na2o, mgo=mgo, al2o3=al2o3, cao=cao)

                if modelType == 'BSP':
                    f = open(todir + "/{}_{}_HeFESTo_Infile.txt".format(star, modelType), 'a')
                    tostr = templateBSP(
                        temperature=temp,
                        sio2=normComposition['sio2'],
                        mgo=normComposition['mgo'],
                        feo=normComposition['feo'],
                        na2o=normComposition['na2o'],
                        cao=normComposition['cao'],
                        al2o3=normComposition['al2o3']
                    )
                    f.write(tostr)
                    f.close()

                elif modelType == 'MORB':
                    f = open(todir + "/{}_{}_HeFESTo_Infile.txt".format(star, modelType), 'a')
                    tostr = templateMORB(
                        temperature=temp,
                        sio2=normComposition['sio2'],
                        mgo=normComposition['mgo'],
                        feo=normComposition['feo'],
                        na2o=normComposition['na2o'],
                        cao=normComposition['cao'],
                        al2o3=normComposition['al2o3']
                    )
                    f.write(tostr)
                    f.close()
