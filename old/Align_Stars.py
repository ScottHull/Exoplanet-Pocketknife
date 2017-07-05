import csv, os





def match_stars(filename):

    match_to = []
    match_with = []
    star_data = []

    if "aligned_output.csv" in os.listdir(os.getcwd()):
        os.remove("aligned_output.csv")

    output = open("aligned_output.csv", 'a')

    with open(filename, 'r') as infile:
        reader = csv.reader(infile)
        for row in reader:
            match_to.append(row[0])
            match_with.append(row[1])
            star_data.append(row[2:])
    infile.close()

    for i in match_with:
        if i in match_to:
            print("Matched {}!".format(i))
            star_data_single = star_data[int(match_with.index(i))]
            star_data_single_formatted = ",".join(str(z) for z in star_data_single)
            output.write("{},{}\n".format(i, star_data_single_formatted))
        else:
            output.write("\n")

    output.close()










def initialization():

    print("\n\n\nPlease create a .csv file with the list of stars you would like to align your outputs to"
          "in the first column, and your outputs in the second+ columns.  The script will match the outputs with"
          "the list in the first column.  No header is required.\n\nPlease enter your .csv filename:")
    csv_name = input(">>> ")
    match_stars(filename=str(csv_name))






initialization()