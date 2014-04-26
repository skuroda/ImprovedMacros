# Adapted from @wbond's resource loader.

import sys
import sublime

VERSION = int(sublime.version())

package_name = "ImprovedMacros"
top_level_module = "improved_macros"
mod_prefix = top_level_module
reload_mods = []

if VERSION > 3000:
    mod_prefix = "ImprovedMacros." + mod_prefix
    from imp import reload
    for mod in sys.modules:
        if mod[0:len(package_name)] == package_name and sys.modules[mod] is not None:
            reload_mods.append(mod)
else:

    for mod in sorted(sys.modules):
        if mod[0:len(top_level_module)] == top_level_module and sys.modules[mod] is not None:
            reload_mods.append(mod)

mods_load_order = [
    '.'
    '.package_resources'
    '.run_multiple_commands'
]

for suffix in mods_load_order:
    mod = mod_prefix + suffix
    if mod in reload_mods:
        reload(sys.modules[mod])
