from datetime import datetime, timedelta
import sys
import subprocess
from module import client
from module import describe
from module import alert
from module import cloudwatch


if __name__ == "__main__":
    arguments = sys.argv

    if len(arguments) == 1:
        exit("Please Enter your ProfileName")

    profile_name = arguments[1]

    list_profiles = subprocess.run(
        ["aws", "configure", "list-profiles"], capture_output=True).stdout.decode("utf-8").split("\n")

    for idx, profile in enumerate(list_profiles):
        list_profiles[idx] = profile.replace("\r", "")

    if profile_name not in list_profiles:
        exit("The profile you entered does not exist. Please Check your entered profile again.")

    
    auth_dict = {"profile":profile_name}
    now_date = datetime.now() - timedelta(hours=9) - timedelta(minutes=5)
    cw_client = client.get_client(auth_dict=auth_dict,client_name='cloudwatch')
    
    
    # RDS
    rds_namespace = "AWS/RDS"
    rds_metrics = ["FreeableMemory",
                   "CPUUtilization",
                   "BurstBalance",
                   "EBSIOBalance%",
                   "EBSByteBalance%"]

    
    rds_client = client.get_client(auth_dict=auth_dict,client_name="rds")
    all_rds = describe.all_rds(rds_client=rds_client)
    rds_identifier_list = [ rds["DBInstanceIdentifier"] for rds in all_rds]
    
    for rds_identifier in rds_identifier_list:
        for rds_metric in rds_metrics:
            rds_dimensions = [{
                "Name": "DBInstanceIdentifier",
                "Value": rds_identifier
            }]
            cloudwath_data = cloudwatch.get_metric_statistics(cw_client=cw_client,
                                            namespace=rds_namespace,
                                            metric_name=rds_metric,
                                            dimensions=rds_dimensions,
                                            now_date=now_date)
            if cloudwath_data.b_alert():
                alert.clog_str(log_level=3, cloudwatch_data=cloudwath_data)
        
    
    # EFS
    efs_dimension_name = "FileSystemId"
    efs_namespace = "AWS/EFS"
    efs_metrics = ["PercentIOLimit"]

    # FSX
    efs_dimension_name = "FileSystemId"
    fsx_namespace = "AWS/FSx"
    fsx_metrics = ["FreeStorageCapacity"]

    # ECS
    ecs_namespace = "AWS/ECS"
    ecs_metrics = ["CPUUtilization",
                   "MemoryUtilization"]
    
    
    