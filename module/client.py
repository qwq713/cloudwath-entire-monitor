import boto3

def get_client(auth_dict:dict,client_name:str):
    '''
    boto3 client를 반환합니다. 만약 auth_dict 정보에 profile 정보가 없다면 default로 지정된 access_key에 대한 client를 반환합니다.
    
    :param
    - auth_dict : client 에서 사용할 profile명을 "profile" 키값에 사용합니다.
    - client_name : boto3 client에서 사용할 서비스명을 기입합니다.
    ex) profile : MyProfile , client_name : ec2
        ec2_client = get_client(auth_dict={"profile":"MyProfile",client_name="ec2"}) 
    
    :return
    - 지정한 profile, client에 대한 boto3 client 객체를 반환합니다.
    
    '''
    if not auth_dict:
        return boto3.client(client_name)    
    
    elif auth_dict.get("profile",False):
        session = boto3.Session(profile_name=auth_dict.get("profile"))
        
    else:    
        aws_access_key_id = auth_dict.get("aws_access_key_id",False)
        aws_secret_access_key = auth_dict.get("aws_secret_access_key",False)
        region_name = auth_dict.get("region_name",False)
        session = boto3.Session(aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key,region_name=region_name)
    
    return session.client(client_name)


