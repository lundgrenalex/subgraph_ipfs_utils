import logging
import typing as tp

from pydantic import BaseModel

from src.repository import SubgraphsRepository
from src.use_cases.base import BaseUseCase


class SubgraphFile(BaseModel):
    cid: str
    data: bytes
    file_type: str


class CopySubgraphToIpfsBaseError(Exception):
    code = 100501
    message = 'Base error for copy subgraph to ipfs use case'


class ManifestNotExists(CopySubgraphToIpfsBaseError):
    code = 100502
    message = 'Manifest doesn\'t exist yet, u have download before'


class FileFromManifestNotExists(CopySubgraphToIpfsBaseError):
    code = 100502
    message = 'File from manifest doesn\'t exist yet, u have download before'


class DirectCopySubgraphToIpfsUseCase(BaseUseCase):

    subgraph_files: tp.List[SubgraphFile] = []

    def __init__(self, subgraphs_repo: SubgraphsRepository) -> None:
        self.subgraphs_repo = subgraphs_repo
        self.subgraph_store = './files'

    def execute(self, uc_request: tp.Optional[tp.Any]) -> tp.Any:

        # get mainfest from store
        subgraph_manifest = self.subgraphs_repo.get_manifest(uc_request)
        if not subgraph_manifest:
            raise ManifestNotExists

        # get all subgraph cids from manifest
        files_cids = self.subgraphs_repo.get_cids_from_manifest(subgraph_manifest)

        # get all files from subgraph cid, owerwise rise Error
        for cid in files_cids:
            cid_data = self.subgraphs_repo.get_file_from_store(f'{cid.name}.{cid.file_type}')
            if not cid_data:
                raise FileFromManifestNotExists
            self.subgraph_files.append(
                SubgraphFile(cid=cid.name, data=cid_data, file_type=cid.file_type))

        # upload files to ipfs and save metainformation about destanation
        for sf in self.subgraph_files:
            file_path = f'{self.subgraph_store}/{uc_request}/{sf.cid}.{sf.file_type}'
            upload_result_from_ipfs = self.subgraphs_repo.upload(file_path)
            logging.warning(upload_result_from_ipfs)

        # upload manifest
        file_path = f'{self.subgraph_store}/{uc_request}/{uc_request}.yaml'
        deploy_info = self.subgraphs_repo.upload(file_path)
        logging.info(deploy_info)
