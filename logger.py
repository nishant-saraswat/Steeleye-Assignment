"""
@author: Nishant Saraswat

Module for creating logger and initializing logging file directory
"""

import os
import logging
from datetime import datetime

# Creating directory to store log
if not os.path.exists("run_logs"):
    os.mkdir("run_logs")

# Format for logging
formatter = "%(asctime)s : %(levelname)s : %(module)s : %(funcName)s "\
            ": %(message)s"

# Setting up logger
logging.basicConfig(
    format=formatter,
    level=logging.INFO,
    filename=os.path.join(os.getcwd(), "run_logs/process_logs{0}.log".format(
        datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p"))),
    filemode="a",
)

log = logging.getLogger()
