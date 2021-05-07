# aws-tools

A collection of some AWS tools that may come in handy.
## AiCli [<img src="https://raw.githubusercontent.com/devicons/devicon/c7d326b6009e60442abc35fa45706d6f30ee4c8e/icons/python/python-original.svg" height=15> ](Python)

A cli for some fast aws shortcuts.

Installed as:
```cmd python
>> cd AiCli
>> pip install --editable .
```
AWS credentials are required
___
## lambda_layer_template [<img src="https://raw.githubusercontent.com/devicons/devicon/c7d326b6009e60442abc35fa45706d6f30ee4c8e/icons/docker/docker-original.svg" width=20> ](Docker) [<img src="https://raw.githubusercontent.com/devicons/devicon/c7d326b6009e60442abc35fa45706d6f30ee4c8e/icons/python/python-original.svg" height=15> ](Python)

Generate a lambda layer based on an requirements.txt file.
```python
awesome-package==1.33.7
```
Used as
```cmd
>> python main.py [your-layer-name] [python-runtime]
```
Requires Docker to run
