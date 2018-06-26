from sqlalchemy import Column, Integer, String, DateTime, text, ForeignKey, Float, Enum
from sqlalchemy.ext.declarative import declarative_base

from config import BUG_SEVERITIES, BUG_TYPES

BaseModel = declarative_base()


class ProjectMap(BaseModel):
    __tablename__ = 'project_map'
    id = Column(Integer, primary_key=True)
    project_code = Column(String(50), nullable=False, unique=True, comment='项目主键,必须唯一')
    project_name = Column(String(50), nullable=False, comment='项目名称')
    create_time = Column(DateTime, server_default=text('NOW()'), comment='创建时间')
    update_time = Column(DateTime, onupdate=text('NOW()'), comment='修改时间，自动更新')

    def __repr__(self):
        return "<ProjectMap(project_code='%s', project_name='%s', create_time='%s', update_time='%s')>" % (
            self.project_code, self.project_name, self.create_time, self.update_time)


class ProjectMetrics(BaseModel):
    __tablename__ = 'project_metrics'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('project_map.id'), nullable=False, comment='项目id')
    project_version = Column(String(20))
    unit_test_total = Column(Integer, server_default=0, comment='单元测试总量')
    unit_test_errors = Column(Integer, server_default=0, comment='单元测试错误数')
    unit_test_failures = Column(Integer, server_default=0, comment='单元测试失败数')
    unit_skipped_tests = Column(Integer, server_default=0, comment='单元测试跳过数')
    unit_test_coverage = Column(Float(precision=2), server_default=0.00, comment='单元测试覆盖率%')
    bug_total = Column(Integer, server_default=0, comment='BUG总数')
    comment_lines_density = Column(Float(precision=2), server_default=0.00, comment='代码注释比率%')
    create_time = Column(DateTime, server_default=text('NOW()'), comment='创建时间')
    update_time = Column(DateTime, onupdate=text('NOW()'), comment='修改时间，自动更新')


class ProjectBugs(BaseModel):
    __tablename__ = 'project_bugs'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('project_map.id'), nullable=False, comment='项目id')
    project_version = Column(String(20))
    bug_severities = Column(Enum(*BUG_SEVERITIES), comment='BUG验证程度')
    bug_types = Column(Enum(*BUG_TYPES), comment='BUG类型')
    amounts = Column(Integer, server_default=0, comment='BUG数量')
    create_time = Column(DateTime, server_default=text('NOW()'), comment='创建时间')
    update_time = Column(DateTime, onupdate=text('NOW()'), comment='修改时间，自动更新')
