import logging

# Inits logger
logging.basicConfig(filename='logs.log', level=logging.DEBUG)


def errorLog(message):
    logging.error(message)


def debugLog(message):
    logging.debug(message)


def warningLog(message):
    logging.warn(message)


def infoLog(message):
    logging.info(message)
