#!/usr/bin/env python

import sys
from subprocess import Popen, PIPE

def getmounts():
	p = Popen(['/etc/init.d/netfs', 'status'], stdout=PIPE, stderr=PIPE)
	retcode = p.wait()
	outputarr = []
	actfound = 0
	for i in iter(p.stdout.readline, ''):
		outputarr.append(i.rstrip('/').rstrip())
	outputarr.remove(outputarr[0])
	for index, item in enumerate(outputarr):
		if item.strip() == "Active NFS mountpoints:":
			actfound = 1
			break
	if actfound == 0:
		sys.exit("No active mountpoints found. Check '/sbin/service netfs status' for details\n")
	index+=1
	#print "Active mountpoints found starting at index [%s]\n" % index
	#print "First active mountpoint is [%s]\n" % index
	outputarr=outputarr[index:]
	#f=open('/reserved/mounts.log', 'a')
	#f.write("%s\n" % outputarr)
	#f.close()
	#print outputarr
	return outputarr, p.stderr.readlines(), retcode

def getnfsstats(mntpt):
	#print "mntpt is [%s]\n" % mntpt
	#f=open('/reserved/mntpt.log', 'a')
	#f.write("%s\n" % mntpt)
	#f.close()
	p = Popen(['/usr/sbin/nfsiostat', '%s' % mntpt], stdout=PIPE, stderr=PIPE)
	retcode = p.wait()
	statsarr = []
	for i in iter(p.stdout.readline, ''):
		statsarr.append(i.rstrip())

	return statsarr, p.stderr.readlines(), retcode

class NfsMntStat:
	def __init__(self, mntpt, statdict):
		self.mntpt = mntpt
		self.statdict = statdict
#		print self.statdict[0]
#		print self.statdict[0][0]
		#print "First entry: [%s]\n" % self.statdict[0][1].split()[0]
		#f=open('/reserved/python.log', 'a')
		#f.write("%s\n" % str(self.statdict))
		#f.close()
		self.nfssrc = self.statdict[0][1].split()[0]
		self.oppersec = self.statdict[0][4].split()[0]
		self.rpcbklog = self.statdict[0][4].split()[1]
		self.ropspersec = self.statdict[0][6].split()[0]
		self.rkbpersec = self.statdict[0][6].split()[1]
		self.rkbperop = self.statdict[0][6].split()[2]
		self.rretrans = self.statdict[0][6].split()[3]
		self.ravgrtt = self.statdict[0][6].split()[5]
		self.ravexe = self.statdict[0][6].split()[6]
		self.wopspersec = self.statdict[0][8].split()[0]
		self.wkbpersec = self.statdict[0][8].split()[1]
		self.wkbperop = self.statdict[0][8].split()[2]
		self.wretrans = self.statdict[0][8].split()[3]
		self.wavgrtt = self.statdict[0][8].split()[5]
		self.wavgexe = self.statdict[0][8].split()[6]
	
	def listStats(self):
		print "Mountpoint: [%s]" % self.mntpt
		print "NFS Source: [%s]" % self.nfssrc
		print "Ops/s: [%s]" % self.oppersec
		print "RPC Backlog: [%s]" % self.rpcbklog
		print "Read Ops/s: [%s]" % self.ropspersec
		print "Read kB/s: [%s]" % self.rkbpersec
		print "Read retransmits: [%s]" % self.rretrans
		print "Read Avg RTT: [%s]" % self.ravgrtt
		print "Read Avg exe: [%s]" % self.ravexe
		print "Write Ops/s: [%s]" % self.wopspersec
		print "Write kB/s: [%s]" % self.wkbpersec
		print "Write kB/op: [%s]" % self.wkbperop
		print "Write retransmits: [%s]" % self.wretrans
		print "Write Avg RTT: [%s]" % self.wavgrtt
		print "Write Avg exe: [%s]" % self.wavgexe
		
		print "\n"
	
	def getMntpt(self):
		return self.mntpt

	def getNfssrc(self):
		return self.nfssrc

	def getOpspersec(self):
		return self.oppersec

	def getRPCbklog(self):
		return self.rpcbklog

	def getRopspersec(self):
		return self.ropspersec

	def getRretransmits(self):
		return self.rretrans

	def getRavgrtt(self):
		return self.ravgrtt

	def getRavgexe(self):
		return self.ravexe

	def getWopspersec(self):
		return self.wopspersec

	def getWkbpersec(self):
		return self.wkbpersec

	def getWkbperop(self):
		return self.wkbperop

	def getWretransmits(self):
		return self.wretrans

	def getWavgrtt(self):
		return self.wavgrtt

	def getWavgexe(self):
		return self.wavgexe

	def getStats(self):
		nfsstatdict = [self.oppersec, self.rpcbklog, self.ropspersec, self.rretrans, self.ravgrtt, self.ravexe, self.wopspersec, self.wkbpersec, self.wkbperop, self.wretrans, self.wavgrtt, self.wavgexe]
		return nfsstatdict

def listStats(nfsobj):
	for dkey in mntstats.keys():
		if mntstats[dkey][1] == 0:
			x = NfsMntStat(dkey, mntstats[dkey])
		x.listStats()

def nfsstatInit():
	outarr, stderr, retcode1 = getmounts()
	mntstats = {}
	for i in outarr:
		mntinfo, mnterr, mntret = getnfsstats(i)
		mntstats[i] = [mntinfo, mntret]

	return mntstats
	

def main():

	mntstats = nfsstatInit()
	for dkey in mntstats.keys():
		#print "Mount point:\t[%s] \nStats:\t[%s]\nRetCode:\t[%s]\n" % (dkey,mntstats[dkey][0],mntstats[dkey][1])
#		print mntstats[dkey]
		#print "Dkey is [%s]\n" % dkey
		#print "Retcode is [%s]\n" % mntstats[dkey][1]
		if mntstats[dkey][1] == 0:
			x = NfsMntStat(dkey, mntstats[dkey])
		x.listStats()
	

if __name__ == "__main__":
	main()
