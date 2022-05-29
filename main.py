import sys
import subprocess
from datetime import datetime, timedelta
from module import client
from monitor import rds
from monitor import ecs
from monitor import efs
from monitor import fsx


if __name__ == "__main__":
    arguments = sys.argv

    if len(arguments) == 1:
        exit("Please Enter your ProfileName")

    profile_name = arguments[1]

    '''
    입력한 profile의 등록여부를 확인하고 미등록일 경우 종료합니다.
    '''
    list_profiles = subprocess.run(
        ["aws", "configure", "list-profiles"], capture_output=True).stdout.decode("utf-8").split("\n")

    for idx, profile in enumerate(list_profiles):
        list_profiles[idx] = profile.replace("\r", "")

    if profile_name not in list_profiles:
        exit("The profile you entered does not exist. Please Check your entered profile again.")


    '''
    입력한 profile 정보를 기반으로 boto3 client 객체를 생성합니다.
    '''
    
    auth_dict = {"profile": profile_name}
    
    cw_client = client.get_client(auth_dict=auth_dict, client_name='cloudwatch')
    rds_client = client.get_client(auth_dict=auth_dict, client_name="rds")
    ecs_client = client.get_client(auth_dict=auth_dict, client_name="ecs")
    efs_client = client.get_client(auth_dict=auth_dict, client_name="efs")
    fsx_client = client.get_client(auth_dict=auth_dict, client_name="fsx")

    
    '''
    cloudwatch에서 사용하는 기준시간인 UTC(KST - 9:00) 시간을 사용합니다.
    따라서 UTC 기준 현재시간 -5분 ~ 현재시간까지를 모니터링합니다.
    '''
    now_date = datetime.now() - timedelta(hours=9) - timedelta(minutes=5)


    # 모니터링 결과 메세지 리스트.
    result_messages = []
    
    '''
    RDS CloudWatch 지표에 대한 모니터링 결과값을 반환합니다.
    - monitor/rds.py 의 check function을 사용합니다.
    '''
    rds_result = rds.check(cw_client=cw_client,
                           rds_client=rds_client,
                           now_date=now_date)
    result_messages.extend(rds_result)
    
    
    '''
    ECS CloudWatch 지표에 대한 모니터링 결과값을 반환합니다.
    - monitor/ecs.py 의 check function을 사용합니다.
    '''
    ecs_result = ecs.check(cw_client=cw_client,
                           ecs_client=ecs_client,
                           now_date=now_date)
    result_messages.extend(ecs_result)
    
    
    '''
    EFS CloudWatch 지표에 대한 모니터링 결과값을 반환합니다.
    - monitor/efs.py 의 check function을 사용합니다.
    '''
    efs_result = efs.check(cw_client=cw_client,
                           efs_client=efs_client,
                           now_date=now_date)
    result_messages.extend(efs_result)
    
    
    '''
    FSX CloudWatch 지표에 대한 모니터링 결과값을 반환합니다.
    - monitor/fsx.py 의 check function을 사용합니다.
    '''
    fsx_result = fsx.check(cw_client=cw_client,
                           fsx_client=fsx_client,
                           now_date=now_date)
    result_messages.extend(fsx_result)

    
    