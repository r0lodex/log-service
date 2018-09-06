# -*- coding: utf-8 -*-
"""
@author: Irfan Radzi
@organization: Hermo Creative Sdn Bhd
@created: 04-09-2018
"""

import ConfigParser
import coloredlogs, logging
import datetime
import mysql.connector as database

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)

config = ConfigParser.ConfigParser()

try:
    config.readfp(open('config-production.ini'))
    logging.basicConfig(filename='LogService.log', filemode='w', level=logging.DEBUG)
except IOError:
    config.read('config.ini')

for c in config.sections():
    logger.warning('Database: {0}'.format(config.get(c, 'DATABASE')))

connection = {
    'ORIGIN': database.connect(user=config.get('ORIGIN', 'USER'),
                     password=config.get('ORIGIN', 'PASSWORD'),
                     database=config.get('ORIGIN', 'DATABASE'),
                     port=config.get('ORIGIN', 'PORT'),
                     host=config.get('ORIGIN', 'HOST')
                     ),
    'ARCHIVE': database.connect(user=config.get('ARCHIVE', 'USER'),
                     password=config.get('ARCHIVE', 'PASSWORD'),
                     database=config.get('ARCHIVE', 'DATABASE'),
                     port=config.get('ARCHIVE', 'PORT'),
                     host=config.get('ARCHIVE', 'HOST')
                     )
}

ORIGIN = connection['ORIGIN'].cursor(buffered=True)
ARCHIVE = connection['ARCHIVE'].cursor(buffered=True)
ORIGIN_TABLE = config.get('ORIGIN', 'TABLE')
ARCHIVE_TABLE = config.get('ARCHIVE', 'TABLE')
TIMEDELTA = config.get('STATE', 'SYNC_DELTA_DAYS')