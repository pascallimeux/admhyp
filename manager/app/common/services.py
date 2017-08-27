from app.database import get_session, init_db, drop_database
from app.common.log import get_logger
logger = get_logger()


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

    def get_record(self, model, name):
        obj = model.query.filter(model.name == name).first()
        if obj == None:
            raise ObjectNotFoundException("no {0} for name:{1}".format(model, name))
        return obj

    def CreateDB(self):
        try:
            init_db()
            logger.info("Creation of the database")
        except Exception as e:
            logger.error("Database creation failled: {}".format(e))

    def DropDB(self):
        drop_database()