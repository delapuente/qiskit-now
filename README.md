# qiskit-now

> Qiskit development environment without the configuration pain

## How it works?

`qiskit-now` runs a docker image with all the environment you need to start working with [Qiskit](https://github.com/Qiskit/qiskit/).

## Prerequisites

You need to [install and run Docker](https://docs.docker.com/get-docker/) before launching `qiskit-now`.

## Installation

Use `pip` with any [Python after version 3.7](https://www.python.org/downloads/):

```sh
$ pip install qiskit-now
```

## Run it!

After installing, run this in a command line:

```sh
$ qiskit-now
```

## Using Docker directly

You can also run the following command in macOS or Linux:

```sh
$ docker run -it \
    --user "$(id -u):$(id -g)" \
    --name="qiskit-now" \
    --env="HOME=$HOME" \
    --volume="/etc/group:/etc/group:ro" \
    --volume="/etc/passwd:/etc/passwd:ro" \
    --volume="/etc/shadow:/etc/shadow:ro" \
    --volume="$HOME:$HOME" \
    --publish="8888:8888/tcp" \
    --workdir="$PWD" \
    delapuente/qiskitnow:latest
```

And this other one in Windows:

```sh
$ docker run -it \
    --user "$(id -u):$(id -g)" \
    --name="qiskit-now" \
    --env="HOME=$HOME" \
    --volume="/etc/group:/etc/group:ro" \
    --volume="/etc/passwd:/etc/passwd:ro" \
    --volume="/etc/shadow:/etc/shadow:ro" \
    --volume="$HOME:$HOME" \
    --publish="8888:8888/tcp" \
    --workdir="$PWD" \
    delapuente/qiskitnow:latest
```