from config import SONAR_HOST, METRIC_KEYS
from util.sonar import QueryInfo

data = QueryInfo(_host=SONAR_HOST, _keys=METRIC_KEYS)

# data.get_project_bugs()
data.get_project_metrics()
