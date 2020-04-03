"""
Place to put environment variables that are read by the unit test harness
"""
import os
import re

# Host to connect to
DOCKER_HOST = os.environ.get('DOCKER_HOST', '')

# Get the Docker Hostname from the docker host.
# i.e. tcp://jenkins:2375 => jenkins
match = re.match(r'^(.*://)?(.*):[0-9]+$', DOCKER_HOST)
DOCKER_HOSTNAME = match[2] if match else 'localhost'

# Docker tag to use in containers booted up for tests
TAG = os.environ.get('TAG', 'latest')

# Which Docker containers to show logs for in docker-compose calls. Can be a comma
# Serparated list of containers, or 'all' for all logs
DOCKER_LOGS = os.environ.get('DOCKER_LOGS', '').replace(',', ' ')

# Whether to show logs from docker compsoe subprocess OVERRIDES DOCKER_LOGS
SUBPROCESS_LOGS = os.environ.get('SUBPROCESS_LOGS', '1')

# Label to identify all testing resources
TEST_LABEL = 'eucalyptus_client'
