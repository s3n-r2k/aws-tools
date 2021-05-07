import os

import click


@click.command()
@click.argument("name")
@click.argument("runtime")
def main(name, runtime):
    os.system(f"echo {runtime}")
    os.system(f"docker build -t {name} . --build-arg RUNTIME={runtime}")
    os.system(f"docker run --name test_1337 -idt {name}")
    os.system(f"docker cp test_1337:/DockerZip.zip {name}.zip")
    os.system("docker stop test_1337")
    os.system("docker container rm test_1337")
    os.system(f"docker image rm {name}")


if __name__ == "__main__":
    main()
