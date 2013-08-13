import sys
import time
import requests

from base_parser import BaseParser
from datetime import datetime
from datetime import timedelta

class ChandraParser(BaseParser):
  def __init__(self):
    BaseParser.__init__(self)
    self._telescope = 'Chandra'
    self._datetime_format = '%Y:%j:%H:%M:%S'


  def fetch_schedule(self):
    try:
      schedule = list()
      filename=sys.argv[1]
      for line in open(filename, "r" ):
        print line
        #TargetName                RA(J2000)    Dec(J2000)    PI                ProgName     pid   AOT         min_dur Start Of Execution (UTC)   AOR_key    AOR_LABEL
        #          1         2         3         4         5         6         7         8         9         0         1         2         3
        #0123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890
        #Seq #     ObsID Constr.    Target              Start        Time   SI   Grat    RA       Dec    Roll   Pitch   Slew
        #702849    15042 3              Sgr A 2013:223:23:12:44.143  49.4 ACIS-S NONE 266.4093 -28.9891 253.50 127.36  54.93 dss pspc rass
        #702836 P1 15029 0 SDSS J161027.41+1308 2013:224:13:22:52.143  15.0 ACIS-S NONE 242.6094  13.1595 253.10  96.39  48.11 dss pspc rass

        n = 0
        print "*" + line[36] + "*"
        if line[36] != " ":
          print "Offset +2"
          n = 2
        start_str = line[37+n:54+n].strip() # remove milliseconds
        duration  = line[59+n:62+n].strip() # remove milliseconds
        print "Start/end " + start_str + "," + duration
        start = datetime.strptime(start_str, self._datetime_format)
        end   = datetime.strptime(start_str, self._datetime_format) + timedelta(0,int(duration))
        target= line[18:36+n].strip()
        ra    = line[77+n:86+n].strip()
        dec   = line[86+n:94+n].strip()
        obsid = line[10+n:15+n].strip()
        if ra and dec:
          try:
            print ra + "," + dec
            coords = self._parse_coords(ra, dec)
          except:
            coords = None
          if coords:
            print coords
            #print start + "," + end
            observation = {
                  '_id'     : self._telescope + '|' + obsid,
                  'observation': obsid,
                  'source'  : self._telescope,
                  'target'  : target,
                  'ra'      : coords['ra_float'],
                  'dec'     : coords['dec_float'],
                  'ra_str'  : coords['ra_str'],
                  'dec_str' : coords['dec_str'],
                  'l'       : coords['l_float'],
                  'b'       : coords['b_float'],
                  'start'   : start,
                  'end'     : end
            }
            print observation
            schedule.append(observation)
      return schedule
    except Exception as e:
      print line
      print time.asctime() + ' | ERROR | Failed to fetch schedule for ' + self._telescope +'. Error: ' + str(e)
      return None

if __name__ == '__main__':
  parser = ChandraParser()
  parser.run()
