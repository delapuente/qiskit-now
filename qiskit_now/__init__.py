#!/usr/bin/env python

import os
import pwd
import argparse
import logging
import urllib3

import docker
import docker.errors


logger = logging.getLogger(__name__)

def _env():
    return {
        'HOME': _user_home()
    }


def _container_name():
    return 'qiskit-now'


def _host_user_and_group():
    return _user_id()


def _user_home():
    from pathlib import Path
    return Path.home()


def _user_id():
    return os.geteuid()


def _user_group():
    return pwd.getpwuid(_user_id()).pw_gid


def _working_dir():
    return os.getcwd()


def _volumes():
    home = _user_home()
    return {
        '/etc/group': { 'bind': '/etc/group', 'mode': 'ro' },
        '/etc/passwd' : { 'bind': '/etc/passwd', 'mode': 'ro' },
        '/etc/shadow': { 'bind': '/etc/shadow', 'mode': 'ro' },
        f'{home}': { 'bind': f'{home}', 'mode': 'rw' },
    }


def _ports():
    port = 8888
    return { f'{port}/tcp': port }


def _run():
    environment = _env()
    name = _container_name()
    user_and_group = _host_user_and_group()
    working_dir = _working_dir()
    volumes = _volumes()
    ports = _ports()

    try:
        client = docker.from_env()
    except docker.errors.DockerException as e:
        if _is_connection_refused(e):
            logger.warning('Docker seems not to be running. Launch Docker before using qiskit-now.')
            logger.warning('You can get Docker from https://docs.docker.com/get-docker/')
        else:
            raise e
    else:
        client.containers.run(
            'delapuente/qiskitnow:latest',
            environment=environment,
            name=name,
            user=user_and_group,
            working_dir=working_dir,
            volumes=volumes,
            ports=ports
        )


def _is_connection_refused(e: docker.errors.DockerException) -> bool:
    current_exception = e
    while current_exception.__context__:
        current_exception = current_exception.__context__
        if isinstance(current_exception, urllib3.exceptions.ConnectionError):
            return True

    return False

def main():
    parser = argparse.ArgumentParser(
        description='Qiskit development environment without the configuration pain.')
    _args = parser.parse_args()
    _run()

if __name__ == '__main__':
    main()