from module import describe
from module import cloudwatch
from module import alert
from typing import List

# FSx
def check(cw_client, fsx_client, now_date) -> List[str]:
    '''
    :param
    - cw_client : boto3 cloudwatch client
    - {name}_client : boto3 {name} client
    - now_date : datetime 모듈로 구한 현재 시간
    
    :return
    - 모니터링 결과에 대한 메세지목록을 (List[str]) 반환합니다.
    ''' 
    result = []
    fsx_namespace = "AWS/FSx"
    fsx_metrics = ["FreeStorageCapacity"]
    
    all_fsx = describe.all_fsx(fsx_client=fsx_client)
    
    
    for fsx in all_fsx:
        file_system_id = fsx["FileSystemId"]
        fsx_dimensions = [{"Name":"FileSystemId",
                           "Value":file_system_id}]
        for fsx_metric in fsx_metrics: 
            cloudwatch_data = cloudwatch.get_metric_statistics(cw_client=cw_client,
                                                namespace=fsx_namespace,
                                                metric_name=fsx_metric,
                                                dimensions=fsx_dimensions,
                                                now_date=now_date)
            if cloudwatch_data.b_alert():
                alert_result = alert.clog_str(log_level=3, cloudwatch_data=cloudwatch_data)
                # alert_result = alert.clog(log_level=3, cloudwatch_data=cloudwath_data)
                result.append(alert_result)
    return result
        