import sys
import subprocess
from module import client
from module import describe 


if __name__ == "__main__":
    arguments = sys.argv
    
    if len(arguments) == 1 :
        exit("Please Enter your ProfileName")

    profile_name = arguments[1]
    
    list_profiles = subprocess.run(["aws","configure","list-profiles"],capture_output=True).stdout.decode("utf-8").split("\n")
    
    for idx,profile in enumerate(list_profiles):
        list_profiles[idx] = profile.replace("\r","")
    
    if profile_name not in list_profiles:
        exit("The profile you entered does not exist. Please Check your entered profile again.")
        
    
    # RDS
    rds_dimension_name = "DBInstanceIdentifier"
    rds_namespace = "AWS/RDS"
    rds_metrics = ["FreeableMemory",
                   "CPUUtilization",
                   "BurstBalance",
                   "EBSIOBalance%",
                   "EBSByteBalance%"]
    
    # EFS
    efs_dimension_name = "FileSystemId"
    efs_namespace ="AWS/EFS"
    efs_metrics = ["PercentIOLimit"]
    
    # FSX
    efs_dimension_name = "FileSystemId"
    fsx_namespace = "AWS/FSx"
    fsx_metrics = ["FreeStorageCapacity"]
    
    # ECS
    ecs_namespace = "AWS/ECS"
    ecs_metrics = ["CPUUtilization",
                   "MemoryUtilization"]
    
    # append file.
    
    # execute clog
    
    
    