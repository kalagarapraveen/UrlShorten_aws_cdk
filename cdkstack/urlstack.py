import os
import aws_cdk as cdk
from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as _lambda,
    aws_iam  as iam,
    aws_dynamodb as dynamodb,
    )
from constructs import Construct

class URLstack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        aws_region = os.environ['CDK_DEFAULT_REGION']
        aws_acc_num = os.environ['CDK_DEFAULT_ACCOUNT']

        url_lambda_role = iam.Role(
            self, "lambdaprod",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
            ],
            role_name="URl-shortern-role"
            )
        
        table = dynamodb.Table.from_table_arn(self, "ImportedTable", "arn:aws:dynamodb:ap-south-1:028642144348:table/url_shorten_table")
        # now you can just call methods on the table
        table.grant_read_write_data(url_lambda_role)

        cors_options= _lambda.FunctionUrlCorsOptions(
            allowed_origins=['*'], allowed_methods=[_lambda.HttpMethod.POST],
            allowed_headers=[
                'x-amz-content-sha256', 'x-amz-date', 'authorization', 'content-type'
            ]
        )

        url_lambda = _lambda.Function(
            self, 
            "url_shortern_stg", 
            code=_lambda.Code.from_asset('./src'),
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler='url_stg.main',
            description='URL lambda',
            memory_size=2048,
            timeout=cdk.Duration.seconds(30),
            role=url_lambda_role
        )

        url_lambda.add_function_url(cors=cors_options)


