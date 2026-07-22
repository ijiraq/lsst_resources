# This file is part of lsst-resources.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# Use of this source code is governed by a 3-clause BSD-style
# license that can be found in the LICENSE file.

"""Support for authenticated direct datastore reads via `HttpResourcePath`."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .http import HttpResourcePath

# Attribute name stored on HttpResourcePath instances that represent artifact
# URLs returned by a remote-butler server with ``auth="datastore"``.
DATASTORE_AUTHENTICATED_ATTR = "_cadc_datastore_access"


def mark_datastore_authenticated_path(path: HttpResourcePath) -> None:
    """Mark ``path`` as requiring direct authenticated GET (no WebDAV probe).

    Remote-butler clients set this when converting server-provided artifact
    URLs that use ``auth_mode == "datastore"``. CADC storage endpoints reject
    WebDAV ``OPTIONS`` requests against the server root but accept direct
    ``GET`` requests to artifact URLs with bearer-token headers.

    Parameters
    ----------
    path : `httpResourcePath`
         Path element to update attributes of.
    """
    setattr(path, DATASTORE_AUTHENTICATED_ATTR, True)
    path._is_webdav = False
    path._server = None


def uses_datastore_authentication(path: HttpResourcePath) -> bool:
    """Return `True` if ``path`` is a direct authenticated datastore read.

    Parameters
    ----------
    path : `httpResourcePath`
         Path to check for CADC datastore auth usage.
    """
    return bool(getattr(path, DATASTORE_AUTHENTICATED_ATTR, False))
