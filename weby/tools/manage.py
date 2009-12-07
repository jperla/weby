#!/usr/bin/env python

import weby
import tests

if __name__ == '__main__':
    modules = [tests,]
    app = tests.apps.hello.app 
    weby.tools.watcher_launcher(modules, app)

