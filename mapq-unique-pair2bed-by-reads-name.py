#!/usr/bin/env python
# Report uniquely aligned pairs from BWA sam output.
from __future__ import print_function
import sys

if len(sys.argv) == 2:
    input_file = sys.stdin
elif len(sys.argv) == 3:
    input_file = open(sys.argv[2],"r")
else:
    print ("Usage: python *.py mapq input.sam or stdin")
    sys.exit(-1)

i = 0
uPair = 0
mapq = int(sys.argv[1])

for l in input_file:
#write header info
	if l.startswith('@'):
		#sys.stdout.write( l )
		continue
#precess reads
	lsplit = l.strip().split('\t')
	i += 1
	if int(lsplit[4]) >= mapq:
		if (i % 2) ==1:
			r1_name = lsplit[0]
			uPair = 1
			continue
		elif (i % 2) ==0:
			r2_name = lsplit[0]
			if uPair == 1 and r1_name == r2_name:
				if int(lsplit[8]) > 0:
					chrom = str(lsplit[2])
					chromStart = int(lsplit[3]) - 1
					chromEnd = int(lsplit[3]) -1 + int(lsplit[8])
					fraglength = chromEnd - chromStart				
					print (chrom, chromStart, chromEnd, fraglength, sep='\t')
				elif int(lsplit[8]) < 0:
					chrom = str(lsplit[2])
					chromStart = int(lsplit[7]) - 1
					chromEnd = int(lsplit[7]) - 1 - int(lsplit[8])
					fraglength = chromEnd - chromStart				
					print (chrom, chromStart, chromEnd, fraglength, sep='\t')
			else:
				print ("reads name do not match!!")
				break
				
	elif int(lsplit[4]) < mapq:
		uPair = 0
		continue
				
input_file.close()