"""HTTP client request generator"""
import http.client
import socket
import os
import sys
import logging
import time
from config import config

def init_logger():
    """Initial logger to console and if configured to a logfile."""
    logger = logging.getLogger(config["logger_name"])
    logger.setLevel(config["log_level"])
    formatter = logging.Formatter(config["log_format"])

    if config["logfile"]:
        logger.addHandler(make_filehandler(config["logfile"], formatter))
    # always log to console
    logger.addHandler(make_consolehandler(formatter))

    return logger
    

def  make_filehandler(logfile, formatter, level=logging.DEBUG):
    """Return a logging filehandler"""
    fh = logging.FileHandler(logfile)
    fh.setLevel(level)
    fh.setFormatter(formatter)
    return fh


def make_consolehandler(formatter, level=logging.INFO):
    """Return a console logging handler."""
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(formatter)
    return ch

def get_connection(server=config['server'],
                    port=config['port'],
                    srv_path=config['srv_path'],
                    logger=None):
    conn = http.client.HTTPConnection(server, port)
    connected = False
    while (not connected):
        try:
            if logger:
                logger.info("Address info for {} {}".format(server, socket.getaddrinfo(server, port)))
            else:
                print("Address info for {} {}".format(server, socket.getaddrinfo(server, port)))
            conn.request("GET", srv_path)
            connected = True
        except socket.gaierror as e:
            if logger:
                logger.error("Initial connection caught {}; retrying.".format(e))
            else:
                print("Initial connection caught {}; retrying.".format(e))
            time.sleep(5)
    return conn
                
def send(server = 'localhost', port = 8080, srv_path = '/'):
    """Send requests endlessly"""
    logger.info("Connecting to http://{}:{}{}".format(server, port, srv_path))
    headers = {
        'User-Agent': 'Request-generator 0.2'
    }
    connected = False
    conn = http.client.HTTPConnection(server, port)
    while (not connected):
        try:
            logger.info("Address info for {} {}".format(server, socket.getaddrinfo(server, port)))
            conn.request("GET", srv_path, headers=headers)
            connected = True
        except socket.gaierror as e:
            logger.error("Initial connection caught {}; retrying.".format(e))
            time.sleep(5)
    resp = conn.getresponse()
    count = 1
    t0 = time.time() # Set start time
    t1 = t0

    logger.info("Starting endless loop")
    while (200 == resp.status):
        try:
            conn.request("GET", srv_path, headers=headers)
            resp = conn.getresponse()
            count += 1
            if (0 == count % 1000):
                t = time.time()
                logger.info("Send {} requests with {} req/s".format(count, round(1000/(t - t1),3)))
                t1 = t
                if ( 0 == count % 10000):
                    logger.info("Send {} requests in {} seconds with an average of {} req/s".format(count, round(t - t0,3), round(count/(t - t0),3)))
        
        except socket.gaierror as e:
            logger.error("Caught socket gaierror {} going to retry".format(e))
        except socket.timeout:
            logger.error("Caught socket timeout. Going to retry now.")
            conn = http.client.HTTPConnection(server, port)
        except http.client.NotConnected as e:
            logger.error("Caught socket timeout. Going to retry now.")
            conn = http.client.HTTPConnection(server, port) 
        except Exception as e:
            logger.error("Unknown exception, trying to reconnect {}".format(e))
            conn = http.client.HTTPConnection(server, port)


if __name__ == "__main__":
    logger = init_logger()
    try:
        send(config["server"], config["port"], config["srv_path"])
    except KeyboardInterrupt:
        logger.info("Stopped by keyboard interrupt")
        pass