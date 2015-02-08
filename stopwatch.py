"""This script is an advanced stopwatch
designed for use by the DTU Roadrunners
at the Shell Eco Marathon. v0.1 by Nils
Toudal."""

#Import needed functions
import time
import sys
import linecache
import os

def start():
    goOn = False
    #This function defines the start time if the user chooses to.
    while goOn!=True:
        inp = raw_input('Enter S for Start or E for Exit: ')
        if inp == 'S':
            tStart = time.time()
            goOn = True
        elif inp == 'E':
            print 'You terminated the program.'
            print 'Goodbye\n'
            sys.exit()
        else:
            print 'Your input was not accepted.'
            print 'Please enter a valid input.'
            goOn = False
    return tStart

def lapTime(startTime): #, data
  #This function writes the time since startTime in datafile choosen by user
  leng = str(file_len(trackfile) - 12)
  print  'There are ' + leng + ' positions on the track.'
  text = 'Enter a position between 1 and ' + leng +', or enter E for exit: '
  place = raw_input(text)
  if place == 'E':
    print 'You terminated the program.'
    print 'Goodbye \n'
    return False
  else:
    t = time.time()
    delta = t - startTime
    data.write(str(delta) + ' ' + place + '\n')
    #print ' '*22 + 'Time: '+ str(delta) + ' '*4 + 'Position: ' + place + '\n'
    return True

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def load_track(track):
    leng = file_len(trackfile) - 12
    zones = [0]*leng
    for n in range(leng):
        zones[n] = linecache.getline('trackdata.txt',13+n)
        zones[n] = zones[n][0:len(zones[n])-1]
        zones[n] = str(zones[n])
        zones[n] = zones[n].split(' ',2)
    return zones

def analyze(data,zonedict):
    #Read file from beginning, file is read on every itteration of while loop.
    #Not super elegant.
    data.seek(0,0)
    #Read data into content, to treat as a str
    content = data.read()
    #Split data into each line, will output a 2d array
    splits = content.splitlines()
    times = [0]*len(splits)
    sector = [0]*len(splits)
    for n in range(len(splits)):
        #Convert to string to use string methods. Back to 1d array.
        splits[n] = str(splits[n])
        #Split by space, into 2d again
        splits[n] = splits[n].split()
        #Time is first, then sector indicator.
        times[n] = splits[n][0]
        sector[n] = splits[n][1]
        #Print for confirmation
        print 'Line: ' +str(n+1) + ' Time: ' +times[n] + ' Sector: ' +sector[n]
        print 'Sector length: ' + str(zonedict[n+1][0])
        print 'Expected time: ' + str(zonedict[n+1][1]) + '\n'


def trackdict(trackfile):
    track.seek(0,0)
    #Read data into content, to treat as a str
    tcontent = track.read()
    tcontent = str(tcontent)
    tcontent = tcontent.split('zones:\n')
    tcontent = tcontent[1]
    tcontent = tcontent.split()
    zonedict = {}
    for n in range(len(tcontent)/2):
        zonedict[n+1] = [int(tcontent[n*2]),int(tcontent[n*2+1])]
    print zonedict
    return zonedict



#Ask user for output file name and trackname
#For development 'trackdata.txt' and 'some.dat ' are selected
filename = 'some.dat' #raw_input('Select a name for your output data file: ')
trackfile = 'trackdata.txt' #raw_input('Enter name of track data file: ')
mapfile = linecache.getline('trackdata.txt',4)
mapfile = mapfile[0:len(mapfile)-1]

#Files are opened
data = open(filename,'w+')
track = open(trackfile,'r')
themap = open(mapfile,'r')

#Before printing anything, clear terminal
os.system('clear')

#Map is printed from file and file is closed again.
trackname = linecache.getline('trackdata.txt',2)
print '\n \nThis is a map of ' + trackname
print themap.read()
themap.close()

#Zones are printed
zones = load_track(track)
a = 1
for obj in zones:
    print 'Zone ' + str(a) + ' length: ' + obj[0] + ', expected time: ' + obj[1]
    a = a + 1
print '\n'

#Zones area loaded from trackfile
zonedict = trackdict(trackfile)

#Time is started by user command
tStart = start()

#Race is going on as long as the user wants
race = 'go'
entries = 1
os.system('clear')
while race != False:
    themap = open(mapfile,'r')
    print themap.read()
    themap.close()
    #Analyze data on every run exept the first
    if race == True:
        analyze(data,zonedict)
    race = lapTime(tStart)
    #Clear terminal
    os.system('clear')

data.close()

result = open(filename,'r')
print result.read()

#At end files are closed for safety
result.close()
track.close()
