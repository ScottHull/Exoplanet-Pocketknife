import os
import shutil
import pandas as pd

class _AtomicWeights:

    def __init__(self):
        self.fe = 55.845
        self.mg = 24.305
        self.si = 28.086
        self.ca = 40.078
        self.al = 26.982
        self.ti = 47.867
        self.na = 22.99
        self.o = 15.99


class _OxideCationNumbers:

    def __init__(self):
        self.fe = 1  # feo, 1
        self.mg = 1  # mgo, 1
        self.si = 1  # sio2, 1
        self.ca = 1  # cao, 1
        self.al = 2  # al2o3, 2
        self.ti = 1  # tio2, 1
        self.na = 2  # na2o, 2


class _OxideWeights:

    def __init__(self):
        self.atomic_weights = _AtomicWeights()
        self.oxide_cation_numbers = _OxideCationNumbers()
        self.feo = (self.atomic_weights.fe * self.oxide_cation_numbers.fe) + self.atomic_weights.o
        self.mgo = (self.atomic_weights.mg * self.oxide_cation_numbers.mg) + self.atomic_weights.o
        self.sio2 = (self.atomic_weights.si * self.oxide_cation_numbers.si) + (self.atomic_weights.o * 2)
        self.cao = (self.atomic_weights.ca * self.oxide_cation_numbers.ca) + self.atomic_weights.o
        self.al2o3 = (self.atomic_weights.al * self.oxide_cation_numbers.al) + (self.atomic_weights.o * 3)
        self.tio2 = (self.atomic_weights.ti * self.oxide_cation_numbers.ti) + (self.atomic_weights.o * 2)
        self.na2o = (self.atomic_weights.na * self.oxide_cation_numbers.na) + self.atomic_weights.o

class HeFESTpFileWriter:

    def __init__(self, from_path, to_path, temperatures, material):
        self.df = pd.read_csv(from_path)
        self.to_path = to_path
        self.temperatures = temperatures
        self.material = material
        self.BSP_FILE_FORMAT = "0,20,80,{},0,-2,0\n6,2,4,2\noxides\nSi          {}      5.39386    0\nMg          {}     2.71075    0\n" \
                             "Fe          {}      .79840    0\nCa            {}      .31431    0\nAl            {}      .96680    0\n" \
                             "Na            {}      .40654    0\n1,1,1\ninv251010\n47\nphase plg\n1\nan\nab\nphase sp\n0\nsp\nhc\n" \
                             "phase opx\n1\nen\nfs\nmgts\nodi\nphase c2c\n0\nmgc2\nfec2\nphase cpx\n1\ndi\nhe\ncen\ncats\njd\n" \
                             "phase gt\n0\npy\nal\ngr\nmgmj\njdmj\nphase cpv\n0\ncapv\nphase ol\n1\nfo\nfa\nphase wa\n0\nmgwa\nfewa\n" \
                             "phase ri\n0\nmgri\nferi\nphase il\n0\nmgil\nfeil\nco\nphase pv\n0\nmgpv\nfepv\nalpv\nphase ppv\n0\nmppv\n" \
                             "fppv\nappv\nphase cf\n0\nmgcf\nfecf\nnacf\nphase mw\n0\npe\nwu\nphase qtz\n1\nqtz\nphase coes\n0\ncoes\n" \
                             "phase st\n0\nst\nphase apbo\n0\napbo\nphase ky\n0\nky\nphase neph\n0\nneph"
        self.MORB_FILE_FORMAT = "0,20,80,{},0,-2,0\n6,2,4,2\noxides\nSi           {}     5.33159    0\n" \
                             "Mg           {}     1.37685    0\nFe           {}      .55527    0\n" \
                             "Ca           {}     1.33440    0\nAl           {}     1.82602    0\n" \
                             "Na           {}     0.71860    0\n1,1,1\ninv251010\n47\nphase plg\n1\nan\nab\nphase sp\n0\nsp\n" \
                             "hc\nphase opx\n1\nen\nfs\nmgts\nodi\nphase c2c\n0\nmgc2\nfec2\nphase cpx\n1\ndi\nhe\ncen\ncats\n" \
                             "jd\nphase gt\n0\npy\nal\ngr\nmgmj\njdmj\nphase cpv\n0\ncapv\nphase ol\n1\nfo\nfa\nphase wa\n0\n" \
                             "mgwa\nfewa\nphase ri\n0\nmgri\nferi\nphase il\n0\nmgil\nfeil\nco\nphase pv\n0\nmgpv\nfepv\nalpv\n" \
                             "phase ppv\n0\nmppv\nfppv\nappv\nphase cf\n0\nmgcf\nfecf\nnacf\nphase mw\n0\npe\nwu\nphase qtz\n" \
                             "1\nqtz\nphase coes\n0\ncoes\nphase st\n0\nst\nphase apbo\n0\napbo\nphase ky\n0\nky\nphase neph\n" \
                             "0\nneph"

    def __oxide_pct_to_cation_pct(self, df, row):
        mgo = self.df['MgO'][row].item()
        sio2 = self.df['SiO2'][row].item()
        feo = self.df['FeO'][row].item()
        al2o3 = self.df['Al2O3'][row].item()
        na2o = self.df['Na2O'][row].item()
        cao = self.df['CaO'][row].item()
        tio2 = self.df['TiO2'][row].item()
        sum = (mgo + sio2 + feo + al2o3 + na2o + cao + tio2)

        c = _OxideCationNumbers()
        o = _OxideWeights()
        print(o.mgo, o.sio2, o.feo, o.al2o3, o.na2o, o.cao, o.tio2)
        mg = (mgo / o.mgo) * c.mg
        si = (sio2 / o.sio2) * c.si
        fe = (feo / o.feo) * c.fe
        al = (al2o3 / o.al2o3) * c.al
        na = (na2o / o.na2o) * c.na
        ca = (cao / o.cao) * c.ca
        ti = (tio2 / o.tio2) * c.ti

        sum = (mg + si + fe + al + na + ca + ti)

        mg = mg / sum * 100.0
        si = si / sum * 100.0
        fe = fe / sum * 100.0
        al = al / sum * 100.0
        na = na / sum * 100.0
        ca = ca / sum * 100.0
        ti = ti / sum * 100.0

        return {
            'mg': mg,
            'si': si,
            'fe': fe,
            'al': al,
            'na': na,
            'ca': ca,
            'ti': ti
        }


    def writefiles(self):
        for t in self.temperatures:
            print(t)
            if os.path.exists(self.to_path + "/" + str(t)):
                shutil.rmtree(self.to_path + "/" + str(t))
            os.mkdir(self.to_path + "/" + str(t))
            for row in self.df.index:
                if len(str(self.df['MgO'][row])) > 0:
                    star = self.df['Star'][row]
                    print(star)
                    cations = self.__oxide_pct_to_cation_pct(df=self.df, row=row)
                    mg = cations['mg']
                    si = cations['si']
                    fe = cations['fe']
                    al = cations['al']
                    na = cations['na']
                    ca = cations['ca']
                    ti = cations['ti']

                    if self.material.lower() == 'bsp':
                        bsp_contents = self.BSP_FILE_FORMAT.format(t, si, mg, fe, ca, al, na)
                        with open(self.to_path + "/" + str(t) + "/{}_{}_{}_HeFESTo_Input_File.txt".format(star, self.material.upper(), t), 'w') as infile:
                            infile.write(bsp_contents)
                            infile.close()
                    else:
                        morb_contents = self.MORB_FILE_FORMAT.format(t, si, mg, fe, ca, al, na)
                        with open(self.to_path + "/" + str(t) + "/{}_{}_{}_HeFESTo_Input_File.txt".format(star, self.material.upper(), t), 'w') as infile:
                            infile.write(morb_contents)
                            infile.close()


