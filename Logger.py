import logging
import sys
import os
import fnmatch
import argparse

logger = logging.getLogger()
# Logger initializing
def init(logfile, debuLvl):
    logging.basicConfig(filename=logfile,
                        format='%(asctime)s %(levelname)s %(funcName)s %(message)s',
                        filemode='a')

    global logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.debug("Start Logging ###########")