import imp
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from migrate.versioning import api

from config import SQLALCHEMY_MIGRATE_REPO, SQLALCHEMY_DATABASE_URI
from model.datamodel import BaseModel


class DbSession:
    session = None
    engine = None
    model = None

    def __init__(self):
        self.engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
        _session = sessionmaker(bind=self.engine, autocommit=False, autoflush=False)
        self.session = _session()
        self.model = BaseModel

    def create_tables(self):
        """
        仅执行一次，用于初始化数据库，对于已经建立的表不会重建\n
        :return:
        """
        self.model.metadata.create_all(self.engine)
        if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
            # self.model.metadata.create_all(self.engine)
            api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
            api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
        else:
            print('已经建立了数据库')
            api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO,
                                version=api.version(SQLALCHEMY_MIGRATE_REPO))

    def migrate_tables(self):
        """
        用于迁移数据库，每次对表字段或表类型进行修改时，执行该方法\n
        :return:当前迁移版本\n
        """
        migration = SQLALCHEMY_MIGRATE_REPO + '/versions/%03d_migration.py' % (
            api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO) + 1)
        tmp_model = imp.new_module('old_model')
        old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
        exec(old_model, tmp_model.__dict__)
        script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, tmp_model.meta,
                                                  self.model.metadata)
        open(migration, 'wt').write(script)
        api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
        print('New migration saved as ' + migration)
        return str(api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO))

    def drop_tables(self):
        """
        不要轻易使用该方法，会清空数据库\n
        :return:
        """
        self.model.metadata.drop_all(self.engine)

    def add_data(self, data):
        """
        添加数据到库\n
        :param data: 在 :class:`datamodel` 中已定义的数据对象，可以是tuple元组\n
        :return:
        """
        if isinstance(data, list):
            self.session.add_all(data)
        else:
            self.session.add(data)
        self.session.commit()

    def query_data(self, query_string):
        """
        通过SQL语句查询数据\n
        :param query_string:SQL执行语句\n
        :return:全部查询结果,多行时为tuple元组
        """
        s = text(query_string)
        return self.session.execute(s).fetchall()

    def get_session(self):
        """
        获取当前session，用于自定义执行SQL\n
        :return: 当前session
        """
        return self.session

    def close_session(self):
        """
        关闭当前session的全部连接,在不再使用session时关闭。\n
        :return:
        """
        self.session.close_all()
