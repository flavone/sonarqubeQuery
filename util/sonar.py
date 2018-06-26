from config import PROJECT_SEARCH_ROUTE, MEASURE_ROUTE, METRIC_KEYS, USER_NAME, PASS_WORD, BUG_ROUTE, \
    BUG_SEVERITIES, BUG_TYPES, DINGDING_ACCESS_TOKEN
from projectmap import PROJECT_MAP
from util.uhttp import HttpUtil


def __get_project_cn_name__(project_code):
    project_name = project_code
    for project_map in PROJECT_MAP:
        if project_map[0] == project_code:
            project_name = project_map[1]
            break
    return project_name


class QueryInfo:
    metric_keys = None
    host = None
    session = None

    def __init__(self, _host, _keys=None):
        self.host = _host
        self.metric_keys = _keys
        self.session = HttpUtil(_host + '/authentication/login', username=USER_NAME, password=PASS_WORD)

    def __conglue__(self):
        metric_keys_str = ''
        if len(self.metric_keys) <= 0:
            return None
        for key in self.metric_keys:
            metric_keys_str += key[0] + ','
        return metric_keys_str

    def __get_project_list__(self):  # TODO 项目信息入库
        url = self.host + PROJECT_SEARCH_ROUTE
        json = self.session.get_json(url)
        if json is None:
            return None
        components = json.get('components')
        project_list = []
        if len(components) <= 0:
            return None
        for component in components:
            project_list.append(component.get('key'))
        return project_list

    def get_project_metrics(self):  # TODO 项目独立结果入库
        key = self.__conglue__()
        url = self.host + MEASURE_ROUTE
        metrics = []
        project_list = self.__get_project_list__()
        if project_list is None or len(project_list) <= 0:
            return metrics
        for index in range(len(project_list)):
            project_code = project_list[index]
            para = {'component': project_code,
                    'metricKeys': key}
            json = self.session.get_json(url, para=para)
            result = json.get('component').get('measures')
            project_name = __get_project_cn_name__(project_code)
            tmp = '%s:\n ' % project_name
            if result is None:
                tmp += '\t没有sonar的结果！\n'
            for i in range(len(METRIC_KEYS)):
                metrics_key = METRIC_KEYS[i]
                for j in range(len(result)):
                    if result[j]['metric'] == metrics_key[0]:
                        tmp += '\t%s = %s\n' % (metrics_key[1], result[j]['value'])
                        break
            # print(tmp)
            metrics.append(tmp)
        from util.dingdingpush import send_message
        send_message(DINGDING_ACCESS_TOKEN, metrics)
        return metrics

    def get_project_bugs(self):  # TODO 项目BUG入库
        url = self.host + BUG_ROUTE
        bug_list = []
        project_list = self.__get_project_list__()
        if project_list is None or len(project_list) <= 0:
            return bug_list
        for index in range(len(project_list)):
            project_code = project_list[index]
            project_name = __get_project_cn_name__(project_code)
            tmp = project_name + ':\n '
            for bug_type in BUG_TYPES:
                tmp += '\t%s:\n' % bug_type
                for bug_severity in BUG_SEVERITIES:
                    para = {'componentKeys': project_code,
                            's': 'FILE_LINE',
                            'p': '1',
                            'ps': '1',
                            'resolved': 'false',
                            'severities': bug_severity,
                            'types': bug_type
                            }
                    json = self.session.get_json(url, para=para)
                    result = json.get('total')
                    if result is None:
                        result = 0
                    tmp += '\t\t%s: %s\n' % (bug_severity, str(result))
            # print(tmp)
            bug_list.append(tmp)
        from util.dingdingpush import send_message
        send_message(DINGDING_ACCESS_TOKEN, bug_list)
        return bug_list
