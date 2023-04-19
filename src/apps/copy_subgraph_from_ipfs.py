import logging
import sys

from src.drivers import FileStoreDriver, IpfsDriver
from src.repository import SubgraphsRepository
from src.settings.base import AppSettings
from src.use_cases import CopySubgraphFromIpfsUseCase


def run_app() -> None:

    try:
        subgraph_ipfs_hash = sys.argv[1]
    except IndexError:
        sys.exit('Pleace, provede ipfs hash for subgraph.')

    # settings
    settings = AppSettings()

    # logging setup
    logging.basicConfig(**settings.logging_settings.dict())

    # drivers
    ipfs_driver = IpfsDriver(
        host=settings.ipfs.host,
        port=settings.ipfs.port)

    # test connection
    logging.info(f"IPFS CONNECTION ID: {dict(ipfs_driver.test_connection())['ID']}")

    file_store_driver = FileStoreDriver(subgraph_ipfs_hash)

    # repository
    subgraph_repo = SubgraphsRepository(ipfs_driver, file_store_driver)

    # use_case
    use_case = CopySubgraphFromIpfsUseCase(subgraph_repo)
    use_case.execute(subgraph_ipfs_hash)


if __name__ == '__main__':
    run_app()
