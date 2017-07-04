import os, string, csv





def initialization():

    print("\nInput the name of a .csv with all of the values you want to check that each value does not exist more than once.")
    in1 = raw_input(">>> ")

    with open(in1, 'r') as infile:
        reader = csv.reader(infile)
    
        check_list = []
        check_with_list = []
        repeat_list = []
        single_list = []

        for row in reader:
            check_list.append(row[0])
        infile.close()

    for i in check_list:
        x = check_list.count(i)
        print("Length for star {}: {}".format(i, x))
        if x > 1:
            repeat_list.append(i)
        else:
            single_list.append(i)



#    print(repeat_list)
    print(len(repeat_list))
    print(len(single_list))


initialization()

