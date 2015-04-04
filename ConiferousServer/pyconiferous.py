# -*- coding: UTF-8 -*-

__author__ = 'yangtianhang'

import argparse
import logging

from thrift.transport import TSocket
from thrift.server import TNonblockingServer

from Coniferous import Coniferous
from Coniferous.ttypes import *
from idworker import IdWorker


DEBUG_LEVELS = {
    "ERROR": logging.ERROR,
    "WARN": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG
}


def get_log_level(debug_level_string):
    d = debug_level_string.upper()
    if d in DEBUG_LEVELS:
        return DEBUG_LEVELS[d]

    return logging.INFO


def run(args):
    log_level = get_log_level(args.log_level)

    logger = logging.getLogger()
    logger.setLevel(log_level)
    if args.verbose:
        ch = logging.StreamHandler()
        ch.setLevel(log_level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    logging.info("Starting pyconiferous server %s:%d" % (args.host, args.port))

    handler = IdWorker(args.worker_id, args.data_center_id)
    processor = Coniferous.Processor(handler)
    transport = TSocket.TServerSocket(port=args.port)
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    logging.info("logging level: %s" % args.log_level)
    server = TNonblockingServer.TNonblockingServer(processor, transport, pfactory, threads=1)
    logging.info("RUNNING")
    server.serve()


def main():
    parser = argparse.ArgumentParser(description='Python based Coniferous server')
    parser.add_argument("worker_id", type=int, help="Worker ID")
    parser.add_argument("data_center_id", type=int, help="Data Center ID")
    parser.add_argument("--host", type=str, help="Host address (default 127.0.0.1)", default="127.0.0.1")
    parser.add_argument("--port", type=int, help="port (default 9100)", default=9100)
    parser.add_argument("--log_level", type=str, help="Log level (default: INFO). Values: ERROR,WARN,INFO,DEBUG", default="INFO")
    parser.add_argument("--verbose", help="Be verbose!", action="store_true")

    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()