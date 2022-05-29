from datetime import datetime
from datetime import timedelta
from typing import Dict
from typing import List


class CloudWatchData:
    """
    CloudWatch API의 결과를 저장하는 Class.
    """

    def __init__(self, date: datetime, namespace: str, identifier: str, label: str, data_point: float, unit: str):
        self.date = date #: dattime 날짜정보
        self.namespace = namespace #: namespace 정보 . ex: AWS/RDS , AWS/FSX ...
        self.identifier = identifier #: identifier(구분자 정보) . ex: filesystem_id ...
        self.label = label #: Metric Label 정보 . ex : MemoryUtilization, CPUUtilization ...
        self.data_point = data_point #: CloudWatch 메트릭으로 수집된 값.
        self.unit = unit #: CloudWatch 메트릭으로 수집된 값의 단위

    def __str__(self) -> str:
        format = "%Y/%m/%d %H:%M:%S"
        str_date = self.date.strftime(format)
        return f"[{str_date}] {self.namespace} {self.identifier} {self.label} {self.data_point} {self.unit}"

    def b_alert(self) -> bool:
        '''
        CloudWatchData 객체의 namespace,label 정보에 따른 Metric지표가 
        설정된 임계치(threshold)보다 높을 경우 True값을 반환합니다.
        
        :return
        - bool ( True or False ) 설정된 임계치(threshold)보다 높은 경우 True, 이외 False
        '''
        
        # data_point 값이 -1 이면 Pass. ( 사용할수 없는 지표 )
        if self.data_point == -1:
            return False

        # 초기 쓰레기값 설정.
        threshold = -1
        alert = False

        # namespace : AWS/RDS
        if self.namespace == "AWS/RDS":
            # Lable : FreeableMemory , CPUUtilization, BurstBalance, EBSIOBalance%, EBSByteBalance%
            if self.label == "FreeableMemory":
                # 1 GB
                threshold = 1 * 1024 * 1024 * 1024
                if self.data_point < threshold:
                    alert = True

            elif self.label == "CPUUtilization":
                threshold = 75
                if self.data_point > threshold:
                    alert = True

            elif self.label == "BurstBalance":
                threshold = 85
                if self.data_point < threshold:
                    alert = True

            elif self.label == "EBSIOBalance%":
                threshold = 85
                if self.data_point < threshold:
                    alert = True

            elif self.label == "EBSByteBalance%":
                threshold = 90
                if self.data_point < threshold:
                    alert = True

        # namespace : AWS/EFS
        elif self.namespace == "AWS/EFS":
            # Lable : PercentIOLimit
            if self.label == "PercentIOLimit":
                threshold = 70
                if self.data_point > threshold:
                    alert =  True

        # namespace : AWS/FSx
        elif self.namespace == "AWS/FSx":
            # Lable : FreeStorageCapacity
            if self.label == "FreeStorageCapacity":
                # 15 GB
                threshold = 15 * 1024*1024*1024
                if self.data_point < threshold:
                    alert = True
            
            # Sum(DataReadBytes + DataWriteBytes)
            elif self.label == "TotalThroughput":
                # 16 MB / sec
                threshold = 16 * 1024 * 1024
                if self.data_point > threshold:
                    alert =  True

        # namespace : AWS/ECS
        elif self.namespace == "AWS/ECS":
            # Lable : CPUUtilization, MemoryUtilization
            if self.label == "CPUUtilization":
                threshold = 80
                if self.data_point > threshold:
                    alert = True
            
            elif self.label == "MemoryUtilization":
                threshold = 80
                if self.data_point > threshold:
                    alert =  True

        # 미구현 Label인 경우 Exception 발생
        if threshold == -1:
            raise Exception("namespace , label이 정의된 값이 아닙니다.")

        return alert


def get_metric_statistics(cw_client, namespace: str, metric_name: str, dimensions:List[Dict[str,str]], now_date: datetime,statistic:str="Average") -> CloudWatchData:
    '''
    boto3 cloudwatch client에서 제공하는 get_metric_statistics 함수를 일정하게 사용할 수 있도록 커스텀한 함수.
    
     :param
    - cw_client : boto3 cloudwatch client
    - namespace: str
    - metric_name: str
    - dimensions:List[Dict[str,str]]
    - now_date: datetime
    - statistic:str="Average" 
    
    :return
    - CloudWatchData : get_metric_statistics 결과값을 CloudWatchData 클래스의 객체로 변환
    
    '''
    response = cw_client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=dimensions,
        StartTime=now_date,
        EndTime=now_date+timedelta(minutes=5),
        Period=300,
        Statistics=[
            statistic,
        ]
    )
    label = response.get("Label")
    data_points = response.get("Datapoints",[])

    data_point = -1
    unit = "None"

    if data_points:
        data_point = data_points[0].get("Average", -1)
        unit = data_points[0].get("Unit", "None")

    identifier = dimensions[-1]["Value"]
    
    return CloudWatchData(date=now_date, namespace=namespace, identifier=identifier, label=label, data_point=data_point, unit=unit)
