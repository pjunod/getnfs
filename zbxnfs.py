#!/usr/bin/env python

import getnfs
import sys
from optparse import OptionParser

mntpt = sys.argv[1]
nfsdata = sys.argv[2]

nfsopts = {"oppersec":0, "rpcbklog":1, "ropspersec":2, "rretrans":3, "ravgrtt":4, "ravexe":5, "wopspersec":6, "wkbpersec":7, "wkbperop":8, "wretrans":9, "wavgrtt":10, "wavgexe":11}

if nfsdata in nfsopts.keys():
	mntstats = {}

	mntinfo, mnterr, mntret = getnfs.getnfsstats(mntpt)

	if mntret == 0:
		mntstats[mntpt] = [mntinfo, mntret]

		x = getnfs.NfsMntStat(mntpt, mntstats[mntpt])
		z = x.getStats()
	
		print z[nfsopts[nfsdata]]
	else:
		print "-1"
else:
	print "-1"

