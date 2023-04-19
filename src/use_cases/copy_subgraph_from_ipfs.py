import logging
import typing as tp

import yaml

from src.repository import SubgraphsRepository
from src.repository.subgraphs import SubgraphFile
from src.use_cases.base import BaseUseCase


class CopySubgraphFromIpfsUseCase(BaseUseCase):

    cids: tp.List[SubgraphFile] = []

    def __init__(self, subgraphs_repo: SubgraphsRepository) -> None:
        self.subgraphs_repo = subgraphs_repo

    def __save(self,) -> None:
        for subgraph_file in self.cids:
            self.subgraphs_repo.download(
                subgraph_file.name, subgraph_file.file_type)

    def execute(self, uc_request: tp.Any) -> tp.Any:
        logging.info(f'UseCase started, uc_request is: {uc_request}')
        main_subgraph_config_bytes: bytes = self.subgraphs_repo.get(uc_request)
        if not main_subgraph_config_bytes:
            logging.warning(f'Cannot get data from ipfs, data is: {main_subgraph_config_bytes}')
            return False

        self.cids.append(SubgraphFile(name=uc_request, file_type='yaml'))
        manifest_raw: str = main_subgraph_config_bytes.decode(encoding='utf-8')
        manifest: tp.Dict[str, tp.Any] = yaml.safe_load(manifest_raw)
        sids_from_manifest = self.subgraphs_repo.get_cids_from_manifest(manifest)
        self.cids += sids_from_manifest
        self.__save()
