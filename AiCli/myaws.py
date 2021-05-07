import boto3
import click
from aws_cli import aws_cli
import time

@click.group()
def cli():
    pass


@cli.command()
def ls():
    """List all instances and there states"""
    ls = aws_cli().get_instance_status()
    for ins, val in ls.items():
        click.echo(
            '{:<20s} [{}] - state: {:<20s}'.format(
                ins,
                val['id'],
                val['state']
                )
            )


@cli.command()
def running():
    """Get all running instances"""
    running = aws_cli().get_running_instances()
    click.echo(running)


@cli.command()
def stopped():
    """Get all stoped instances"""
    stopped = aws_cli().get_stopped_instances()
    click.echo(stopped)


@cli.command()
@click.option('--instance', '-i', required=True)
@click.option('--update', '-u', is_flag=True)
def run(instance, update):
    """Start instance"""
    aws = aws_cli()
    try:
        aws.run_instance(instance_name=instance)
        click.echo(f'Starting the instance {instance}.')
        time.sleep(0.5)
        click.echo(f"Retriving the new IP for {instance}...")
        time.sleep(4)
        while True:
            try:
                IP = aws.get_instance_IP(instance)
                break
            except Exception:
                time.sleep(1)
                continue

        click.echo(f"{instance}: {IP}")
        if update:
            click.echo(f"Updating the SSH Config")
            res = aws.update_ssh_config(instance_name=instance)
            if res == -1:
                click.echo('Something funky happend :/')
    except Exception:
        click.echo(
            f"Can't start the instance: {instance}.\n"
            "This might indicate that the instance is already running"
            " or that you perhaps made a typo :/"
            )


@cli.command()
@click.option('--instance', '-i', required=True)
def stop(instance):
    """Stop instance"""
    try:
        aws_cli().stop_instance(instance_name=instance)
        click.echo(f"Stopping instance: {instance}")
    except Exception:
        click.echo(
            f"Can't stop the instance: {instance}. "
            "This might indicate that the instance is not running"
            " or that you perhaps made a typo :/"
            )


@cli.command()
@click.option('--instance', '-i', required=True)
def ip(instance):
    """Get Instance Public IP adress"""
    try:
        ip = aws_cli().get_instance_IP(instance_name=instance)
        click.echo(ip)
    except Exception:
        click.echo(
            f"Can't fetch the IP for instance: {instance}. "
            "This might indicate that the instance is not running"
            " or that you perhaps made a typo :/"
        )


cli.add_command(ls)
cli.add_command(running)
cli.add_command(stopped)
cli.add_command(run)
cli.add_command(stop)
cli.add_command(ip)

if __name__ == "__main__":
    cli()
