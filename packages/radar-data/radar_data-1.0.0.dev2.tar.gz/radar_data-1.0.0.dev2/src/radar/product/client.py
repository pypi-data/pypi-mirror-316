import json
import atexit
import pickle
import socket
import threading

from .share import *
from ..cosmetics import colorize, pretty_object_name

logger = None


class Client(Manager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = colorize("Client", "green")
        self._host = kwargs.get("host", "localhost")
        self._i = 0
        global logger
        logger = self.logger
        # Wire things up
        self.sockets = []
        self.connectThread = threading.Thread(target=self._connect, daemon=True)
        self.connectThread.start()
        while self.wantActive and len(self.sockets) < self.count:
            time.sleep(0.1)
        atexit.register(self.cleanup)

    def __del__(self):
        self.close()

    def cleanup(self):
        self.stop()

    def _getSocketAndLock(self):
        with self.lock:
            i = self._i
            self._i = (i + 1) % self.count
        sock = self.sockets[i]
        lock = self.clientLocks[i]
        return sock, lock

    def _connect(self):
        myname = colorize("Client.connect", "green")
        while self.wantActive:
            logger.info(f"{myname} Connecting to {self._host}:{self._port} ...")
            with self.lock:
                # Make n connections
                self._i = 0
                self.sockets = []
                for _ in range(self.count):
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    logger.debug(f"{myname} socket[{sock.fileno()}] connecting ...")
                    try:
                        sock.settimeout(2.5)
                        sock.connect((self._host, self._port))
                    except ConnectionRefusedError:
                        logger.info(f"{myname} Connection refused ...")
                        break
                    except:
                        logger.warning(f"{myname} Unexpected error ...")
                        break
                    self.sockets.append(sock)
            if len(self.sockets) != self.count:
                logger.info(f"{myname} Only {len(self.sockets)} out of {self.count} connections")
                for sock in self.sockets:
                    sock.close()
                self._shallow_sleep(2.5)
                continue
            # Keep running until told to stop
            ping = 0
            while self.wantActive:
                for sock, lock in zip(self.sockets, self.clientLocks):
                    k = sock.fileno()
                    with lock:
                        sock.settimeout(2.5)
                        if self.verbose > 2:
                            logger.debug(f"{myname} sockets[{k}] ping[{ping}] ...")
                        try:
                            send(sock, json.dumps({"ping": ping}).encode())
                        except BrokenPipeError:
                            pong = None
                            break
                        except:
                            logger.warning(f"{myname} socket[{k}] unexpected error during ping.send()")
                            pong = None
                            break
                        try:
                            pong = recv(sock)
                        except ConnectionResetError:
                            pong = None
                        except:
                            logger.warning(f"{myname} sockets[{k}] unexpected error during ping.recv()")
                            pong = None
                    if pong is None:
                        logger.info(f"{myname} sockets[{k}] server not available")
                        break
                if pong is None:
                    break
                self._shallow_sleep(10.0)
                ping += 1
            for sock in self.sockets:
                sock.close()

    def get(self, path, tarinfo=None, want_tarinfo=False):
        if self.sockets == []:
            logger.info(f"{self.name} Not connected")
            return None
        sock, lock = self._getSocketAndLock()
        with lock:
            sock.settimeout(5.0)
            try:
                send(sock, json.dumps({"path": path, "tarinfo": tarinfo}).encode())
                info = recv(sock)
            except BrokenPipeError:
                myname = pretty_object_name("Client.get", sock.fileno())
                logger.warning(f"{myname} BrokenPipeError")
                info = None
        if info is None:
            myname = pretty_object_name("Client.get", sock.fileno())
            logger.error(f"{myname} Server not available")
            self.wakeUp = True
            return None
        output = pickle.loads(info)
        data, new_tarinfo = output["data"], output["tarinfo"]
        if want_tarinfo:
            return data, new_tarinfo
        return data

    def stats(self):
        if self.sockets == []:
            logger.info(f"{self.name} Not connected")
            return None
        sock, lock = self._getSocketAndLock()
        with lock:
            sock.settimeout(5.0)
            send(sock, json.dumps({"stats": 1}).encode())
            message = recv(sock)
            if message is None:
                myname = colorize("Client.stats()", "green")
                logger.error(f"{myname} No message")
                return None
        return message.decode("utf-8")

    def custom(self, command, **kwargs):
        if self.sockets == []:
            logger.info(f"{self.name} Not connected")
            return None
        sock, lock = self._getSocketAndLock()
        with lock:
            sock.settimeout(5.0)
            payload = json.dumps({"custom": command, **kwargs}).encode()
            send(sock, payload)
            message = recv(sock)
            if command == "list":
                message = json.loads(message)
        return message

    def close(self):
        self.wantActive = False
        self.connectThread.join()
