#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------------
#                                                                               -
#  Python dual-logging setup (console and log file),                            -
#  supporting different log levels and colorized output                         -
#                                                                               -
#  Created by Fonic <https://github.com/fonic>                                  -
#  Date: 04/05/20 - 02/07/23                                                    -
#                                                                               -
#  Based on:                                                                    -
#  https://stackoverflow.com/a/13733863/1976617                                 -
#  https://uran198.github.io/en/python/2016/07/12/colorful-python-logging.html  -
#  https://en.wikipedia.org/wiki/ANSI_escape_code#Colors                        -
#                                                                               -
# -------------------------------------------------------------------------------
# Imports
import logging
import os
import sys
import ctypes
from logging.handlers import RotatingFileHandler

# Enable ANSI terminal mode for Command Prompt on Microsoft Windows


def windows_enable_ansi_terminal_mode():
    if (sys.platform != "win32"):
        return None
    try:
        kernel32 = ctypes.windll.kernel32
        result = kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        if (result == 0):
            raise Exception
        return True
    except Exception as e:
        logging.exception(f'Error when enableing terminal mode: {e}')
        return False

# Imports

# Logging formatter supporting colorized output


class LogFormatter(logging.Formatter):

    COLOR_CODES = {
        logging.CRITICAL: "\033[1;35m",  # bright/bold magenta
        logging.ERROR: "\033[1;31m",  # bright/bold red
        logging.WARNING: "\033[1;33m",  # bright/bold yellow
        logging.INFO: "\033[0;37m",  # white / light gray
        logging.DEBUG: "\033[1;30m"  # bright/bold black / dark gray
    }

    RESET_CODE = "\033[0m"

    def __init__(self, color, *args, **kwargs):
        super(LogFormatter, self).__init__(*args, **kwargs)
        self.color = color

    def format(self, record, *args, **kwargs):
        if (self.color is True and record.levelno in self.COLOR_CODES):
            record.color_on = self.COLOR_CODES[record.levelno]
            record.color_off = self.RESET_CODE
        else:
            record.color_on = ""
            record.color_off = ""
        return super(LogFormatter, self).format(record, *args, **kwargs)

# Set up logging


def set_up_logging(console_log_output, console_log_level, console_log_color, logfile_file, logfile_log_level, logfile_log_color, warn_file, warn_log_level, warn_log_color, log_line_template):

    # Create logger
    # For simplicity, we use the root logger, i.e. call 'logging.getLogger()'
    # without name argument. This way we can simply use module methods for
    # for logging throughout the script. An alternative would be exporting
    # the logger, i.e. 'global logger; logger = logging.getLogger("<name>")'
    logger = logging.getLogger()

    # Set global log level to 'debug' (required for handler levels to work)
    logger.setLevel(logging.DEBUG)

    # Create console handler
    console_log_output = console_log_output.lower()
    if (console_log_output == "stdout"):
        console_log_output = sys.stdout
    elif (console_log_output == "stderr"):
        console_log_output = sys.stderr
    else:
        logging.error("Failed to set console output: invalid output: '%s'" % console_log_output)
        return False
    console_handler = logging.StreamHandler(console_log_output)

    # Set console log level
    try:
        console_handler.setLevel(console_log_level.upper())  # only accepts uppercase level names
    except Exception:
        logging.exception("Failed to set console log level: invalid level: '%s'" % console_log_level)
        return False

    # Create and set formatter, add console handler to logger
    console_formatter = LogFormatter(fmt=log_line_template, color=console_log_color)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Create log file handler
    maxBytes = 20 * 1024 * 1024
    backupCount = 20

    try:
        logfile_handler = RotatingFileHandler(logfile_file, maxBytes=maxBytes, backupCount=backupCount, encoding='utf-8')
    except Exception as exception:
        logging.exception("Failed to set up log file: %s" % str(exception))
        return False

    # Set log file log level
    try:
        logfile_handler.setLevel(logfile_log_level.upper())  # only accepts uppercase level names
    except Exception:
        logging.exception("Failed to set log file log level: invalid level: '%s'" % logfile_log_level)
        return False

    # Create and set formatter, add log file handler to logger
    logfile_formatter = LogFormatter(fmt=log_line_template, color=logfile_log_color)
    logfile_handler.setFormatter(logfile_formatter)
    logger.addHandler(logfile_handler)

    # Create log file handler
    try:
        warn_handler = RotatingFileHandler(warn_file, maxBytes=maxBytes, backupCount=backupCount, encoding='utf-8')
    except Exception as exception:
        logging.exception("Failed to set up log file: %s" % str(exception))
        return False

    # Set log file log level
    try:
        warn_handler.setLevel(warn_log_level.upper())  # only accepts uppercase level names
    except Exception:
        logging.exception("Failed to set log file log level: invalid level: '%s'" % warn_log_level)
        return False

    # Create and set formatter, add log file handler to logger
    warn_formatter = LogFormatter(fmt=log_line_template, color=warn_log_color)
    warn_handler.setFormatter(warn_formatter)
    logger.addHandler(warn_handler)

    # Success
    return True

# Main function


def main():

    # Set up logging
    script_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if (not set_up_logging(console_log_output="stdout", console_log_level="info", console_log_color=True,
                           logfile_file=script_name + ".log", logfile_log_level="debug", logfile_log_color=False,
                           warn_file=script_name + "warn.log", warn_log_level="warning", warn_log_color=False,
                           log_line_template="%(color_on)s[%(asctime)s] [%(threadName)s] [%(levelname)-8s] %(message)s%(color_off)s")):
        logging.error("Failed to set up logging, aborting.")
        return 1

    # Log some messages
    logging.debug("Debug message")
    logging.info("Info message")
    logging.warning("Warning message")
    logging.error("Error message")
    logging.critical("Critical message")


# Call main function
if (__name__ == "__main__"):
    sys.exit(main())
