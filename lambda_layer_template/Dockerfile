ARG RUNTIME=runtime
FROM python:${RUNTIME}
RUN apt-get update && apt-get install zip
ENV MyPath = "python/lib/python3.7/site-packages"
RUN mkdir -p $MyPath && mkdir tempdir
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt --target tempdir/
RUN mv tempdir/* ${MyPath}
RUN zip -r DockerZip.zip ${MyPath}/*
