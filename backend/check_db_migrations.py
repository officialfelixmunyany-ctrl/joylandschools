import sqlite3
import sys
import logging

logger = logging.getLogger(__name__)

DB = 'db.sqlite3'
try:
    con = sqlite3.connect(DB)
except Exception as e:
    logger.error('Failed to open database %s', DB, exc_info=e)
    sys.exit(1)

cur = con.cursor()
logger.info('Checking applied migrations for app=users')
try:
    cur.execute("SELECT name, applied FROM django_migrations WHERE app='users'")
    rows = cur.fetchall()
    if not rows:
        # older Django versions may not have 'applied' column; fallback
        cur.execute("SELECT name FROM django_migrations WHERE app='users'")
        rows = [(r[0],) for r in cur.fetchall()]
    for r in rows:
        logger.info('  Migration: %s', r)
except Exception as e:
    logger.error('Could not read django_migrations table', exc_info=e)

logger.info('Checking indexes on users_studentprofile table')
try:
    cur.execute("PRAGMA index_list('users_studentprofile')")
    idxs = cur.fetchall()
    if not idxs:
        logger.info('No indexes found on users_studentprofile')
    else:
        for idx in idxs:
            idx_name = idx[1]
            logger.info('  Found index: %s', idx_name)
            cur.execute(f"PRAGMA index_info('{idx_name}')")
            info = cur.fetchall()
            logger.info('    Columns: %s', info)
except Exception as e:
    logger.error('Error inspecting indexes', exc_info=e)

con.close()
