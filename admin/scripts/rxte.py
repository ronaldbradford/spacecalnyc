import sys
import time
import requests

from base_parser import BaseParser
from datetime import datetime


class RXTEParser(BaseParser):
  def __init__(self):
    BaseParser.__init__(self)
    self._telescope = 'RXTE'
    self._datetime_format = '%Y:%j:%H:%M:%S'


  def fetch_schedule(self):
    try:
      schedule = list()
      filename=sys.argv[1]
      for line in open( filename, "r" ):
        info = line.split("\t")
        ra = info[3]
        dec = info[4]
        print ra  + dec
        if ra and dec:
          try:
            coords = self._parse_coords(ra, dec)
          except:
            coords = None
          if coords:
            observation = {
                  '_id'     : self._telescope + '|' + info[5],
                  'observation'     : info[5],
                  'source'  : self._telescope,
                  'target'  : info[2],
                  'ra'      : coords['ra_float'],
                  'dec'     : coords['dec_float'],
                  'ra_str'  : coords['ra_str'],
                  'dec_str' : coords['dec_str'],
                  'l'       : coords['l_float'],
                  'b'       : coords['b_float'],
                  'start'   : datetime.strptime(info[0], self._datetime_format),
                  'end'     : datetime.strptime(info[1], self._datetime_format)
            }
            print observation
            schedule.append(observation)
      return schedule
    except Exception as e:
      print time.asctime() + ' | ERROR | Failed to fetch schedule for ' + self._telescope +'. Error: ' + str(e)
      return None


if __name__ == '__main__':
  parser = RXTEParser()
  parser.run()
