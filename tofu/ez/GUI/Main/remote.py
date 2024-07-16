import logging
import os
import time
from pathlib import Path

from tofu.ez.main import execute_reconstruction
from tofu.ez.params import EZVARS
from tofu.ez.util import export_values

logger = logging.getLogger(__name__)

try:
    from dotenv import load_dotenv
except ImportError:
    logger.info("Install python-dotenv to enable .env file support.")
else:
    load_dotenv()


def print_log(res, data):
    print(data, end="")


def remote_reconstruction():
    from szrpc.client import Client
    szrpc_address = f"tcp://{os.getenv('SZRPC_HOST')}:{os.getenv('SZRPC_PORT')}"
    logger.debug(f"Connecting to {szrpc_address}")
    client = Client(szrpc_address)
    # wait for client to be ready before sending commands
    while not client.is_ready():
        time.sleep(.001)
    logger.debug("Connected to dpserver")
    output_dir = Path(EZVARS['inout']['output-dir']['value'])
    output_dir.mkdir(exist_ok=True, parents=True)
    param_path = output_dir / "tofuez_remote.yaml"
    export_values(param_path, ['ezvars', 'tofu', 'ezvars_aux'])
    result = client.single(ezvars=str(param_path))
    result.connect('update', print_log)
    result.wait()
    for line in reversed(result.results):
        if line.startswith("*** Processed "):
            return line.split()[2]


def get_execute():
    if os.getenv('SZRPC_HOST') and os.getenv('SZRPC_PORT'):
        logger.info("Using remote reconstruction")
        return remote_reconstruction
    else:
        logger.info("Using local reconstruction")
        return execute_reconstruction

