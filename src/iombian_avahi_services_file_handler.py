#!/usr/bin/env python3

import json
import logging
from watchdog.events import FileSystemEventHandler, FileModifiedEvent
from watchdog.observers import Observer
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)


class IoMBianAvahiServicesFileHandler(FileSystemEventHandler):

    def __init__(self, file_path="/etc/avahi/services/iombian.service"):
        self.file_path = file_path
        self.tree = None
        self.services_discovered_callback = None
        self.observer = None
        self.load_file()

    def start(self):
        logger.debug("Starting Avahi Service File Handler")
        if self.observer:
            logger.error("Service already started")
            return
        self.observer = Observer()
        self.observer.schedule(self, self.file_path)
        self.observer.start()
        self.load_services()

    def stop(self):
        logger.debug("Stopping Avahi Service File Handler")
        if self.observer:
            self.observer.stop()
            self.observer.join()

    def add_services_discovered_callback(self, callback):
        if self.services_discovered_callback:
            logger.warn("Services discovered callback already set")
            return
        self.services_discovered_callback = callback

    def load_file(self):
        self.tree = ET.parse(self.file_path)

    def on_modified(self, event):
        if isinstance(event, FileModifiedEvent):
            logger.debug(f"Avahi file ('{self.file_path}') has been modified")
            self.load_services()

    def load_services(self):
        services = {}
        txt_records_elements = self.tree.findall(".//txt-record")
        for txt_record_element in txt_records_elements:
            txt_record = txt_record_element.text
            service_name, service_info = txt_record.split("=")
            services[service_name] = json.loads(service_info)
        if self.services_discovered_callback:
            self.services_discovered_callback(services)
