#!python3
import sys
import select
import paramiko
import socketserver
from optparse import OptionParser


# TODO
# Inspired and some code reused from https://github.com/paramiko/paramiko/blob/main/demos/forward.py
DEFAULT_DEST_PORT = "22"


class ForwardServer(socketserver.ThreadingTCPServer):
    daemon_threads = True
    allow_reuse_address = True


class RequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            channel = self.ssh_transport.open_channel(
                "direct-tcpip",
                (self.chain_host, self.chain_port),
                self.request.getpeername(),
            )
        except Exception as e:
            print("Incoming Request Failed!")
            print(f"Source: {self.chain_host}:{self.chain_port}, Exception: {repr(e)}")
            return
        if channel is None:
            print("Incoming Request was rejected!")
            print(f"Source: {self.chain_host}:{self.chain_port}")
            return
        while True:
            r, w, x = select.select([self.request, channel], [], [])
            if self.request in r:
                data = self.request.recv(1024)
                if len(data) == 0:
                    break
                channel.send(data)
            if channel in r:
                data = channel.recv(1024)
                if len(data) == 0:
                    break
                self.request.send(data)

        peername = self.request.getpeername()
        channel.close()
        self.request.close()

def fwd_handler(src_port, dest_host, dest_port, transport):
    class ReqHandler(RequestHandler):
        chain_host = dest_host
        chain_port = dest_port
        ssh_transport = transport

    ForwardServer(("", src_port), ReqHandler).serve_forever()


def parse_options():
    help_msg = (f"Usage: {sys.argv[0]} [-h|--help] [-g|--grey|--gray] [-c|--compact] [-d|--decimal]\n"
                "-h, --help\t\tShow this help.\n"
                "")
    for i in range(1, len(sys.argv)):
        if (sys.argv[i] == "-h") | (sys.argv[i] == "--help"):
            print(help_msg)
            exit(0)
    parser = OptionParser(usage=help_msg)  # TODO
    parser.add_option(
        "-D", "--dest", action="store", type="string", dest="dest_host",
        help="Destination Host Address (and Port, default is 22)"
    )
    parser.add_option(
        "-P", "--port", action="store", type="int", dest="local_port",
        help="Local Listening Port"
    )
    parser.add_option(
        "-K", "--key", action="store", type="string", dest="key_file",
        help="SSH Key File"
    )
    options, args = parser.parse_args()
    dest_host_port = (options.dest_host.split(":", 1) + [DEFAULT_DEST_PORT])[:2]
    destination_host = dest_host_port[0]
    destination_port = int(dest_host_port[1])
    return destination_host, destination_port, options.local_port, options.key_file


hostname = ""
local_port = 22
port = 22
key_file = ""


def main():
    print("==== SSH Tunnel Forward Tool ====")
    dest_host, dest_port, income_port, key_filename = parse_options()

    src_server = ('127.0.0.1', local_port)
    client = paramiko.SSHClient()
    try:
        client.connect(
            hostname=dest_host,
            port=dest_port,
            username="test",
            key_filename=key_filename,
            look_for_keys=True
        )
    except Exception as e:
        print("Cannot connect to destination server!")
        print(f"Error :{repr(e)}")

    try:
        fwd_handler('127.0.0.1', 22, 22, client.get_transport())  # tmp values
    except KeyboardInterrupt:
        print("Server Connection Stopped.")
        sys.exit(0)


if __name__ == "__main__":
    main()
