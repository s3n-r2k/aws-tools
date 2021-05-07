import boto3
import os
import re


class aws_cli:
    def __init__(self, region: str = 'eu-central-1'):
        self.client = boto3.client('ec2', region)

    def get_instance_status(self):
        # Get Instances
        Reservations = self.client.describe_instances().get('Reservations', [])
        all_instances = {}
        for reservation in Reservations:
            for instance in reservation.get('Instances', []):
                instance_id = instance.get('InstanceId')
                state = instance.get('State').get('Name')
                for tag in instance['Tags']:
                    if tag['Key'] == 'Name':
                        instance_name = tag.get('Value')
                all_instances.update(
                    {instance_name: {'id': instance_id, 'state': state}}
                )
        return all_instances

    def get_running_instances(self) -> dict:
        return {
            key: val['id'] for key, val in self.get_instance_status().items()
            if val['state'] == 'running'
        }

    def get_stopped_instances(self) -> dict:
        return {
            key: val['id'] for key, val in self.get_instance_status().items()
            if val['state'] == 'stopped'
        }

    def stop_all_instances(self) -> None:
        instances_to_stop = [
            instance_id for instance_id in
            self.get_running_instances().values()
        ]
        self.client.stop_instances(
            InstanceIds=[*instances_to_stop]
        )

    def run_instance(self, instance_name: str) -> None:
        try:
            instances_to_start = self.get_stopped_instances()[instance_name]
        except Exception:
            raise(Exception(f"Invalid Instance Name: {instance_name}"))
        # Start instance
        self.client.start_instances(InstanceIds=[instances_to_start])

    def stop_instance(self, instance_name: str) -> None:
        try:
            instances_to_start = self.get_running_instances()[instance_name]
        except Exception:
            raise(Exception(f"Invalid Instance Name: {instance_name}"))
        # Stop instance
        self.client.stop_instances(InstanceIds=[instances_to_start])

    def get_instance_IP(self, instance_name: str) -> str:
        try:
            instance_id = self.get_running_instances()[instance_name]
        except Exception:
            raise(Exception(f"Invalid Instance Name: {instance_name}"))
        IP = self.client.describe_instances(
            InstanceIds=[instance_id]
        ).get('Reservations', [])[0].get('Instances')[0].get('PublicIpAddress')
        return IP

    def update_ssh_config(self, instance_name: str) -> None:
        ssh_path = os.path.join(
            os.path.expanduser('~'),
            '.ssh/config'
        )
        try:
            new_ip = self.get_instance_IP(instance_name=instance_name)
            with open(ssh_path, 'r') as config_file:
                new_config = config_file.read()

            with open(ssh_path, 'w') as config_file:
                alt_config = new_config.replace('\n', '\\n')
                regex = fr"(Host {instance_name}.*?HostName )(.*?)(\\n)"
                substr = f"\\g<1>{new_ip}\\g<3>"
                alt_config = re.sub(regex, substr, alt_config, 0, re.MULTILINE)
                alt_config = alt_config.replace('\\n', '\n')
                if len(alt_config) > 0:
                    config_file.write(alt_config)
                else:
                    config_file.write(new_config)
                    return -1
        except Exception:
            raise(Exception(f"Invalid Instance Name: {instance_name}"))






