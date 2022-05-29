from datetime import datetime, timedelta
import sys
import subprocess
from module import client
from monitor import rds
from monitor import ecs


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

    auth_dict = {"profile": profile_name}
    now_date = datetime.now() - timedelta(hours=9) - timedelta(minutes=5)
    
    cw_client = client.get_client(auth_dict=auth_dict, client_name='cloudwatch')
    rds_client = client.get_client(auth_dict=auth_dict, client_name="rds")
    ecs_client = client.get_client(auth_dict=auth_dict, client_name="ecs")


    # RDS
    rds_result = rds.check(cw_client=cw_client,
                           rds_client=rds_client,
                           now_date=now_date)

    # ECS
    ecs_result = ecs.check(cw_client=cw_client,
                           ecs_client=ecs_client,
                           now_date=now_date)
    
    # EFS
    efs_dimension_name = "FileSystemId"
    efs_namespace = "AWS/EFS"
    efs_metrics = ["PercentIOLimit"]

    # FSX
    efs_dimension_name = "FileSystemId"
    fsx_namespace = "AWS/FSx"
    fsx_metrics = ["FreeStorageCapacity"]
