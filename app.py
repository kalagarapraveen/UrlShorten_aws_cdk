#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdkstack.urlstack import URLstack
from cdkstack.UrlLayerstack import UrlLayersStack


app = cdk.App()

UrlLayersStack(app, "UrlLayersStack", env=cdk.Environment(
    account='${{ secrets.CDK_DEFAULT_ACCOUNT_PERSONAL }}',  #os.environ['CDK_DEFAULT_ACCOUNT_PERSONAL'],
    region=os.environ['CDK_DEFAULT_REGION']
    ), description="URL Layers stack that creates Lambda layers for URL shorten project"
)


URLstack(app, "URLstack", env=cdk.Environment(
    account=os.environ['CDK_DEFAULT_ACCOUNT_PERSONAL'],
    region=os.environ['CDK_DEFAULT_REGION']
    ), description="URL Layers stack that creates Lambda layer for URL shorten project"
)

app.synth()
