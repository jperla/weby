import os
import sys
import signal
from functools import partial

import pyinotify
from ..http import server

def notifier_in_directory(callback, directory=os.getcwd()):
    '''
    event: {'maskname': 'IN_DELETE', 'wd': 1, 'name': 'bla', 'mask': 512, 'pathname': '/home/jperla/projects/weby/bla', 'path': '/home/jperla/projects/weby', 'dir': False}
    Events Codes (masknames): http://pyinotify.sourceforge.net/doc-v07/public/pyinotify.EventsCodes-class.html
    '''
    # The watch manager stores the watches and provides operations on watches
    wm = pyinotify.WatchManager()
    FLAGS = pyinotify.EventsCodes.ALL_FLAGS
    mask = FLAGS['IN_DELETE'] | FLAGS['IN_CREATE']  # watched events
    wdd = wm.add_watch(os.getcwd(), mask, rec=True)
    notifier = pyinotify.Notifier(wm, callback)
    return notifier

def valid_change(event):
    if event.pathname.endswith('.py'):
        return True
    else:
        return False

def receive(changes, event):
    child_pid = changes['child']
    valid_change = changes['valid_change']
    if valid_change(event):
        #DEBUG: jperla: 
        #print str(event.pathname)
        #print str(event.maskname)
        if child_pid is not None:
            os.kill(child_pid, signal.SIGKILL)
            os.waitpid(child_pid, 0)
            fork_child_and_run(changes)
        else:
            print 'No child'


def fork_child_and_run(changes):
    r = os.fork()
    if r == 0:
        # in child
        try:
            changes['app']()
        except KeyboardInterrupt, e:
            sys.exit(0)
    else:
        # in parent
        changes['child']= r

def reload(filename):
    __name__ = '__main__'
    code = compile(open(filename).read(), filename, 'exec')
    exec(code, locals(), locals())

def run_app(file):
    reload(file)

def watcher_launcher():
    import optparse
    parser = optparse.OptionParser()
    parser.add_option("-f", "--file", dest="file", default=None,
                    help="file")
    parser.add_option("-q", "--quiet",
                    action="store_false", dest="verbose", default=True,
                    help="don't print status messages to stdout")
    (options, args) = parser.parse_args()
    file = options.file
    app = partial(run_app, file)
    changes = {'valid_change':valid_change, 'child':None, 'app':app}
    receive_with_changes = partial(receive, changes)
    fork_child_and_run(changes)
    dir = os.getcwd()
    notifier = notifier_in_directory(receive_with_changes, dir)
    notifier.loop()

