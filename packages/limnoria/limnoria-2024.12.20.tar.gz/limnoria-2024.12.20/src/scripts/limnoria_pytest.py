#!/usr/bin/env python3

###
# Copyright (c) 2002-2005, Jeremiah Fincher
# Copyright (c) 2011, James McCoy
# Copyright (c) 2010-2021, Valentin Lorentz
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
###

import os
import sys
import time
import shutil
started = time.time()

import supybot
import logging
import traceback

# We need to do this before we import conf.
if not os.path.exists('test-conf'):
    os.mkdir('test-conf')

registryFilename = os.path.join('test-conf', 'test.conf')
fd = open(registryFilename, 'w')
fd.write("""
supybot.directories.data: %(base_dir)s/test-data
supybot.directories.conf: %(base_dir)s/test-conf
supybot.directories.log: %(base_dir)s/test-logs
supybot.reply.whenNotCommand: True
supybot.log.stdout: False
supybot.log.stdout.level: ERROR
supybot.log.level: DEBUG
supybot.log.format: %%(levelname)s %%(message)s
supybot.log.plugins.individualLogfiles: False
supybot.protocols.irc.throttleTime: 0
supybot.reply.whenAddressedBy.chars: @
supybot.networks.test.server: should.not.need.this
supybot.networks.testnet1.server: should.not.need.this
supybot.networks.testnet2.server: should.not.need.this
supybot.networks.testnet3.server: should.not.need.this
supybot.nick: test
supybot.databases.users.allowUnregistration: True
""" % {'base_dir': os.getcwd()})
fd.close()

import supybot.registry as registry
registry.open_registry(registryFilename)

import supybot.log as log
import supybot.conf as conf
conf.allowEval = True
conf.supybot.flush.setValue(False)

import re
import sys
import glob
import atexit
import os.path
import unittest

import supybot.utils as utils
import supybot.world as world
import supybot.callbacks as callbacks
world.startedAt = started

import logging
class TestLogFilter(logging.Filter):
    bads = [
        'No callbacks in',
        'Invalid channel database',
        'Exact error',
        'Invalid user dictionary',
        'because of noFlush',
        'Queuing NICK',
        'Queuing USER',
        'IgnoresDB.reload failed',
        'Starting log for',
        'Irc object for test dying',
        'Last Irc,',
        ]
    def filter(self, record):
        for bad in self.bads:
            if bad in record.msg:
                return False
        return True
log._logger.addFilter(TestLogFilter())

def main():
    import glob
    import os.path
    import optparse
    import supybot.test as test
    import supybot.plugin as plugin

    import pytest

    """
    pytest_args = []
    for arg in args:
        s = arg.rstrip('\\/')
        pluginDir = os.path.dirname(s) or '.'
        conf.supybot.directories.plugins.setValue([pluginDir])
        pluginName = os.path.basename(s)

        if pluginName.endswith('.py'):
            pluginName = pluginName[:-3]
        try:
            pluginModule = plugin.loadPluginModule(pluginName)
        except (ImportError, callbacks.Error) as e:
            if pytest:
                pytest_args.append(arg)
            else:
                sys.stderr.write('Failed to load plugin %s:' % pluginName)
                traceback.print_exc()
                sys.stderr.write('(pluginDirs: %s)\n' %
                                 conf.supybot.directories.plugins())
                continue
        else:
            if hasattr(pluginModule, 'test'):
                test.modules.append(pluginModule)"""

    sys.exit(pytest.main(sys.argv[1:], plugins=['supybot']))


if __name__ == '__main__':
    main()

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:

