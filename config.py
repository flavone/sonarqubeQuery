import os

SONAR_HOST = 'http://192.168.5.46:9010/api'

PROJECT_SEARCH_ROUTE = '/projects/search'

MEASURE_ROUTE = '/measures/component'

BUG_ROUTE = '/issues/search'

USER_NAME = 'admin'

PASS_WORD = 'admin'

METRIC_KEYS = [['tests', '单元测试总数'],
               ['test_errors', '单元测试错误数'],
               ['test_failures', '单元测试失败数'],
               ['skipped_tests', '单元测试跳过数'],
               ['coverage', '单元测试覆盖率%'],
               ['bugs', 'BUG总数'],
               ['comment_lines_density', '代码注释比例%']
               ]  # 注意：修改该项时，需要同步修改datamodel中的ProjectMetrics的数据模型

BUG_SEVERITIES = ('MAJOR', 'CRITICAL', 'BLOCKER')
BUG_TYPES = ('CODE_SMELL', 'VULNERABILITY', 'BUG')

DINGDING_ACCESS_TOKEN = 'df32eef6bff0fa38a91ed33afb207b80d5800b2dadb90acaac2f7c77fc5946bb'

SQLALCHEMY_DATABASE_URI = ''  # TODO 添加SQL连接字符串

SQLALCHEMY_MIGRATE_REPO = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'db_repository')
