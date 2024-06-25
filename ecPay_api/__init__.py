import logging
from pathlib import Path
import importlib.util
from database_for_bot import CassandraDB

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
WORKDIR = Path(__file__).parent.absolute()
spec = importlib.util.spec_from_file_location(
    "ecpay_payment_sdk", WORKDIR / "sdk/ecpay_payment_sdk.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
