# Subgraphs ipfs copier

Sometimes we need to move subgraphs just by hash between few ipfs node, there tools help you with it.

## Install apps

```bash
python3 -m venv .venv 
. ./setenv.sh
pip3 install -r requirements.txt
```

## Configuration

```bash
cat baseconfig.env > .env
```

### Config params

```bash
LOG_LEVEL="INFO"
IPFS_HOST="127.0.0.1"
IPFS_PORT=5001
```

## Run apps

### Copy subgraph from ipfs

This app are trying to get main subgraph config from ipfs and download all deps from current IPFS Node.

```bash
python3 src/apps/copy_subgraph_from_ipfs.py {YOUR_SUBGRAPH_IPFSHASH}
```

### Upload existing subgraph to ipfs node

```bash
python3 src/apps/direct_subgraph_copy_to_ipfs_without_mapping.py {YOUR_SUBGRAPH_IPFSHASH}
```

### Upload existing subgraph to ipfs node if you changed subgraph manifest

This app app upload already downloaded subgraph files to IPFS node.

```bash
python3 src/apps/copy_subgraph_to_ipfs.py {YOUR_SUBGRAPH_IPFSHASH}
```
