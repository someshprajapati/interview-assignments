# --------------------------------------
# Script for basic utility functions
# Author: Somesh Kumar Prajapati
# --------------------------------------

import logging
import os
import sys
import subprocess
import datetime

fmt_str = '%(message)s'
logging.basicConfig(level=logging.DEBUG, format=fmt_str)
logger = logging.getLogger(__name__)


def exec_cmd_return_output(command_to_execute, dry_run=False):
    """
    Function to execute a shell command
    :return: Output of the command
    """

    if not command_to_execute or len(command_to_execute.strip()) == 0:
        logger.error("Please pass the command to execute")
        return False

    if dry_run:
        print_msg(command_to_execute, skip_format=True)
        return True

    try:
        cmd_output = subprocess.Popen(
            command_to_execute,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True)
        stdout, stderr = cmd_output.communicate()

        if stderr:
            logger.error("Error occured while executing the command, Error is: {} ".format(stderr))
            return stderr
        return stdout
    except Exception as e:
        logger.error("Exception occured while executing the command, Exception is : {} ".format(e))
        return False


def print_msg(msg, skip_format=False):
    """
    Function to print message in formatted way
    """
    if skip_format:
        logger.info(msg)
        return

    logger.info("")
    logger.info("#===================================================================================")
    logger.info("# " + current_time() + " ==>  " + msg)
    logger.info("#===================================================================================")
    logger.info("")


def current_time():
    """
    Function to check current time
    """
    ctime = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    return ctime