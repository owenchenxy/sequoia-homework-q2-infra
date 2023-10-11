import aws_cdk as core
from aws_cdk import (
    Stack,
    aws_logs as logs,
    aws_ec2 as ec2, 
    aws_sns as sns,
    aws_ecs as ecs,
    aws_sns_subscriptions as subs,
    aws_cloudwatch as cloudwatch,
    aws_cloudwatch_actions as cw_actions,
    aws_ecs_patterns as ecs_patterns
)
from constructs import Construct
from cdk.config import Config

class CdkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # Get Configs
        globals().update(Config().config)

        # Create default VPC
        vpc = ec2.Vpc(self, "MyVpc", max_azs=3)     

        # Create ECS cluster
        cluster = ecs.Cluster(self, "MyCluster", vpc=vpc, cluster_name="MyCluster")

        # Create CloudWatchlog group
        log_group = logs.LogGroup(self, "FargateLogs",
                                  log_group_name="FargateLogs",
                                  retention=logs.RetentionDays.ONE_WEEK,
                                  removal_policy=core.RemovalPolicy.DESTROY)
        
        # Create ECS Fargate service
        ecs_patterns.ApplicationLoadBalancedFargateService(self, "MyFargateService",
            cluster=cluster,            # Required
            service_name="MyFargateService",
            cpu=512,                    # Default is 256
            desired_count=6,            # Default is 1
            memory_limit_mib=2048,      # Default is 512
            public_load_balancer=True,
            listener_port=80,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                family="CdkStackTaskDefinition",
                container_port=9092,
                image=ecs.ContainerImage.from_registry("ghcr.io/owenchenxy/example-hello-world:init"),
                log_driver=ecs.LogDrivers.aws_logs(
                    stream_prefix="FargateLogs",
                    log_group=log_group
                )
            )
        )  
        
        # Create SNS Topic
        topic = sns.Topic(self, "ErrorLogsTopic")
        for email in ADMIN_EMAILS:
            topic.add_subscription(subs.EmailSubscription(email_address=email))

        # Create CloudWatch Logs Metric Filter
        metricFilter = logs.MetricFilter(self, "ErrorLogsMetricFilter",
                          log_group=log_group,
                          filter_pattern=logs.FilterPattern.literal(ALERT_KEYWORD),
                          metric_namespace="MyNamespace",
                          metric_name="ErrorLogsMetric",
                          metric_value="1",
                          )
        
        # Create CloudWatch Alarm
        alarmAction = cw_actions.SnsAction(topic)
        cloudwatch.Alarm(self, "ErrorLogsAlarm",
                         metric=metricFilter.metric(),
                         comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
                         threshold=1,
                         evaluation_periods=1,
                         datapoints_to_alarm=1,
                         treat_missing_data=cloudwatch.TreatMissingData.NOT_BREACHING,
                         alarm_description="Alarm if ERROR keyword found in logs.",
                        ).add_alarm_action(alarmAction)