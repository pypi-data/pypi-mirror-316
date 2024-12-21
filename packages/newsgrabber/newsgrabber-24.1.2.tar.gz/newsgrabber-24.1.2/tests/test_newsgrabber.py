# Copyright (C) 2024 Ahmet Yiğit Budak (https://github.com/yibudak)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
from unittest.mock import Mock

from newsgrabber import NetworkManager, NewsGrabber


def test__str__():
    ng = NewsGrabber("https://example.com/sitemap.xml")
    assert str(ng) == "NewsGrabber: example.com"


def test__repr__():
    ng = NewsGrabber("https://example.com/sitemap.xml")
    assert repr(ng) == "NewsGrabber[example.com]"


def test__get_domain_name():
    ng = NewsGrabber("https://example.com/sitemap.xml")
    assert ng._get_domain_name() == "example.com"


def test__build_network_manager():
    # Without any extra parameters
    ng = NewsGrabber("https://example.com/sitemap.xml")
    network_manager = NetworkManager()
    assert ng.network_manager.session.proxies == network_manager.session.proxies
    assert ng.network_manager.timeout == network_manager.timeout

    # With Proxy Dict
    proxy_dict = {"http": "socks5://127.0.0.1:1080", "https": "socks5://127.0.0.1:1080"}
    ng = NewsGrabber("https://example.com/sitemap.xml", proxy=proxy_dict)
    network_manager = NetworkManager(proxy=proxy_dict)
    assert ng.network_manager.session.proxies == network_manager.session.proxies
    assert ng.network_manager.timeout == network_manager.timeout

    # With Timeout Parameter
    timeout = 30
    ng = NewsGrabber("https://example.com/sitemap.xml", timeout=timeout)
    network_manager = NetworkManager(timeout=timeout)
    assert ng.network_manager.timeout == network_manager.timeout


def test_parse():
    ng = NewsGrabber("https://example.com/sitemap.xml")
    # Get all test files
    test_file_path = "tests/test_xml_files"
    test_files = os.listdir(test_file_path)

    for _ in test_files:
        test_file = open(os.path.join(test_file_path, _), "rb")
        ng.network_manager.fetch_sitemap = Mock(return_value=test_file.read())
        assert ng.parse()
