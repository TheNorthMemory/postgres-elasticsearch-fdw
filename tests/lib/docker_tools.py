""" Commands for interacting with docker """
# pylint: disable=no-member

from os.path import join

import io
import re
import sh

from .tools import DOCKER_FOLDER

def docker_compose(version):
    """ Wrapper around the docker compose command """

    compose_file = join(DOCKER_FOLDER, version, 'docker-compose.yml')
    return sh.docker_compose.bake('-f', compose_file)

def exec_container(version, container):
    """ Wrapper around executing commands in a container """

    container = container_name(version, container)
    return sh.docker.bake('exec', '-i', container)

def container_name(version, container):
    """ Determine container name """

    with io.StringIO() as buf:
        docker_compose(version)('ps', '-q', container, _out=buf)
        return re.sub(r'\n.*', '', buf.getvalue())

def container_port(version, container, port):
    """ Determine mapped container port """

    with io.StringIO() as buf:
        docker_compose(version)('port', container, port, _out=buf)
        host_and_port = re.sub(r'\n.*', '', buf.getvalue())
        return re.sub(r'.*:', '', host_and_port)
