from module import describe
from module import cloudwatch
from module import alert
from typing import List

# EFS
def check(cw_client, efs_client, now_date) -> List[str]:
    '''
    :param
    - cw_client : boto3 cloudwatch client
    - {name}_client : boto3 {name} client
    - now_date : datetime 모듈로 구한 현재 시간
    
    :return
    - 모니터링 결과에 대한 메세지목록을 (List[str]) 반환합니다.
    '''   
    result = []
    efs_namespace = "AWS/EFS"
    efs_metrics = ["PercentIOLimit"]
    
    all_efs = describe.all_efs(efs_client=efs_client)
    
    
    for efs in all_efs:
        file_system_id = efs["FileSystemId"]
        efs_dimensions = [{"Name":"FileSystemId",
                           "Value":file_system_id}]
        for efs_metric in efs_metrics: 
            cloudwatch_data = cloudwatch.get_metric_statistics(cw_client=cw_client,
                                                namespace=efs_namespace,
                                                metric_name=efs_metric,
                                                dimensions=efs_dimensions,
                                                now_date=now_date)
            if cloudwatch_data.b_alert():
                alert_result = alert.clog_str(log_level=3, cloudwatch_data=cloudwatch_data)
                # alert_result = alert.clog(log_level=3, cloudwatch_data=cloudwath_data)
                result.append(alert_result)
    return result
        