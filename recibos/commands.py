#!/usr/bin/env python
# -*- coding: utf8 -*-
#
# Copyright © 2008 - 2012 Carlos Flores <cafg10@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

"""This module contains functions to be called from console script entry points.
"""

# symbols which are imported by "from turboaffiliate.command import *"
__all__ = ['bootstrap', 'ConfigurationError', 'start']

import optparse
import sys
from os import getcwd
from os.path import dirname, exists, join

import pkg_resources

try:
    pkg_resources.require("TurboGears>=1.5")
except pkg_resources.DistributionNotFound:
    print("""\
This is a TurboGears (http://www.turbogears.org) application. It seems that
you either don't have TurboGears installed or it can not be found.

Please check if your PYTHONPATH is set correctly. To install TurboGears, go to
http://docs.turbogears.org/Install and follow the instructions there. If you
are stuck, visit http://docs.turbogears.org/GettingHelp for support options.""")
    sys.exit(1)
try:
    pkg_resources.require("SQLAlchemy>=0.6.0")
except pkg_resources.DistributionNotFound:
    from turbogears.util import missing_dependency_error

    print(missing_dependency_error('SQLAlchemy'))
    sys.exit(1)

import cherrypy
import turbogears

cherrypy.lowercase_api = True


class ConfigurationError(Exception):
    pass


def _read_config(args):
    """Read deployment configuration file.
	
    First looks on the command line for a desired config file, if it's not on
    the command line, then looks for 'setup.py' in the parent of the directory
    where this module is located.
	
    If 'setup.py' is there, assumes that the application is started from
    the project directory and should run in development mode and so loads the
    configuration from a file called 'dev.cfg' in the current directory.
	
    If 'setup.py' is not there, the project is probably installed and the code
    looks first for a file called 'prod.cfg' in the current directory and, if
    this isn't found either, for a default config file called 'default.cfg'
    packaged in the egg.
	
    """
    setupdir = dirname(dirname(__file__))
    curdir = getcwd()

    if args:
        configfile = args[0]
    elif exists(join(setupdir, "setup.py")):
        configfile = join(setupdir, "dev.cfg")
    elif exists(join(curdir, "prod.cfg")):
        configfile = join(curdir, "prod.cfg")
    else:
        try:
            configfile = pkg_resources.resource_filename(
                pkg_resources.Requirement.parse("recibos"),
                "config/default.cfg")
        except pkg_resources.DistributionNotFound:
            raise ConfigurationError("Could not find default configuration.")

    turbogears.update_config(configfile=configfile,
                             modulename="recibos.config")


def bootstrap():
    """Example function for loading bootstrap data into the database
	
    You can adapt this to your needs to e.g. accept more options or to
    run more functions for bootstrapping other parts of your application.
    By default this runs the function 'turboaffiliate.model.bootstrap_model', which
    creates all database tables and optionally adds a user.
	
    The following line in your project's 'setup.py' file takes care of
    installing a command line script when you install your application via
    easy_install which will run this function:
	
        'bootstrap-recibos = recibos.command:bootstrap',
	
    """

    optparser = optparse.OptionParser(usage="%prog [options] [config-file]",
                                      description="Load bootstrap data into the database defined in "
                                                  "config-file.", version="1.0")
    optparser.add_option('-C', '--clean', dest="clean", action="store_true",
                         help="Purge all data in the database before loading the bootrap data.")
    optparser.add_option('-u', '--user', dest="user", metavar="USERNAME",
                         help="Create a default user USERNAME (prompts for password).")
    options, args = optparser.parse_args()
    if options.user:
        options.user = options.user.decode(sys.getfilesystemencoding())
    _read_config(args)
    # from turboaffiliate.model import bootstrap_model
    # bootstrap_model(options.clean, options.user)


def start():
    """Start the CherryPy application server."""

    _read_config(sys.argv[1:])

    from recibos.controllers import root
    return turbogears.start_server(root.Root())
