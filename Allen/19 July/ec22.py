import boto.ec2.cloudwatch
boto.ec2.EC2Connection(AWS_Access_Key, AWS_Secret)
cw = boto.ec2.cloudwatch.connect_to_region('us-west-2c')
print cw.get_metric_statistics(
        300,
        datetime.datetime.utcnow() - datetime.timedelta(seconds=600),
        datetime.datetime.utcnow(),
        'CPUUtilization',
        'AWS/EC2',
        'Average',
        dimensions={'InstanceId':['i-11111111']}
   )
