import random

MASTER_DB = 'master_db'
SLAVE_DB = 'slave_db'


class TetVietRouter:
    def db_for_read(self, model, **hints):
        return random.choice([MASTER_DB, SLAVE_DB])

    def db_for_write(self, model, **hints):
        return MASTER_DB

    def allow_relation(self, obj1, obj2, **hints):
        db_list = (MASTER_DB, SLAVE_DB)
        if obj1._state.db in db_list and obj2._state.db in db_list:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True
