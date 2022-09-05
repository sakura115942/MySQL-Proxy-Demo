import socket
import logging
import sys

import mysql.connector


logging.basicConfig(level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S',
                    format='[%(asctime)s] [%(levelname)s] %(message)s')

file_handler = logging.FileHandler('test.log', 'a', encoding='utf-8')
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
file_handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(file_handler)

DB_HOST = '192.168.2.110'
DB_PORT = 3306
DB_USER = 'root'
DB_PWD = '123456'

db = mysql.connector.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PWD)
cursor = db.cursor()

LOCAL_HOST = socket.gethostname()
LOCAL_PORT = 33060


def send(conn, content):
    if isinstance(content, str):
        content = content.encode()
    conn.sendall(content)
    return len(content)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((LOCAL_HOST, LOCAL_PORT))
    s.listen()
    logger.info("MySQL proxy server start ...")
    while True:
        conn, addr = s.accept()
        nrecv_bytes = 0
        nsend_bytes = 0
        with conn:
            logger.info(f"Connected by {addr}")
            while True:
                _message = conn.recv(1024)
                nrecv_bytes += len(_message)
                message = _message.decode()

                if message.lower().strip() == 'quit':
                    nsend_bytes += send(conn, 'Bye')
                    logger.info(f"{addr} exited")
                    logger.info(f"{addr} send {nsend_bytes} bytes, receive {nrecv_bytes} bytes")
                    break
                elif message is not None:
                    logger.info(message)
                    try:
                        cursor.execute(message)
                        data = cursor.fetchall()
                        logger.info(data)
                        nsend_bytes += send(conn, str(data))
                    except Exception as e:
                        logger.error(str(e))
                        nsend_bytes += send(conn, str(e))
                else:
                    pass
            