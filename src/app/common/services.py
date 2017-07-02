from app.database import get_session, init_db
from common.log import logging
logger = logging.getLogger(__name__)


class MissingParametersException(Exception):
    pass

class ObjectNotFoundException(Exception):
    pass

class Services():

    def SaveRecord(self, obj):
        try:
            get_session().add(obj)
            get_session().commit()
        except Exception as e:
            get_session().rollback()
            logger.error("{0}".format(e))
            raise e

    def CreateDB(self):
        try:
            init_db()
            logger.info("Creation of the database")
        except Exception as e:
            logger.error("Database creation failled: {}".format(e))