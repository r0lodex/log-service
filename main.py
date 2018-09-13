# -*- coding: utf-8 -*-
"""
@author: Irfan Radzi
@organization: Hermo Creative Sdn Bhd
@created: 04-09-2018
"""

import sys
import datetime as DT
from db import logger, connection, ORIGIN, ORIGIN_TABLE, ARCHIVE, ARCHIVE_TABLE, TIMEDELTA, BATCH
from utilities import archiveLogClick, purgeOrigin, closeConnections
import mysql.connector as database

today = DT.date.today()
batch = BATCH

if len(sys.argv) > 1:
    batch = sys.argv[1]

date_condition = today - DT.timedelta(days=int(TIMEDELTA))
logger.info("Data will be selected from {} onwards ({} days) from table {}.".format(date_condition, TIMEDELTA, ORIGIN_TABLE))

try:
    # Get data
    ORIGIN.execute("select * FROM log_clicks WHERE created >= '{0!s}'".format(date_condition))
    data = ORIGIN.fetchall()

    ORIGIN.execute("desc {}".format(ORIGIN_TABLE))
    origin_columns = ORIGIN.fetchall()

    origin_ids = archiveLogClick(data, ORIGIN,origin_columns, ARCHIVE_TABLE, batch) # For the existing DB

    if len(origin_ids) > 0:
        logger.warning('%s rows successfully added into origin' % len(archive_ids))

    archive_ids = archiveLogClick(data, ARCHIVE, origin_columns, ARCHIVE_TABLE, batch) # For the new DB
    # clear log_clicks after archived, only after successfully archived, hence the archive_ids length
    if len(archive_ids) > 0:
        logger.warning('%s rows successfully archived' % len(archive_ids))
        purgeOrigin(ORIGIN, archive_ids)
    else:
        logger.info('Nothing is done...')

except (database.IntegrityError, database.ProgrammingError) as error:
    logger.warning(error)
    for key, conn in connection.items():
        conn.rollback()
        conn.close()
        logger.info("Rollback {}".format(key))
