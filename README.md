# Architecture Overview

This Project creates an environment in AWS:
1. A VPC
2. An ECS cluster
3. An LoadBalancer with public domain name
4. A Fargate service running in the ECS cluster
5. Log stream of the Fargate service will be sent to CloudWatch
6. CloudWatch will send emails to the admins when `ERROR` is detected in the logs

![image](images/Arch%20Overview.png)

# Install Dependencies
To manually create a virtualenv on MacOS and Linux:

```bash
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```bash
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```bash
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```bash
$ pip3 install -r requirements.txt
```

# Prepare Environment Variables
Cdk will use your AWS account id and credentials, set them as environment variables
```bash
export AWS_ACCOUNT_ID=<AWS_ACCOUNT_ID>
export AWS_REGION=us-west-2
export AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>
export AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>
```

# Configurations
Configuration file `config.yaml` is under the root path of the repo.
- **ALERT_KEYWORD**: Alert will be triggered if the ALERT_KEYWORD is detected in the service log, default is `ERROR`(For testing purpose, you can set it to `INFO` to receive the alert email notification)
- **ADMIN_EMAILS**: The email addresses listed here will receive alert notification, set it to your administrators' email addresses.

# Create Stack in AWS
At this point you can now synthesize the CloudFormation template for this code.

```bash
$ cdk synth
```

Then run command to create your stack in AWS
```bash
$ cdk deploy
```

After the stack being deployed, you can find the fargate service url in the output like below:
```bash
[...snip...]
Outputs:
CdkStack.MyFargateServiceLoadBalancerDNS704F6391 = CdkSta-MyFar-qVJemk7PHa1u-2119635329.us-west-2.elb.amazonaws.com
CdkStack.MyFargateServiceServiceURL4CF8398A = http://CdkSta-MyFar-qVJemk7PHa1u-2119635329.us-west-2.elb.amazonaws.com
[...snip...]
```

Go to the site `http://CdkSta-MyFar-qVJemk7PHa1u-2119635329.us-west-2.elb.amazonaws.com` in your browser, you will see the response:
```
Hello FUCKING World!!!
```
