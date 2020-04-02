"""Docker utilities"""
import docker
from . config import TEST_LABEL
from logging import getLogger


log = getLogger(__name__)


def create_network(network_name, label=TEST_LABEL):
    """Create or get a network for services"""
    client = docker.from_env()
    networks = client.networks.list(names=[network_name])

    # Get the network if it exists
    if len(networks) > 0:
        log.info(f'Network {network_name} found')
        return networks[0]

    log.info(f'Creating new network {network_name}')
    return client.networks.create(
        network_name,
        labels={label: label},
        attachable=True,
        check_duplicate=True
    )


def remove_network(network_name):
    """Finds and removes network by name, if it exists"""
    client = docker.from_env()
    networks = client.networks.list(names=[network_name])

    # Get the network if it exists
    if len(networks) == 0:
        log.info(f'No network named: {network_name}')
        return

    # Remove the network
    return networks[0].remove()


def clean_up(labels=TEST_LABEL):
    """
    Clean up all docker resources allocated
    """
    client = docker.from_env()

    # Find and kill containers
    containers = client.containers.list(all=True, filters={'label': [labels]})
    num1 = len(containers)
    for container in containers:
        container.remove(force=True)

    # Find and rewmove networks
    networks = client.networks.list(filters={'label': labels})
    num2 = len(containers)
    for network in networks:
        network.remove()

    log.info(f'Removed {num1} Containers and {num2} Networks')
