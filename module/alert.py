import subprocess
from module.cloudwatch import CloudWatchData


def clog(log_level:int,cloudwatch_data:CloudWatchData):
    message = f"[{cloudwatch_data.namespace}] {cloudwatch_data.identifier} {cloudwatch_data.data_point} {cloudwatch_data.unit} SMS to CloudAdmin"
    result = subprocess.run(["clog",log_level,message],capture_output=True).stdout.decode("utf-8")
    return result

def clog_str(log_level:int,cloudwatch_data:CloudWatchData):
    message = f"[{cloudwatch_data.namespace}] {cloudwatch_data.identifier} {cloudwatch_data.label} {cloudwatch_data.data_point} {cloudwatch_data.unit} SMS to CloudAdmin"
    print(message)
    return message

