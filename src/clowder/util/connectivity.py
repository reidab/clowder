# -*- coding: utf-8 -*-
"""Network connectivity

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""


import socket

import clowder.util.formatting as fmt
from clowder.error.clowder_exit import ClowderExit


def is_offline(host='8.8.8.8', port=53, timeout=3):
    """Returns True if offline, False otherwise

    Service: domain (DNS/TCP)

    .. note:: Implementation source https://stackoverflow.com/a/33117579

    :param str host: Host to check. Default is 8.8.8.8 (google-public-dns-a.google.com)
    :param int port: Port number. Default is 53/tcp
    :param int timeout: Seconds to wait until timeout
    :return: True, if offline
    :rtype: bool
    :raise ClowderExit:
    """

    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return False
    except socket.error:
        return True
    except (KeyboardInterrupt, SystemExit):
        raise ClowderExit(1)


def network_connection_required(func):
    """If no network connection, print offline message and exit"""

    def wrapper(*args, **kwargs):
        """Wrapper

        :raise ClowderExit:
        """

        if is_offline():
            print(fmt.offline_error())
            raise ClowderExit(1)
        return func(*args, **kwargs)

    return wrapper
