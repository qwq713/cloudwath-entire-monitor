# READMD.md

## CW-ENTIRE-MONITOR

- AWS 자원의 CloudWatch Metric 통계를 이용하여 특이사항 발생 시 알람을 발생하는 기능 구현
- 특정 자원을 등록할 필요없이 구현된 모든 메트릭에 대해 모니터링
- 일정주기 ( 5분 ) 단위로 실행하여 임계치에 위배되는 자원유무에 대해 모니터링

### 필요사항

- python3.6
- boto3
- AWS CLI Profile ( AccessKey & SecretKey )
  - (IAM) ReadOnlyAccess 권한 필요.

#### 실행 방법

- `python3 ./main.py {AWSCLI_PROFILE_NAME}`

#### 구현 내역 ( 20220529 )

- RDS
  - FreeableMemory
  - CPUUtilization
  - BurstBalance
  - EBSIOBalance%
  - EBSByteBalance%
- ECS
  - CPUUtilization
  - MemoryUtilization
- EFS
  - PercentIOLimit
- FSx
  - FreeStorageCapacity
