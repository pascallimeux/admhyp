from app.database import db_session, init_db
from common.log import LOG_LEVEL, log_handler
import logging
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(log_handler)


class MissingParametersException(Exception):
    pass

class Services():

    def SaveRecord(self, obj):
        try:
            db_session.add(obj)
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            logger.error("{0}".format(e))
            raise e

    def CreateDB(self):
        try:
            init_db()
            logger.info("Creation of the database")
        except Exception as e:
            logger.error("Database creation failled: {}".format(e))