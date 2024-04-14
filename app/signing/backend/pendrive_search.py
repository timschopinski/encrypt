import os
import time

import psutil
from PyQt6.QtCore import pyqtSignal, QObject, QThread


class PendriveSearchWorker(QObject):
    found_private_key = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._stop_search = False

    def search(self):
        while not self._stop_search:
            mounted_disks = psutil.disk_partitions()

            for disk in mounted_disks:
                disk_path = disk.mountpoint
                private_key_files = [f for f in os.listdir(disk_path) if f.endswith('.pem')]
                if private_key_files:
                    encrypted_private_key_path = os.path.join(disk_path, private_key_files[0])
                    self.found_private_key.emit(encrypted_private_key_path)
                    self.finished.emit()
                    return

            time.sleep(0.5)

    def stop_search(self):
        self._stop_search = True


class PendriveSearchThread(QThread):
    def __init__(self):
        super().__init__()
        self.worker = PendriveSearchWorker()

    def run(self):
        self.worker.search()
