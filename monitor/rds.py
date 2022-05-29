from module import describe
from module import cloudwatch
from module import alert

def check(cw_client,rds_client,now_date):
    # RDS
    result = []
    rds_namespace = "AWS/RDS"
    rds_metrics = ["FreeableMemory",
                   "CPUUtilization",
                   "BurstBalance",
                   "EBSIOBalance%",
                   "EBSByteBalance%"]

    
    all_rds = describe.all_rds(rds_client=rds_client)
    rds_identifier_list = [ rds["DBInstanceIdentifier"] for rds in all_rds]
    
    for rds_identifier in rds_identifier_list:
        for rds_metric in rds_metrics:
            rds_dimensions = [{
                "Name": "DBInstanceIdentifier",
                "Value": rds_identifier
            }]
            cloudwatch_data = cloudwatch.get_metric_statistics(cw_client=cw_client,
                                            namespace=rds_namespace,
                                            metric_name=rds_metric,
                                            dimensions=rds_dimensions,
                                            now_date=now_date)
            if cloudwatch_data.b_alert():
                alert_result = alert.clog_str(log_level=3, cloudwatch_data=cloudwatch_data)
                # alert_result = alert.clog(log_level=3, cloudwatch_data=cloudwath_data)
                result.append(alert_result)
    return result