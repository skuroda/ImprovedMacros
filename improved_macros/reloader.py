# Adapted from @wbond's resource loader.

import sys
import sublime

VERSION = int(sublime.version())

mod_prefix = "improved_macros"
reload_mods = []

if VERSION > 3000:
    mod_prefix = "ImprovedMacros." + mod_prefix
    from imp import reload
    for mod in sys.modules:
        if mod[0:14] == 'ImprovedMacros' and sys.modules[mod] is not None:
            reload_mods.append(mod)
else:

    for mod in sorted(sys.modules):
        if mod[0:15] == 'improved_macros' and sys.modules[mod] is not None:
            reload_mods.append(mod)

mods_load_order = [
    '.run_multiple_commands'
]

for suffix in mods_load_order:
    mod = mod_prefix + suffix
    if mod in reload_mods:
        reload(sys.modules[mod])
