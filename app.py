#!/usr/bin/env python3
import os

import aws_cdk as cdk
from cdk.cdk_stack import CdkStack

app = cdk.App()
CdkStack(app, "CdkStack",env=cdk.Environment(
        account=os.getenv('AWS_ACCOUNT_ID'),
        region=os.getenv('AWS_REGION', "us-west-2"),
    ),   
)
app.synth()
