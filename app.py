#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdkstack.urlstack import URLstack


app = cdk.App()
URLstack(app, "URLstack",
    env=cdk.Environment(account=os.environ['CDK_DEFAULT_ACCOUNT'],
                     region=os.environ['CDK_DEFAULT_REGION']),
    )

app.synth()
