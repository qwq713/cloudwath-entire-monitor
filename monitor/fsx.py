from module import describe
from module import cloudwatch
from module import alert


def check(cw_client, fsx_client, now_date):
    # FSx
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
        