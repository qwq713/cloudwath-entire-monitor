from datetime import datetime
from datetime import timedelta
from typing import Dict
from typing import List


class CloudWatchData:

    def __init__(self, date: datetime, namespace: str, identifier: str, label: str, data_point: float, unit: str):
        self.date = date
        self.namespace = namespace
        self.identifier = identifier
        self.label = label
        self.data_point = data_point
        self.unit = unit

    def __str__(self) -> str:
        format = "%Y/%m/%d %H:%M:%S"
        str_date = self.date.strftime(format)
        return f"[{str_date}] {self.namespace} {self.identifier} {self.label} {self.data_point} {self.unit}"

    def b_alert(self):

        # data_point 값이 -1 이면 Pass. ( 사용할수 없는 지표 )

        if self.data_point == -1:
            return False

        # 초기 쓰레기값 설정.
        threshold = -1
        alert = False

        # AWS/RDS
        if self.namespace == "AWS/RDS":
            ""
            if self.label == "FreeableMemory":
                # 1024 MB
                threshold = 1024*1024*1024
                if self.data_point < threshold:
                    alert = True

            elif self.label == "CPUUtilization":
                threshold = 75
                if self.data_point > threshold:
                    alert = True

            elif self.label == "BurstBalance":
                threshold = 90
                if self.data_point < threshold:
                    alert = True

            elif self.label == "EBSIOBalance%":
                threshold = 90
                if self.data_point < threshold:
                    alert = True

            elif self.label == "EBSByteBalance%":
                threshold = 90
                if self.data_point < threshold:
                    alert = True

        # AWS/EFS
        elif self.namespace == "AWS/EFS":
            if self.label == "PercentIOLimit":
                threshold = 16 * 1024 * 1024 * 1024
                if self.data_point > threshold:
                    alert =  True

        # AWS/FSX
        # Available storage capacity
        # Total throughput
        elif self.namespace == "AWS/FSx":
            if self.lable == "FreeStorageCapacity":
                # 15 GB
                threshold = 20*1024*1024*1024*1024
                if self.data_point < threshold:
                    alert = True
            
            # Sum(DataReadBytes + DataWriteBytes)
            elif self.label == "TotalThroughput":
                # 16 MB / sec
                threshold = 16 * 1024 * 1024 * 1024
                if self.data_point > threshold:
                    alert =  True

        # AWS/ECS
        elif self.namespace == "AWS/ECS":
            if self.lable == "CPUUtilization":
                threshold = 80
                if self.data_point > threshold:
                    alert = True
            
            elif self.label == "MemoryUtilization":
                threshold = 80
                if self.data_point > threshold:
                    alert =  True

        if threshold == -1:
            raise Exception("namespace , label이 정의된 값이 아닙니다.")

        return alert


def get_metric_statistics(cw_client, namespace: str, metric_name: str, dimensions:List[Dict[str,str]], now_date: datetime,statistic:str="Average") -> CloudWatchData:
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
    data_points = response.get("Datapoints")

    data_point = -1
    unit = "None"

    if data_points:
        data_point = data_points[0].get("Average", -1)
        unit = data_points[0].get("Unit", "None")

    identifier = dimensions[-1]["Value"]
    
    return CloudWatchData(date=now_date, namespace=namespace, identifier=identifier, label=label, data_point=data_point, unit=unit)
