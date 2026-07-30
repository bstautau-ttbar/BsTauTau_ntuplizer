# -*- coding: utf-8 -*-

class color_text:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def print_error(message, logger=None):
    print("{}[ERROR]{} {}".format(color_text.RED, color_text.END, message))
    if logger:
        logger.write(message + '\n')


def print_warning(message, logger=None):
    print("{}[WARNING]{} {}".format(color_text.YELLOW, color_text.END, message))
    if logger:
        logger.write(message + '\n')


def print_info(message, logger=None):
    print("{}[INFO]{} {}".format(color_text.BLUE, color_text.END, message))
    if logger:
        logger.write(message + '\n')


def print_success(message, logger=None):
    print("{}[DONE!]{} {}".format(color_text.GREEN, color_text.END, message))
    if logger:
        logger.write(message + '\n')


def print_bold(message, logger=None):
    print("{}{}{}".format(color_text.BOLD, message, color_text.END))
    if logger:
        logger.write(message + '\n')


def print_addition(message, logger=None):
    print("{}[+]{} {}".format(color_text.BOLD, color_text.END, message))
    if logger:
        logger.write(message + '\n')

def print_exe(message, logger=None):
    print("{}[EXE]{} {}".format(color_text.CYAN, color_text.END, message))
    if logger:
        logger.write(message + '\n')