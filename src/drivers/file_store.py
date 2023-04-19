import os
import logging


class FileStoreDriver:

    BASE_DIR = './files/'

    def __init__(self, subgraph_name: str) -> None:
        self.subgraph_storage = f'{self.BASE_DIR}{subgraph_name}'
        self.__create_subgraph_dir()

    def save(self, file_name: str, data: bytes) -> bool:
        try:
            with open(f'{self.subgraph_storage}/{file_name}', 'wb') as file_obj:
                file_obj.write(data)
                return True
        except Exception as e:
            logging.error(e)
            return False

    def get(self, file_name: str) -> bytes:
        with open(f'{self.subgraph_storage}/{file_name}', 'rb') as file_obj:
            return file_obj.read()

    def __create_subgraph_dir(self) -> bool:
        if os.path.isdir(self.subgraph_storage):
            return False
        os.makedirs(self.subgraph_storage)
        return True
