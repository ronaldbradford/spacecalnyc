import sys
import time
import requests

from base_parser import BaseParser
from datetime import datetime
from datetime import timedelta

class SpitzerParser(BaseParser):
  def __init__(self):
    BaseParser.__init__(self)
    self._telescope = 'Spitzer'

  def fetch_schedule(self):
    try:
      schedule = list()
      filename=sys.argv[1]
      for line in open(filename, "r" ):
        print line
        #TargetName                RA(J2000)    Dec(J2000)    PI                ProgName     pid   AOT         min_dur Start Of Execution (UTC)   AOR_key    AOR_LABEL
        #          1         2         3         4         5         6         7         8         9         0         1         2         3
        #0123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890
        #HD218528                  23:08:49.41  -08:48:28.10  Reach             CAL_IRAC_110  1101 irac          4.24   2003-12-01 14:50:46.6      7890688  IRAC_calstar_HD218528_spt4l2
        start_str = line[111:130].strip() # remove milliseconds
        duration  = line[100:105].strip() # remove milliseconds
        print start_str,duration
        start = datetime.strptime(start_str, self._datetime_format)
        end   = datetime.strptime(start_str, self._datetime_format) + timedelta(0,int(duration))
        target= line[0:25].strip()
        ra    = line[25:36].strip()
        dec   = line[38:50].strip()
        obsid = line[136:144].strip()
        if ra and dec:
          try:
            coords = self._parse_coords(ra, dec)
          except:
            coords = None
          if coords:
            #print coords
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
  parser = SpitzerParser()
  parser.run()
