import typing as tp
import ipfshttpclient2
import logging


class IpfsDriverBaseError(Exception):
    code = 100500
    messages = 'Couldn\'t get data from ipfs node'


class IpfsDriver:

    def __init__(self, host: str, port: int) -> None:
        addr = f'/ip4/{host}/tcp/{port}/http'
        self.__store = ipfshttpclient2.Client(addr)

    def test_connection(self,) -> tp.Any:
        return self.__store.id()

    def upload(self, file_path: str) -> None:
        res = self.__store.add(file_path)
        logging.info(res)
        return res

    def get(self, cid: str) -> bytes:
        res = self.__store.cat(cid=cid)
        return res

    def download(self, hash: str, dst: str) -> None:
        self.__store.get(hash)
