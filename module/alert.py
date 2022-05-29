import subprocess
from module.cloudwatch import CloudWatchData

log_map = {1:"info",
           2:"minor",
           3:"major",
           4:"critical",
           5:"down"}

def clog(log_level:int,cloudwatch_data:CloudWatchData):
    '''
    clog 를 발생시킵니다.
    :param
    - log_level : 1(info) 2(minor) 3(major) 4(critical) 5(down)
    :return
    - message 결과
    '''
    message = f"[{log_map[log_level]}][{cloudwatch_data.namespace}] {cloudwatch_data.identifier} {cloudwatch_data.data_point} {cloudwatch_data.unit} SMS to CloudAdmin"
    result = subprocess.run(["clog",log_level,message],capture_output=True).stdout.decode("utf-8")
    print(result)
    return message

def clog_str(log_level:int,cloudwatch_data:CloudWatchData):
    '''
    clog 를 문자열 형태로만 발생시킵니다.
    :param
    - log_level : 1(info) 2(minor) 3(major) 4(critical) 5(down)
    :return
    - message 결과
    '''
    message = f"[{log_map[log_level]}][{cloudwatch_data.namespace}] {cloudwatch_data.identifier} {cloudwatch_data.label} {cloudwatch_data.data_point} {cloudwatch_data.unit} SMS to CloudAdmin"
    print(message)
    return message

