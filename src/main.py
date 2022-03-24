#!/usr/bin/env python3

import logging
import signal
import time

from communication_module import CommunicationModule
from firestore_services_handler import FirestoreServicesHandler
from iombian_avahi_services_file_handler import IoMBianAvahiServicesFileHandler

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s - %(name)-16s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def signal_handler(sig, frame):
    logger.info("Stopping IoMBian Services Uploader Service")
    comm_module.stop()
    firestore_services_handler.stop()
    avahi_file_handler.stop()


def on_services_discovered(services):
    if services != firestore_services_cache:
        logger.info("Database services are different, synchronize them")
        firestore_services_handler.update_services(services)


def on_db_services_updated(services):
    global firestore_services_cache
    logger.debug(f"Database services updated: {services}")
    firestore_services_cache = services


if __name__ == "__main__":
    logger.info("Starting IoMBian Services Uploader Service")

    comm_module = CommunicationModule(host="127.0.0.1", port=5555)
    comm_module.start()

    api_key = comm_module.execute_command("get_api_key")
    project_id = comm_module.execute_command("get_project_id")
    refresh_token = comm_module.execute_command(
        "get_refresh_token")
    device_id = comm_module.execute_command("get_device_id")

    firestore_services_cache = None
    firestore_services_handler = FirestoreServicesHandler(
        api_key, project_id, refresh_token, device_id)
    firestore_services_handler.add_services_update_callback(
        on_db_services_updated)
    firestore_services_handler.start()

    while(firestore_services_cache == None):
        time.sleep(0.1)

    avahi_file_handler = IoMBianAvahiServicesFileHandler()
    avahi_file_handler.add_services_discovered_callback(on_services_discovered)
    avahi_file_handler.start()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.pause()
