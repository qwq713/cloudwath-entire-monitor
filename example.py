import sys
import boto3
from datetime import datetime,timedelta
from pprint import pprint


"""
RDS CloudWatch Monitor Example.

1. python3 설치
2. 특정 경로로 이동하여 파이썬 가상환경 세팅
   `python3 -m venv ./venv`
3. boto3 패키지 설치
   `./venv/Script/easy_installer.py boto3`
4. `./venv/Script/Activate.ps1`
5. example.py 실행
   `./venv/Script/python.exe ./example.py {ProfileName}`
"""


if __name__ == "__main__":
    '''
    CMD) python3 ./example.py argument[1] argument[2] ...
    위 명시된 command로 파이썬 실행 시. sys.argv 값을 통해 arguments 정보를 불러올 수 있습니다.
    예를들어 `python3 ./example.py MyProfile`와 같이 입력 시 arguments값은 순서대로 아래와 같이 입력됩니다.
    - sys.argv[0] : "./example.py"
    - sys.argv[1] : MyProfile
    '''
    arguments = sys.argv
    profile_name = arguments[1]
    print(profile_name) # MyProfile

    
    '''
    입력한 profile을 기반으로 session정보를 가져옵니다.
    추후 동일한 profile을 기반으로 파이썬 소스코드를 실행해야하므로 한번 읽은 세션정보를 변수로 저장하는것이 중요합니다.
    '''
    session = boto3.Session(profile_name=profile_name)
    
 
    '''
    이제 session 정보를 기반으로 boto3에서 제공하는 패키지를 사용하여 ,
    cloudwatch에서 사용할 rds의 identifier 정보를 가져와 봅시다. 
    (rds identifier는 rds를 구분하는 기준으로 사용됨)
    '''
    
    # boto3에서 제공하는 rds client
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#client
    rds_client = session.client('rds')
    
    
    '''
    cloudwatch client를 사용하기위해 rds client에서 제공하는
    describe_db_instances() function을 사용해서
    rds의 구분자 ( identifier ) 목록 중 한개를 가져와 봅시다.
    '''
    
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Client.describe_db_instances
    rds_response = rds_client.describe_db_instances()
    
    # response 항목 중 "DBInstances" 내에 존재하는 첫번째 RDS 정보를 가져옵니다.
    rds_instances = rds_response.get("DBInstances",[])
    rds = rds_instances[0]
    pprint(rds) # rds 정보를 확인할 수 있습니다.
    
    # 각 rds의 정보 중 cloudwatch에서 구분자로 사용할 "DBInstanceIdentifier" 정보를 가져옵니다.
    rds_identifier = rds["DBInstanceIdentifier"]
    
    
    '''
    이제 cloudwatch로부터 "FreeableMemory" metric 정보를 추출해봅시다.
    이때 위에서 가져온 rds_identifier정보를 이용합니다. 
    '''
    
    # boto3 cloudwatch client
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#client
    cw_client = session.client('rds')
    
    
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.get_metric_statistics
    cw_response = cw_client.get_metric_statistics(
        Namespace="AWS/RDS",
        MetricName="FreeableMemory",
        Dimensions=[{
            "Name":"DBInstanceIdentifier",
            "Value":rds_identifier
            }],
        # UTC Datetime ( CloudWatch에서는 표준 시간으로 UTC를 사용 )
        StartTime=datetime.now() - timedelta(hours=9) - timedelta(minutes=5),
        EndTime=datetime.now() - timedelta(hours=9),
        Period=300,
        Statistics=[
            "Average"
        ]
    )
    
    
    '''
    "-5분 ~ 현재시간" 간 rds의 FreeableMemory 자원값 통계를 알 수 있음.
    '''
    pprint(cw_response)
    

'''
위 로직을 기반으로 RDS, ECS, EFS, FSx 의 CloudWatch Metric 정보를 추출하여
임계치 이상일 경우 알람을 발생하는 소스코드를 구현함.
'''