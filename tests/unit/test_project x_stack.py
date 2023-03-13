import aws_cdk as core
import aws_cdk.assertions as assertions

from project x.project x_stack import ProjectXStack

# example tests. To run these tests, uncomment this file along with the example
# resource in project x/project x_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ProjectXStack(app, "project-x")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
