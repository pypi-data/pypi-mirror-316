import os
import builtins
import io
import socket
import select
from collections import deque

from . import DEFAULT_TIMEOUT, DEFAULT_SOCK_PATH

BUFSIZE = 4096
FILE_OK = b"OK"
GOODBYE = b"BYE"
ROTATED = b"ROTATED"

def _make_exception(response):
    # Generate an exception object from a response from the server. Or return None if no
    # response
    try:
        exc_class_name, message = response.decode('utf8').split(': ', 1)
        exc_class = getattr(builtins, exc_class_name, ValueError)
    except ValueError:
        exc_class = ValueError
        message = response
    return exc_class(message)


class _ByteQueue:
    """Class to queue unsent data. Stores data in a dequeue of BytesIO objects
    containing up to BUFSIZE bytes each. All interior elements have exactly BUFSIZE
    bytes each, but the first and last elements may have fewer. Idea is to call put() to
    queue unsent data, to call peek() to get a chunk of data to be sent from the queue
    without removing, and then to report how many bytes were successfully sent by
    calling done(n), which clears the last n bytes from the queue. len() returns the
    length of the queue in bytes."""

    def __init__(self):
        self.q = deque()

    def __len__(self):
        qlen = len(self.q)
        if not qlen:
            return 0
        n = self.q[0].getbuffer().nbytes
        if qlen > 1:
            n += self.q[-1].getbuffer().nbytes
        if qlen > 2:
            n += BUFSIZE * (qlen - 2)
        return n

    def put(self, data):
        """Append data to the back of the queue"""
        if self:  # non-empty
            curr_chunk_nbytes_avail = BUFSIZE - self.q[-1].getbuffer().nbytes
            if curr_chunk_nbytes_avail:
                self.q[-1].write(data[:curr_chunk_nbytes_avail])
                data = data[curr_chunk_nbytes_avail:]
        while data:
            chunk = io.BytesIO()
            chunk.write(data[:BUFSIZE])
            self.q.append(chunk)
            data = data[BUFSIZE:]

    def peek(self):
        """Get up to BUFSIZE bytes from the front of the queue without removing them"""
        return self.q[0].getvalue()

    def done(self, n):
        """Remove nbytes from the front of the queue"""
        if not n:
            return
        chunk = self.q.popleft()
        if n < chunk.getbuffer().nbytes:
            newchunk = io.BytesIO()
            newchunk.write(chunk.getvalue()[n:])
            self.q.appendleft(newchunk)


