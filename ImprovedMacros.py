import sublime
import sys

VERSION = int(sublime.version())

reloader = "improved_macros.reloader"

if VERSION > 3000:
    reloader = 'ImprovedMacros.' + reloader
    from imp import reload


# Make sure all dependencies are reloaded on upgrade
if reloader in sys.modules:
    reload(sys.modules[reloader])

if VERSION > 3000:
    from .improved_macros import reloader
    from .improved_macros.run_multiple_commands import *
else:
    from improved_macros import reloader
    from improved_macros.run_multiple_commands import *
