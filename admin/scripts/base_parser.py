import sys
import time
import pymongo
import requests

import mysql.connector

from datetime import datetime
from BeautifulSoup import BeautifulSoup
from astropysics.coords import ICRSCoordinates, GalacticCoordinates

class BaseParser:
  def __init__(self):
    self._conn = None
    self._telescope = 'BaseTelescope'
    self._data_url = None
    self._datetime_format = '%Y-%m-%d %H:%M:%S'
    self._init_mongo()

  def _init_mongo(self):
    try:
      self._conn = pymongo.MongoClient()
      self._db = self._conn['spacecalnyc']
    except Exception as e:
      print time.asctime() + ' | ERROR | Failed to init database, exiting...'
      self._exit()

  def run(self):
    schedule = self.fetch_schedule()
    if schedule:
      self.save_schedule(schedule)
    self._exit()


  def fetch_schedule(self):
    print time.asctime() + ' | ERROR | fetch_schedule not implemented for ' + \
        self._telescope
    return None


  def save_schedule(self, schedule):
    try:
      cnx = mysql.connector.connect(user='spacecalnyc', password='challenge', database='spacecalnyc')
      cursor = cnx.cursor()
      for observation in schedule:
        add_schedule = ("INSERT INTO schedule (_id, source, target, start, end, ra, `dec`, ra_str, dec_str, l, b, observation, created) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW()) "
                        "ON DUPLICATE KEY UPDATE target = %s, start = %s, end = %s, ra = %s, `dec` = %s, ra_str = %s, dec_str = %s, l = %s, b = %s")
        data_schedule = (observation['_id'], observation['source'], observation['target'], observation['start'], observation['end'], observation['ra'], observation['dec'], observation['ra_str'], observation['dec_str'], observation['l'], observation['b'], observation['observation'],
        observation['target'], observation['start'], observation['end'], observation['ra'], observation['dec'], observation['ra_str'], observation['dec_str'], observation['l'], observation['b'])
        cursor.execute(add_schedule, data_schedule)

      print time.asctime() + ' | INFO | Sucessfully saved schedule for ' + self._telescope
      cursor.close()
      cnx.commit()
    except Exception as e:
      print time.asctime() + ' | ERROR | Failed to save schedule for ' + self._telescope + ' ' + str(e)


  ## this takes two strings in, one for the right ascension, and one for the declination
  ## this can be passed in with a range of formats. If it fails then it throws a
  def _parse_coords(self, ra_str, dec_str):
    eq_coords = ICRSCoordinates(ra_str,dec_str)
    gal_coords = eq_coords.convert(GalacticCoordinates)
    return {
        'ra_float'  : eq_coords.ra.degrees,
        'dec_float' : eq_coords.dec.degrees,
        'l_float'   : gal_coords.l.degrees,
        'b_float'   : gal_coords.b.degrees,
        'ra_str'    : eq_coords.ra.getHmsStr(),
        'dec_str'   : eq_coords.dec.getDmsStr(sep=('d', 'm', 's'))
     }

  def _exit(self):
    if self._conn:
      self._conn.close()
    sys.exit(0)
