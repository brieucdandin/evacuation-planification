import sys

pathfile = "../Instances/"
#filename = sys.argv[1]
filename = "dense_10_30_3_1.full"

f = open(pathfile+filename,"r")
for x in f:
    print(x)
