import sys
import time
import requests

from base_parser import BaseParser
from datetime import datetime
from datetime import timedelta

class HerschelParser(BaseParser):
  def __init__(self):
    BaseParser.__init__(self)
    self._telescope = 'Herschel'
    self._datetime_format = '%Y-%m-%dT%H:%M:%SZ'

  def fetch_schedule(self):
    try:
      schedule = list()
      filename=sys.argv[1]
      for line in open(filename, "r" ):
        info = line.split(",")
        #120,HD_181327,19h22m58.940s,-54d32m17.00s,AOTVAL_bdent_2,PacsPhoto,159,2009-09-11T18:16:52Z,1342183658,HD_181327_continuum,SPG v10.3.0,PASSED
        for i in range(0,len(info)):
          info[i] = info[i].replace('"','')
        #print info
        start = info[7]
        duration = info[6]
        ra = info[2]
        dec = info[3]
        obsid=info[8]
        if ra and dec:
          print ra + "," + dec
          try:
            coords = self._parse_coords(ra, dec)
          except:
            print "Cant get coords"
            coords = None
          if coords:
            #print start + "," + end
            observation = {
                  '_id'     : self._telescope + '|' + obsid,
                  'observation': obsid,
                  'source'  : self._telescope,
                  'target'  : info[2],
                  'ra'      : coords['ra_float'],
                  'dec'     : coords['dec_float'],
                  'ra_str'  : coords['ra_str'],
                  'dec_str' : coords['dec_str'],
                  'l'       : coords['l_float'],
                  'b'       : coords['b_float'],
                  'start'   : datetime.strptime(start, self._datetime_format),
                  'end'     : datetime.strptime(start, self._datetime_format) + timedelta(0,int(duration))
            }
            print observation
            schedule.append(observation)
      return schedule
    except Exception as e:
      print time.asctime() + ' | ERROR | Failed to fetch schedule for ' + self._telescope +'. Error: ' + str(e)
      return None

if __name__ == '__main__':
  parser = HerschelParser()
  parser.run()
