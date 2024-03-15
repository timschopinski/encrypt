import os
import unittest


class MediaTestCase(unittest.TestCase):
    MEDIA_DIR = None

    @classmethod
    def tearDownClass(cls) -> None:
        for filename in os.listdir(cls.MEDIA_DIR):
            file_path = os.path.join(cls.MEDIA_DIR, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Error while deleting {file_path}: {e}")
