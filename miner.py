import sys
import apriori


if len(sys.argv) < 3:
    print("Expected format: python miner.py <data> <out file> <OPTIONAL sigma> <OPTIONAL min set size>")
elif len(sys.argv) >= 3:
    data = sys.argv[1]
    out_file = sys.argv[2]
    try:
        sigma = int(sys.argv[3])
        min_set_size = int(sys.argv[4])
    except IndexError:
        sigma = 4
        min_set_size = 3

    print("Setting sigma to {} and minimum set size to {}.".format(sigma,min_set_size))

    AP = apriori.APriori(data=sys.argv[1],out=sys.argv[2])
    AP.find_frequent(sigma,min_set_size)
