import logging
import typing as tp

import yaml
from pydantic import BaseModel

from src.drivers import FileStoreDriver, IpfsDriver


class SubgraphFile(BaseModel):
    name: str
    file_type: str


class SubgraphsRepository:

    def __init__(self, ipfs_driver: IpfsDriver, file_store_driver: FileStoreDriver) -> None:
        self.__ipfs_driver = ipfs_driver
        self.__file_store_driver = file_store_driver

    def get_file_from_store(self, file_name: str) -> bytes:
        return self.__file_store_driver.get(file_name)

    def get_manifest(self, cid: str) -> tp.Dict[str, tp.Any]:
        bytes_manifest: bytes = self.get_file_from_store(f'{cid}.yaml')
        return yaml.safe_load(bytes_manifest)

    def upload(self, file_path: str) -> tp.Any:
        return dict(self.__ipfs_driver.upload(file_path))

    def get(self, cid: str) -> bytes:
        return self.__ipfs_driver.get(cid=cid)

    def download(self, cid: str, file_type: str) -> None:
        data: bytes = self.__ipfs_driver.get(cid=cid)
        self.__file_store_driver.save(f'{cid}.{file_type}', data)

    def get_cids_from_manifest(self, manifest: tp.Dict[str, tp.Any]) -> tp.List[SubgraphFile]:

        cids = []

        def get_cid(cid_with_path: str) -> str:
            return cid_with_path.replace('/ipfs/', '')

        # MAPPING PROCCESING
        if 'dataSources' in manifest:
            for m in manifest['dataSources']:

                cids.append(
                    SubgraphFile(
                        name=get_cid(m['mapping']['file']['/']),
                        file_type='wasm'))

                for abis in m['mapping']['abis']:
                    cids.append(
                        SubgraphFile(
                            name=get_cid(abis['file']['/']),
                            file_type='json'))

        # TEMPLATES PROCESSING
        if 'templates' in manifest:
            for tm in manifest['templates']:

                cids.append(
                    SubgraphFile(
                        name=get_cid(tm['mapping']['file']['/']),
                        file_type='wasm'))

                for abis in tm['mapping']['abis']:
                    cids.append(
                        SubgraphFile(
                            name=get_cid(abis['file']['/']),
                            file_type='json'))

        # SCHEMA RROCESSING
        if 'schema' in manifest:
            cids.append(
                SubgraphFile(
                    name=get_cid(manifest['schema']['file']['/']),
                    file_type='graphql'))

        return cids

    def change_cids_in_manifest(
            self,
            manifest: tp.Dict[str, tp.Any],
            cids: tp.List[tp.Dict[str, str]]) -> tp.Dict[str, tp.Any]:
        """Return a new manifest with changed cids"""

        def get_cid(ipfs_path: str) -> str:
            return ipfs_path.replace('/ipfs/', '')

        def get_new_ipfs_path(old_ipfs_path: str, new_cids: tp.List[tp.Dict[str, str]]) -> str:
            current_cid = get_cid(old_ipfs_path)
            for cid in new_cids:
                logging.info([cid['name_without_type'], current_cid])
                if cid['name_without_type'] == current_cid:
                    return f"/ipfs/{cid['name_without_type']}"
            return ''

        # MAPPING PROCCESING
        if 'dataSources' in manifest:
            for m in manifest['dataSources']:
                # WASM
                m['mapping']['file']['/'] = get_new_ipfs_path(
                    m['mapping']['file']['/'], cids)
                for abis in m['mapping']['abis']:
                    # JSON
                    abis['file']['/'] = get_new_ipfs_path(
                        abis['file']['/'], cids)
        # TEMPLATES PROCESSING
        if 'templates' in manifest:
            for tm in manifest['templates']:
                # WASM
                tm['mapping']['file']['/'] = get_new_ipfs_path(
                    tm['mapping']['file']['/'], cids)
                for abis in tm['mapping']['abis']:
                    # JSON
                    abis['file']['/'] = get_new_ipfs_path(
                        abis['file']['/'], cids)
        # SCHEMA RROCESSING
        if 'schema' in manifest:
            # SCHEMA
            manifest['schema']['file']['/'] = get_new_ipfs_path(
                manifest['schema']['file']['/'], cids)

        return manifest
