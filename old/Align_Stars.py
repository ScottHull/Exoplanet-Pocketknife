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

    matched_val = 0
    missed_val = 0

    for i in match_to:
        if i in match_with:
            print("[~] Matched {}! ({} + {})".format(i, i, match_with[match_with.index(i)]))
            star_data_single = star_data[int(match_with.index(i))]
            star_data_single_formatted = ",".join(str(z) for z in star_data_single)
            output.write("{},{}\n".format(i, star_data_single_formatted))
            matched_val += 1
        else:
            print("[X] Failed to find {}!".format(i))
            output.write("{},""\n".format(i))
            missed_val += 1

    print("\nMatched {}\nMissed {}\n\n".format(matched_val, missed_val))

    output.close()










def initialization():

    print("\n\n\nPlease create a .csv file with the list of stars you would like to align your outputs to"
          "in the first column, and your outputs in the second+ columns.  The script will match the outputs with"
          "the list in the first column.  No header is required.\n\nPlease enter your .csv filename:")
    csv_name = input(">>> ")
    match_stars(filename=str(csv_name))






initialization()
