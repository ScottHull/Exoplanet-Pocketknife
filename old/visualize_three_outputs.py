import os, csv
import matplotlib.pyplot as plt






def plotit(inputfile):

    x_ticks = ["2x Na", "Normal Na", "1/2x Na"]
    x_axis = [1, 2, 3]

    normal_greaterthan_half = []
    twice_greaterthan_normal = []
    twice_lessthan_half = []
    normal_stars = []


    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()
    fig3, ax3 = plt.subplots()
    fig4, ax4 = plt.subplots()
    fig5, ax5 = plt.subplots()

    if "buoyancy_report.csv" in os.listdir(os.getcwd()):
        os.remove("buoyancy_report.csv")

    output = open("buoyancy_report.csv", 'a')
    header = "Star,2xNa Buoyancy Force,Normal Na Buoyancy Force,1/2x Na Buoyancy Force"
    output.write("{}\n".format(header))

    with open(inputfile, 'r') as infile:
        reader = csv.reader(infile)
        for row in reader:
            if "" not in row and "FAILURE" not in row:
                star_name = row[0]
                if "M" in star_name:
                    data = []  # 2x Na at 0, normal Na at 1, 1/2 x Na at 2
                    twice = float(row[1])
                    normal = float(row[2])
                    half = float(row[3])
                    if normal <= half:
                        normal_greaterthan_half.append(star_name)
                    if twice <= normal:
                        twice_greaterthan_normal.append(star_name)
                    if twice <= half:
                        twice_lessthan_half.append(star_name)
                    data.append(twice)
                    data.append(normal)
                    data.append(half)
                    print(x_axis)
                    print(data)
                    ax2.plot(x_axis, data)
                else:
                    data = []  # 2x Na at 0, normal Na at 1, 1/2 x Na at 2
                    twice = float(row[1])
                    normal = float(row[2])
                    half = float(row[3])
                    if normal <= half:
                        normal_greaterthan_half.append(star_name)
                    if twice <= normal:
                        twice_greaterthan_normal.append(star_name)
                    if twice <= half:
                        twice_lessthan_half.append(star_name)
                    data.append(twice)
                    data.append(normal)
                    data.append(half)
                    print(x_axis)
                    print(data)
                    ax1.plot(x_axis, data)
    infile.close()


    with open(inputfile, 'r') as infile:
        reader = csv.reader(infile)
        for row in reader:
            if row[0] in normal_greaterthan_half:
                data2 = [] # 2x Na at 0, normal Na at 1, 1/2 x Na at 2
                data2.append(row[1])
                data2.append(row[2])
                data2.append(row[3])
                ax3.plot(x_axis, data2)
            if row[0] in twice_greaterthan_normal:
                data2 = [] # 2x Na at 0, normal Na at 1, 1/2 x Na at 2
                data2.append(row[1])
                data2.append(row[2])
                data2.append(row[3])
                ax4.plot(x_axis, data2)
            if row[0] in twice_lessthan_half:
                data2 = [] # 2x Na at 0, normal Na at 1, 1/2 x Na at 2
                data2.append(row[1])
                data2.append(row[2])
                data2.append(row[3])
                ax5.plot(x_axis, data2)
            if not row[0] in normal_greaterthan_half and not row[0] in twice_greaterthan_normal and not row[0] in\
                    twice_lessthan_half:
                normal_stars.append(row[0])
                pass

    infile.close()

    with open(inputfile, 'r') as infile:
        output.write("\n\nNormal Na Buoyancy >= 1/2x Na Buoyancy")
        reader = csv.reader(infile)
        for row in reader:
            if row[0] in normal_greaterthan_half:
                row_formatted = ",".join(i for i in row)
                output.write("{}\n".format(row_formatted))
    infile.close()

    with open(inputfile, 'r') as infile:
        output.write("\n\n\nNormal Na Buoyancy Force <= 1/2x Na Buoyancy Force\n")
        reader = csv.reader(infile)
        for row in reader:
            if row[0] in normal_greaterthan_half:
                row_formatted = ",".join(i for i in row)
                output.write("{}\n".format(row_formatted))
    infile.close()
    with open(inputfile, 'r') as infile:
        output.write("\n\n\n2x Na Buoyancy Force <= Normal Na Buoyancy Force\n")
        reader = csv.reader(infile)
        for row in reader:
            if row[0] in twice_greaterthan_normal:
                row_formatted = ",".join(i for i in row)
                output.write("{}\n".format(row_formatted))
    infile.close()
    with open(inputfile, 'r') as infile:
        output.write("\n\n\n2x Na Buoyancy Force <= 1/2x Na Buoyancy Force\n")
        reader = csv.reader(infile)
        for row in reader:
            if row[0] in twice_lessthan_half:
                row_formatted = ",".join(i for i in row)
                output.write("{}\n".format(row_formatted))
    infile.close()



    fig1.set_tight_layout(True)
    fig2.set_tight_layout(True)
    fig3.set_tight_layout(True)
    fig4.set_tight_layout(True)
    fig5.set_tight_layout(True)



    ax1.set_title("Adibekyan 2012 Stars")
    ax2.set_title("Kepler Stars")
    ax3.set_title("Normal Na >= 1/2x Na Buoyant Force")
    ax4.set_title("2x Na <= Normal Na Buoyant Force")
    ax5.set_title("2xNa <= 1/2x Na Buoyant Force")
    ax1.xaxis.major.locator.set_params(nbins=3)
    ax2.xaxis.major.locator.set_params(nbins=3)
    ax3.xaxis.major.locator.set_params(nbins=3)
    ax4.xaxis.major.locator.set_params(nbins=3)
    ax5.xaxis.major.locator.set_params(nbins=3)
    ax1.set_xticklabels(x_ticks, rotation=45)
    ax1.grid()
    ax1.set_xlabel("Na Abundance")
    ax1.set_ylabel("Buoyancy Force (N/m)")
    ax2.set_xticklabels(x_ticks, rotation=45)
    ax2.grid()
    ax2.set_xlabel("Na Abundance")
    ax2.set_ylabel("Buoyancy Force (N/m)")
    ax3.set_xticklabels(x_ticks, rotation=45)
    ax3.grid()
    ax3.set_xlabel("Na Abundance")
    ax3.set_ylabel("Buoyancy Force (N/m)")
    ax4.set_xticklabels(x_ticks, rotation=45)
    ax4.grid()
    ax4.set_xlabel("Na Abundance")
    ax4.set_ylabel("Buoyancy Force (N/m)")
    ax5.set_xticklabels(x_ticks, rotation=45)
    ax5.grid()
    ax5.set_xlabel("Na Abundance")
    ax5.set_ylabel("Buoyancy Force (N/m)")

    print("\n\nNormal <= Half\n{}".format(normal_greaterthan_half))
    print("\n\nTwice <= Normal\n{}".format(twice_greaterthan_normal))
    print("\n\nTwice Na <= Half\n{}".format(twice_lessthan_half))

    output.close()

    print("\n\nNormal Na >= 1/2x Na Buoyancy Force: {} stars\n2x Na Buoyancy Force >= Normal Na Buoyancy Force: {} stars"
          "\n2xNa Buoyancy Force <= 1/2x Na Buoyancy Force: {} stars\n""Normal: {} stars\n".format(len(normal_greaterthan_half),
            len(twice_greaterthan_normal), len(twice_lessthan_half), len(normal_stars)))



    fig1.savefig("Adibekyan_2012_Stars.png", format='png')
    fig2.savefig("Kepler_Stars.png", format='png')
    fig3.savefig("NormalNa_lessthan_HalfNa.png", format='png')
    fig4.savefig("2xNa_lessthan_NormalNa.png", format='png')
    fig5.savefig("2xNa_lessthan_halfNa.png", format='png')

    plt.show()
    plt.close()







def initialization():

    print("\n\n\nPlease input a .csv with three columns of data to be plotted.")
    print("This is useful for visualizing normal, 1/2x, and 2x Na outputs.\n")
    in1 = input(">>> ")
    plotit(inputfile=in1)




initialization()