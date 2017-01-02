import boto3
import logging
import datetime

#setup simple logging for INFO
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#define the connection
ec2 = boto3.client('ec2')
ec2inst = boto3.resource('ec2')

def lambda_handler(event, context):
    
    # Use the filter() method of the instances collection to retrieve
    # all running EC2 instances.
    filters = [
        {
            'Name': 'instance-state-name', 
            'Values': ['running']
        },
        {
            'Name': 'tag:development',
            'Values': ['True']
        }
    ]
    
    #filter the instances
    answer = ec2.describe_instances(Filters=filters)
    
    if len(answer) > 0:
        
        for reservation in answer['Reservations']:
            for instance in reservation['Instances']:
                launch_time = instance['LaunchTime']
                inst = instance['InstanceId']
                now = datetime.datetime.now(launch_time.tzinfo)
                delta = now - launch_time
                #print(delta)
                if delta > datetime.timedelta(hours=24):
                    print('old instances found and terminated')
                    ShutDown = ec2inst.instances.filter(InstanceIds=[inst]).stop()
                    print (ShutDown)
                else:
                    print('no old instances found')
    else:
        print('No instances running')
