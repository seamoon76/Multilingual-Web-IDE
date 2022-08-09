import sys
from pdb import Pdb

class Restart(Exception):
    """Causes a debugger to be restarted for the debugged python program."""
    pass

class Mypdb(Pdb):
    def __init__(self, *args, **kwargs):
        super(Mypdb, self).__init__(*args, **kwargs)
        self._user_requested_quit = False
        self.prompt = "[my-pdb] "

    def do_line(self, arg: str) -> bool:
        self.lastcmd = 'line'
        last = None
        lineno=self.curframe.f_lineno

        filename = self.curframe.f_code.co_filename
        breaklist = self.get_file_breaks(filename)
        self.message('lineno:'+str(lineno)+'.end')

    do_ln=do_line


def stop():
    debugger = Mypdb()
    debugger.set_trace(sys._getframe().f_back)


_usage="usage: pdb.py [-c command] ... [-m module | pyfile] [arg]"

def main():
    import getopt
    import pdb
    import os
    import sys
    import traceback
    opts, args = getopt.getopt(sys.argv[1:], 'mhc:', ['help', 'command='])

    if not args:
        print(_usage)
        sys.exit(2)

    commands = []
    run_as_module = False
    for opt, optarg in opts:
        if opt in ['-h', '--help']:
            print(_usage)
            sys.exit()
        elif opt in ['-c', '--command']:
            commands.append(optarg)
        elif opt in ['-m']:
            run_as_module = True

    mainpyfile = args[0]     # Get script filename
    if not run_as_module and not os.path.exists(mainpyfile):
        print('Error:', mainpyfile, 'does not exist')
        sys.exit(1)
    
    if run_as_module:
        import runpy
        try:
            runpy._get_module_details(mainpyfile)
        except Exception:
            traceback.print_exc()
            sys.exit(1)

    sys.argv[:] = args      # Hide "pdb.py" and pdb options from argument list

    if not run_as_module:
        mainpyfile = os.path.realpath(mainpyfile)
        # Replace pdb's dir with script's dir in front of module search path.
        sys.path[0] = os.path.dirname(mainpyfile)
    
    # Note on saving/restoring sys.argv: it's a good idea when sys.argv was
    # modified by the script being debugged. It's a bad idea when it was
    # changed by the user from the command line. There is a "restart" command
    # which allows explicit specification of command line arguments.
    debugger = Mypdb()
    debugger.rcLines.extend(commands)
    while True:
        try:
            
            if run_as_module:
                debugger._runmodule(mainpyfile)
            else:
                debugger._runscript(mainpyfile)
            if debugger._user_requested_quit:
                break
            print("The program finished and will be restarted")
        except pdb.Restart:
            print("Restarting", mainpyfile, "with arguments:")
            print("\t" + " ".join(sys.argv[1:]))
        except SystemExit:
            # In most cases SystemExit does not warrant a post-mortem session.
            print("The program exited via sys.exit(). Exit status:", end=' ')
            print(sys.exc_info()[1])
        except SyntaxError:
            traceback.print_exc()
            sys.exit(1)
        except:
            traceback.print_exc()
            print("Uncaught exception. Entering post mortem debugging")
            print("Running 'cont' or 'step' will restart the program")
            t = sys.exc_info()[2]
            debugger.interaction(None, t)
            print("Post mortem debugger finished. The " + mainpyfile +
                  " will be restarted")


# When invoked as main program, invoke the debugger on a script
if __name__ == '__main__':
    main()
