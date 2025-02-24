# domain management - common code
#
# Copyright Matthias Dieter Wallnoefer 2009
# Copyright Andrew Kroeger 2009
# Copyright Jelmer Vernooij 2007-2012
# Copyright Giampaolo Lauria 2011
# Copyright Matthieu Patou <mat@matws.net> 2011
# Copyright Andrew Bartlett 2008-2015
# Copyright Stefan Metzmacher 2012
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from uuid import UUID

from samba.dsdb import (
    DS_DOMAIN_FUNCTION_2000,
    DS_DOMAIN_FUNCTION_2003,
    DS_DOMAIN_FUNCTION_2008,
    DS_DOMAIN_FUNCTION_2008_R2,
    DS_DOMAIN_FUNCTION_2012,
    DS_DOMAIN_FUNCTION_2012_R2,
    DS_DOMAIN_FUNCTION_2003_MIXED,
    DS_DOMAIN_FUNCTION_2016
)
from samba.netcmd import CommandError, Option
from samba.samdb import get_default_backend_store

common_ntvfs_options = [
    Option("--use-ntvfs", help="Use NTVFS for the fileserver (default = no)",
           action="store_true")
]

common_provision_join_options = [
    Option("--machinepass", type="string", metavar="PASSWORD",
           help="choose machine password (otherwise random)"),
    Option("--plaintext-secrets", action="store_true",
           help="Store secret/sensitive values as plain text on disk" +
           "(default is to encrypt secret/sensitive values)"),
    Option("--backend-store", type="choice", metavar="BACKENDSTORE",
           choices=["tdb", "mdb"],
           help="Specify the database backend to be used "
           "(default is %s)" % get_default_backend_store()),
    Option("--backend-store-size", type="bytes", metavar="SIZE",
           help="Specify the size of the backend database, currently only " +
                "supported by lmdb backends (default is 8 Gb)."),
    Option("--targetdir", metavar="DIR",
           help="Set target directory (where to store provision)", type=str),
    Option("-q", "--quiet", help="Be quiet", action="store_true"),
]

common_join_options = [
    Option("--server", help="DC to join", type=str),
    Option("--site", help="site to join", type=str),
    Option("--domain-critical-only",
           help="only replicate critical domain objects",
           action="store_true"),
    Option("--dns-backend", type="choice", metavar="NAMESERVER-BACKEND",
           choices=["SAMBA_INTERNAL", "BIND9_DLZ", "NONE"],
           help="The DNS server backend. SAMBA_INTERNAL is the builtin name server (default), "
           "BIND9_DLZ uses samba4 AD to store zone information, "
           "NONE skips the DNS setup entirely (this DC will not be a DNS server)",
           default="SAMBA_INTERNAL"),
    Option("-v", "--verbose", help="Be verbose", action="store_true")
]


string_version_to_constant = {
    "2000": DS_DOMAIN_FUNCTION_2000,
    "2003": DS_DOMAIN_FUNCTION_2003,
    "2008": DS_DOMAIN_FUNCTION_2008,
    "2008_R2": DS_DOMAIN_FUNCTION_2008_R2,
    "2012": DS_DOMAIN_FUNCTION_2012,
    "2012_R2": DS_DOMAIN_FUNCTION_2012_R2,
    "2016": DS_DOMAIN_FUNCTION_2016,
}


def string_to_level(string):
    """Interpret a string indicating a functional level."""
    try:
        return string_version_to_constant[string]
    except KeyError as e:
        raise CommandError(f"'{string}' is not a valid domain level")


def level_to_string(level):
    """turn the level enum number into a printable string."""
    if level < DS_DOMAIN_FUNCTION_2000:
        return "invalid"
    strings = {
        DS_DOMAIN_FUNCTION_2000: "2000",
        DS_DOMAIN_FUNCTION_2003_MIXED: \
            "2003 with mixed domains/interim (NT4 DC support)",
        DS_DOMAIN_FUNCTION_2003: "2003",
        DS_DOMAIN_FUNCTION_2008: "2008",
        DS_DOMAIN_FUNCTION_2008_R2: "2008 R2",
        DS_DOMAIN_FUNCTION_2012: "2012",
        DS_DOMAIN_FUNCTION_2012_R2: "2012 R2",
        DS_DOMAIN_FUNCTION_2016: "2016",
    }
    return strings.get(level, "higher than 2016")


def parse_text(value):
    """Parse message element to string value."""
    if value is not None:
        return str(value)


def parse_guid(value):
    """Parse message element containing utf-16 le encoded uuid to string."""
    if value is not None:
        return str(UUID(bytes_le=value[0]))