df_paths = [
    "/Users/scotthull/Documents - Scott’s MacBook Pro/PhD Research/depleted-lithosphere/adibekyan_f1200_depleted_lithosphere_oxides.csv",
    "/Users/scotthull/Documents - Scott’s MacBook Pro/PhD Research/depleted-lithosphere/adibekyan_f1400_depleted_lithosphere_oxides.csv",
    "/Users/scotthull/Documents - Scott’s MacBook Pro/PhD Research/depleted-lithosphere/adibekyan_f1600_depleted_lithosphere_oxides.csv",
    "/Users/scotthull/Documents - Scott’s MacBook Pro/PhD Research/depleted-lithosphere/kepler_f1200_depleted_lithosphere_oxides.csv",
    "/Users/scotthull/Documents - Scott’s MacBook Pro/PhD Research/depleted-lithosphere/kepler_f1400_depleted_lithosphere_oxides.csv",
    "/Users/scotthull/Documents - Scott’s MacBook Pro/PhD Research/depleted-lithosphere/kepler_f1600_depleted_lithosphere_oxides.csv",
]

temperatures = [
    [1200],
    [1200, 1400],
    [1200, 1400, 1600],
    [1200],
    [1200, 1400],
    [1200, 1400, 1600]
]

to_paths = [
    "/Users/scotthull/Documents - Scott’s MacBook Pro/PhD Research/depleted-lithosphere/adibekyan_depleted_lithosphere_compositions_f1200",
    "/Users/scotthull/Documents - Scott’s MacBook Pro/PhD Research/depleted-lithosphere/adibekyan_depleted_lithosphere_compositions_f1400",
    "/Users/scotthull/Documents - Scott’s MacBook Pro/PhD Research/depleted-lithosphere/adibekyan_depleted_lithosphere_compositions_f1600",
    "/Users/scotthull/Documents - Scott’s MacBook Pro/PhD Research/depleted-lithosphere/kepler_depleted_lithosphere_compositions_f1200",
    "/Users/scotthull/Documents - Scott’s MacBook Pro/PhD Research/depleted-lithosphere/kepler_depleted_lithosphere_compositions_f1400",
    "/Users/scotthull/Documents - Scott’s MacBook Pro/PhD Research/depleted-lithosphere/kepler_depleted_lithosphere_compositions_f1600"
]

for index, path in enumerate(df_paths):
    temps = temperatures[index]
    to_path = to_paths[index]
    HeFESTpFileWriter(from_path=path, to_path=to_path, temperatures=temps, material="BSP").writefiles()
