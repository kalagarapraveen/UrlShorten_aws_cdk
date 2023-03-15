import os
import subprocess

from aws_cdk import(
    Stack,
    aws_lambda as _lambda
    )

from constructs import Construct

def subprocess_cmd(command):
    process=subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    print(proc_stdout.decode("utf-8"))


class UrlLayersStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        layer_directory = "./bit_layer"
        if not os.path.isdir(layer_directory):
            subprocess_cmd("Echo 'Building python layers'; ./build_bit_layer_requirements.sh")

        bit_layer = _lambda.LayerVersion(
            self,
            "BitLayer",
            code=_lambda.Code.from_asset(f'{layer_directory}'),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_9],
            description="Bit Layer for dependencies"
        )
