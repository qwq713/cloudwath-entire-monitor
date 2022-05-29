from module import describe
from module import cloudwatch
from module import alert
from typing import List

# ECS
def check(cw_client, ecs_client, now_date) -> List[str]:
    '''
    :param
    - cw_client : boto3 cloudwatch client
    - {name}_client : boto3 {name} client
    - now_date : datetime 모듈로 구한 현재 시간
    
    :return
    - 모니터링 결과에 대한 메세지목록을 (List[str]) 반환합니다.
    ''' 
    result = []

    # ECS
    ecs_namespace = "AWS/ECS"
    ecs_metrics = ["CPUUtilization",
                   "MemoryUtilization"]

    all_ecs_service_arns = describe.all_ecs_service_arns(ecs_client=ecs_client)

    for ecs_serivice_arn in all_ecs_service_arns:
        _, cluster_name, service_name = ecs_serivice_arn.split("/")
        ecs_dimensions = [
            {
                "Name": "ClusterName",
                "Value": cluster_name
            },
            {
                "Name": "ServiceName",
                "Value": service_name
            }
        ]
        for ecs_metric in ecs_metrics:
            cloudwatch_data = cloudwatch.get_metric_statistics(cw_client=cw_client,
                                                               namespace=ecs_namespace,
                                                               metric_name=ecs_metric,
                                                               dimensions=ecs_dimensions,
                                                               now_date=now_date)
            if cloudwatch_data.b_alert():
                alert_result = alert.clog_str(3,cloudwatch_data=cloudwatch_data)
                # alert_result = alert.clog(3,cloudwatch_data=cloudwatch_data)
                result.append(alert_result)
    return result
