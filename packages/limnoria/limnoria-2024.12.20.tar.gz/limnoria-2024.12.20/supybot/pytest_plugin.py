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

import os.path

import pytest

def pytest_addoption(parser):
    group = parser.getgroup("supybot", "options for Supybot/Limnoria configuration")

    parser.addoption('--clean', action='store_true', default=False,
                     dest='supybot_clean', help='Cleans the various data/conf/logs'
                     'directories before running tests.')
    parser.addoption('--timeout', action='store', type='float',
                     dest='supybot_timeout',
                     help='Sets the timeout, in seconds, for tests to return '
                     'responses.')
    parser.addoption('--no-network', action='store_true', default=False,
                     dest='supybot_nonetwork',
                     help='Causes the network-based tests not to run.')
    parser.addoption('--no-setuid', action='store_true', default=False,
                     dest='supybot_nosetuid',
                     help='Causes the tests based on a setuid executable not to run.')
    parser.addoption('--trace-calls', action='store_true', default=False,
                     dest='supybot_trace',
                     help='Traces all calls made.  Unless you\'re really in '
                     'a pinch, you probably shouldn\'t do this; it results '
                     'in copious amounts of output.')
    parser.addoption('--disable-multiprocessing', action='store_true',
                     dest='supybot_disableMultiprocessing',
                     help='Disables multiprocessing stuff.')


def pytest_configure(config):
    config.getini('python_files').append('test.py')

    from supybot import conf, log, test, world

    world.disableMultiprocessing = config.option.supybot_disableMultiprocessing

    if config.option.supybot_timeout:
        test.timeout = options.timeout

    if config.option.supybot_trace:
        traceFilename = conf.supybot.directories.log.dirize('trace.log')
        fd = open(traceFilename, 'w')
        sys.settrace(utils.gen.callTracer(fd))
        atexit.register(fd.close)
        atexit.register(lambda : sys.settrace(None))

    world.myVerbose = config.option.verbose

    if config.option.supybot_nonetwork:
        test.network = False
    if config.option.supybot_nosetuid:
        test.setuid = False

    log.testing = True
    world.testing = True

    if config.option.supybot_clean:
        shutil.rmtree(conf.supybot.directories.log())
        shutil.rmtree(conf.supybot.directories.conf())
        shutil.rmtree(conf.supybot.directories.data())

def pytest_pycollect_makemodule(path, parent):
    print('pytest_pycollect_makemodule')
    print(parent, repr(parent.__class__), path)
    print(repr(path.__class__))
    from supybot import conf, plugin
    (dirname, filename) = os.path.split(path)
    if filename == '__init__.py':
        plugin_path = dirname
    else:
        plugin_path = path

    (plugin_dir, plugin_name) = os.path.split(plugin_path)

    print('pytest_pycollect_makemodule', 'plugin_dir', plugin_dir)

    with conf.supybot.directories.plugins.context([plugin_dir]):
        try:
            plugin_module = plugin.loadPluginModule(plugin_name)
            print('loaded plugin', repr(plugin_module))
            assert plugin_module.__file__.startswith(plugin_dir)
            print('assert suceeded')
        except ImportError:
            print('failed to import')
            pass
        else:
            print('imported', plugin_name, plugin_module)
            import sys
            sys.modules[plugin_name] = plugin_module
            return pytest.Module(path, parent)
            '''
            import sys
            sys.modules[plugin_module.__name__] = plugin_module
            import py
            path = py.path.local(plugin_module.__name__).dirpath()
            plugin_module.__file__ = str(path)
            return pytest.Module(path, parent)'''




'''
def pytest_collect_directory(path, parent):
    from supybot import conf, plugin
    print('pytest_collect_directory', path)
    (pluginDir, pluginName) = os.path.split(path)
    with conf.supybot.directories.plugins.context([pluginDir]):
        try:
            pluginModule = plugin.loadPluginModule(pluginName)
        except ImportError:
            print('failed to import')
            pass
        else:
            print('imported')


def pytest_collect_file(parent, path):
    from supybot import conf
    pluginDirs = conf.supybot.directories.plugins()
    (dir_, filename) = os.path.split(path)
    (pluginDir, pluginName) = os.path.split(dir_)
    #print('prepending', pluginDir)
    #pluginDirs += ['.']
    #conf.supybot.directories.plugins.setValue(pluginDirs)
'''
