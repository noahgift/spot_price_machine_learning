[![CircleCI CircleCI Build Status](https://circleci.com/gh/noahgift/spot_price_machine_learning/tree/master.svg?style=svg)](https://circleci.com/gh/noahgift/spot_price_machine_learning/tree/master)

# AWS Spot Price Machine Learning Tools

Machine Learning for Spot Prices Command-Line Tool and Jupyter Notebook.  This material is covered in [Chapter 9 of Pragmatic AI](https://amzn.to/2LFLVEg)

## Pragmatic AI Labs
![alt text](https://paiml.com/images/logo_with_slogan_white_background.png)

You can continue learning about these topics by:

*   Buying a copy of [Pragmatic AI: An Introduction to Cloud-Based Machine Learning](https://amzn.to/2LFLVEg)
*   Viewing more content at [noahgift.com](https://noahgift.com/)


## Contains two command-line tools

* [Spot Price ML](https://github.com/noahgift/spot_price_machine_learning/blob/master/spot-price-ml.py)
* [Spot Price Launcher](https://github.com/noahgift/spot_price_machine_learning/blob/master/spot_launcher.py)


## TO DO

* Linear Optimization using Pyomo
* Documentation

## Assumptions, AWS account and/or profile with credentials.

[happygolucky]

aws_access_key_id = <foo>

aws_secret_access_key = <bar>

## Running lint and tests

To make sure it works, do something like below:

```make setup && make install```

```source <your virtualenv>``` (not required)

```make lint```

```make test``` Runs Jupyter notebook test of project

## Problems Solved:  Recommended Spot Instances and Finding Deals


### Describe Spot Instances by Median Price History and Price per ECU

```
(.pragia-aws) ➜  pragai-aws git:(master) ✗ ./spot-price-ml.py describe
              SpotPrice  price_ecu_spot  cluster  price_memory_spot
InstanceType                                                       
r4.xlarge         0.033           0.002        0              0.001
r4.large          0.017           0.002        0              0.001
r4.2xlarge        0.061           0.002        0              0.001
c3.2xlarge        0.098           0.003        1              0.007
r4.4xlarge        0.158           0.003        0              0.001
r3.xlarge         0.044           0.003        0              0.001
m4.4xlarge        0.185           0.003        0              0.003
m3.xlarge         0.043           0.003        0              0.003
m3.medium         0.009           0.003        0              0.002
c3.4xlarge        0.175           0.003        1              0.006
c3.8xlarge        0.368           0.003        1              0.006
cc2.8xlarge       0.344           0.004        1              0.006
r4.8xlarge        0.385           0.004        0              0.002
c3.large          0.027           0.004        1              0.007
c3.xlarge         0.053           0.004        1              0.007
r4.16xlarge       0.805           0.004        0              0.002
c4.2xlarge        0.125           0.004        1              0.008
c4.xlarge         0.057           0.004        1              0.008
m4.16xlarge       0.712           0.004        0              0.003
m4.10xlarge       0.440           0.004        0              0.003
c4.4xlarge        0.265           0.004        1              0.009
m3.2xlarge        0.094           0.004        0              0.003
c4.8xlarge        0.558           0.004        1              0.009
m4.2xlarge        0.133           0.005        0              0.004
m4.xlarge         0.062           0.005        0              0.004
g3.4xlarge        0.247           0.005        0              0.002
r3.4xlarge        0.237           0.005        0              0.002
r3.8xlarge        0.668           0.006        0              0.003
d2.4xlarge        0.319           0.006        0              0.003
x1.32xlarge       1.998           0.006        2              0.001
r3.2xlarge        0.195           0.007        0              0.003
i2.4xlarge        0.416           0.008        0              0.003
g3.8xlarge        0.762           0.008        0              0.003
i2.8xlarge        0.848           0.008        0              0.003
x1.16xlarge       1.394           0.008        2              0.001
d2.8xlarge        1.018           0.009        2              0.004
i2.2xlarge        0.335           0.012        1              0.005
g3.16xlarge       2.409           0.013        2              0.005
p2.8xlarge        1.800           0.019        2              0.004
p2.xlarge         0.267           0.022        2              0.004
```


### Get Machine Learning Based Recommendations on Substitutes for Your Favorite Spot Instance

```
(.pragia-aws) ➜  pragai-aws git:(master) ✗ ./spot-price-ml.py recommend --instance c3.8xlarge 
              SpotPrice  price_ecu_spot  cluster  price_memory_spot
InstanceType                                                       
c3.2xlarge        0.098           0.003        0              0.007
c3.4xlarge        0.176           0.003        0              0.006
c3.8xlarge        0.370           0.003        0              0.006
c4.4xlarge        0.265           0.004        0              0.009
cc2.8xlarge       0.356           0.004        0              0.006
c3.large          0.027           0.004        0              0.007
c3.xlarge         0.053           0.004        0              0.007
c4.2xlarge        0.125           0.004        0              0.008
c4.8xlarge        0.557           0.004        0              0.009
c4.xlarge         0.060           0.004        0              0.008
hi1.4xlarge       0.370           0.011        0              0.006
```
### Launch Self-Terminating Spot Instances

Note, the defaults will need to be set for your environment:  security groups, keyname, etc.

```
(.spot-price-ml) ➜  spot_price_machine_learning git:(master) ./spot_launcher.py launch --help         
Usage: spot_launcher.py launch [OPTIONS]

  Request spot instance

Options:
  --instance TEXT       Instance Type
  --duration TEXT       Duration
  --keyname TEXT        Key Name
  --profile TEXT        IamInstanceProfile
  --securitygroup TEXT  Key Name
  --ami TEXT            Key Name
  --help                Show this message and exit.

```
To launch with a longer duration, say 1 hour and 55 minutes:
```
(.pragia-aws) ➜  pragai-aws git:(master) ✗ ./spot_launcher.py launch --duration 115


2017-09-20 06:46:53,046 - __main__ - INFO - SPOT REQUEST DATA: {'SpotPrice': '0.8', 'Type': 'one-time', 'InstanceCount': 1, 'LaunchSpecification': {'ImageId': 'ami-6df1e514', 'InstanceType': 'r4.large', 'KeyName': 'pragai', 'IamInstanceProfile': {'Arn': 'arn:aws:iam::561744971673:instance-profile/admin'}, 'UserData': 'CiAgICAgICAgI2Nsb3VkLWNvbmZpZwogICAgICAgIHJ1bmNtZDoKICAgICAgICAgLSBlY2hvICJoYWx0IiB8IGF0IG5vdyArIDExNSBtaW4KICAgIA==', 'BlockDeviceMappings': [{'DeviceName': '/dev/xvda', 'Ebs': {'DeleteOnTermination': True, 'VolumeType': 'gp2', 'VolumeSize': 8}}], 'SecurityGroupIds': ['sg-61706e07']}}
```


### Seaborn Plots from Juypter
![Spot Prices vs Spot Prices/ECU](https://user-images.githubusercontent.com/58792/30277517-e7016f3e-96bc-11e7-8dc9-348791ba7b47.png)

![Cluster Facets](https://user-images.githubusercontent.com/58792/30278742-2380d3d4-96c0-11e7-951a-e2fd76f6e603.png)

### Jupyter Notebook Version

https://github.com/noahgift/spot_price_machine_learning/blob/master/notebooks/spot_pricing_ml.ipynb