class ProxyFile:
    """Object to proxy appending file writes via a running offlog server"""

    def __init__(
        self,
        filepath,
        sock_path=DEFAULT_SOCK_PATH,
        timeout=DEFAULT_TIMEOUT,
        block_open=True,
    ):
        self.timeout = timeout
        self.sock_path = sock_path
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.setblocking(0)
        self.poller = select.epoll()
        self.poller.register(self.sock, select.EPOLLIN)
        self._recv_buf = io.BytesIO()
        self._sendqueue = _ByteQueue()
        self._connect()
        self._open(filepath, block=block_open)
        self._rotated = False

    def _connect(self):
        try:
            self.sock.connect(self.sock_path)
        except FileNotFoundError:
            self.sock.close()
            emsg = f"server socket {self.sock_path} not found"
            raise FileNotFoundError(emsg) from None
        except PermissionError:
            self.sock.close()
            raise

    def _recv_msg(self, timeout=None):
        # recv until null byte. If timeout or EOF, raise but leave data read so far in
        # self._recv_buf.
        if timeout is None:
            timeout = self.timeout
        while self.poller.poll(timeout):
            try:
                data = self.sock.recv(BUFSIZE)
            except ConnectionResetError:
                self.sock.close()
                raise
            msg, null, extradata = data.partition(b'\0')
            self._recv_buf.write(msg)
            if not data:
                self.sock.close()
                raise EOFError
            if null:
                msg = self._recv_buf.getvalue()
                self._recv_buf = io.BytesIO()
                self._recv_buf.write(extradata)
                return msg
        self.sock.close()
        raise TimeoutError("no response from server")

    def _open(self, filepath, block=True):
        filepath = os.fsencode(filepath)
        if b'\0' in filepath:
            self.sock.close()
            raise ValueError("embedded null byte in filepath")
        self.write(os.path.abspath(filepath) + b'\0')
        # Check for errors now if block=True, otherwise error responses will be received
        # and raised later when client attempts to write
        if block:
            response = self._recv_msg()
            if response != FILE_OK:
                self.sock.close()
                raise _make_exception(response)

    def check_rotated(self):
        """Return whether the server has sent us a message indicating the underlying
        file was moved/renamed/deleted"""
        self._checkrecv()
        return self._rotated

    def _checkrecv(self, timeout=0):
        """Check if the server has sent us any messages. If it has sent a notification
        that the file was rotated, set self._rotated=True. If it's an error, raise it."""
        while self.poller.poll(0):
            # No possibility of getting a partial message (and therefore TimeoutError)
            # because all messages the server sends are smaller than PIPE_BUF and
            # therefore sent atomically
            msg = self._recv_msg(timeout=0)
            if msg == FILE_OK:
                # indicates sucessful file open, not previously read due to nonblocking
                # _open(). ignore.
                continue
            elif msg == ROTATED:
                self._rotated = True
            else:
                # An error, raise it
                self.sock.close()
                raise _make_exception(msg) from None

    def _checksend(self, data):
        """Send data and return number of bytes sent. If the server has closed the
        socket and sent us an error message, raise it."""
        try:
            return self.sock.send(data)
        except BrokenPipeError:
            self._checkrecv()
            raise # reraise if no error was raised by _checkrecv()
        except ConnectionResetError:
            self.sock.close()
            raise

    def _retry_queued(self):
        """Retry sending as much previously queued data as we can without blocking. On
        BrokenPipeError, check if the server sent us an error and raise it if so."""
        try:
            while self._sendqueue:  # while it's non-empty:
                sent = self._checksend(self._sendqueue.peek())
                self._sendqueue.done(sent)
        except BlockingIOError:
            pass
        except ConnectionResetError:
            self.sock.close()
            raise

    def write(self, data):
        """Send as much as we can without blocking. If sending would block, queue unsent
        data for later. On BrokenPipeError, check if the server sent us an error and
        raise it if so. This method will always attempt to re-send previously-queued
        data before attempting to send new data."""

        if not isinstance(data, bytes):
            data = data.encode('utf8')

        # Retry previously-queued data:
        self._retry_queued()
        try:
            # Try sending new data:
            while data:
                sent = self._checksend(data)
                data = data[sent:]
        except BlockingIOError:
            # Queue unsent data for later
            self._sendqueue.put(data)

    def close(self, block_send=True, block_close=True):
        """Close the socket. Attempt to send all queued unsent data to the server and
        cleanly close the connection to it, raising exceptions if anything goes wrong.
        
        If block_send=True, block for up to self.timeout ms sending unsent data to the
        server, otherwise only send data that can be sent without blocking.

        if block_close=True then wait for a response from the server to confirm all
        previously-sent data was written, and that the file was closed.

        block_send=True and block_close=False is a reasonable arrangement to prevent the
        application blocking due to slow file IO on a small amount of data, whilst
        accepting that it may block if there is so much data that the unix socket's
        buffer is full. This may be useful if the application is closing and reopening
        the file for log rolling purposes (in which case you'd like this to be
        non-blocking unless something is very wrong), wheras at application shutdown you
        probably want block_send=True, block_close=True"""
        if self.sock.fileno() == -1:
            return
        try:
            # Attempt to flush unsent data:
            poller = select.epoll()
            poller.register(self.sock, select.EPOLLOUT)
            if block_send:
                while self._sendqueue:
                    if poller.poll(self.timeout):
                        self._retry_queued()
                    else:
                        raise TimeoutError(
                        "timed out flushing unsent data on close(). "
                        + f"{len(self._sendqueue)} bytes not sent."
                    )
            else:
                self._retry_queued()
            self.sock.shutdown(socket.SHUT_WR)
            if block_close:
                while True:
                    response = self._recv_msg()
                    if response == GOODBYE:
                        return
                    elif response not in [FILE_OK, ROTATED]:
                        raise _make_exception(response)
        finally:
            self.sock.close()

    def __del__(self):
        self.close()
