# ImprovedMacros
This plugin is incomplete. Macro recording, which is the general goal of this plugin, is not yet complete. However, the ability to manually define macros via a file or as a key binding argument is functional.

## Installation
Note it may be necessary to restart the editor after installing the plugin.

### Package Control
Installation through [package control](http://wbond.net/sublime_packages/package_control) is recommended. It will handle updating your packages as they become available. To install, do the following.

* In the Command Palette, enter `Package Control: Install Package`
* Search for `ImprovedMacros` to see install the plugin.

### Manual
Clone or copy this repository into the packages directory. By default, the Package directory is located at:

* OS X: ~/Library/Application Support/Sublime Text 2/Packages/
* Windows: %APPDATA%/Roaming/Sublime Text 2/Packages/
* Linux: ~/.config/sublime-text-2/Packages/

or

* OS X: ~/Library/Application Support/Sublime Text 3/Packages/
* Windows: %APPDATA%/Roaming/Sublime Text 3/Packages/
* Linux: ~/.config/sublime-text-3/Packages/

## Usage
Macros can be define as part of a key binding, or in a file. The content of `args` for a key binding will match what is defined in a file.

## Commands
Below are the commands currently exposed.

* `run_multiple_commands` - This command will run multiple commands, where the macro is specified within the key binding itself.

    * The top level argument for this command is `commands`. It contains a list of entries, as defined in "Defining a macro"

* `run_multiple_commands_from_file` - This command will run multiple commands, where the macro is defined in a file.

### Defining a macro
* `context` - This is the context to run a command. Valid entries for this are `view`, `window`, and `app`. If no context entry is specified, `view` will be used as the default.

* `command` - The name of the command to run. This is the same command that would appear if one were to log the commands using `sublime.log_commands(True)` in the ST console.

* `args` - The arguments for the command.

* `delay` - A delay (in milliseconds) before running the current command.

### Sample usage
Below is an example of `run_multiple_commands`

    {
        "keys": ["f12"], "command": "run_multiple_commands",
        "args": {
            "commands": [{
                "context": "window",
                "command": "next_view"
            },{
                "context": "view",
                "command": "insert",
                "args": {
                    "characters": "qwerty"
                },
                "delay": 1000
            }]
        }
     }

 Below is an example of `run_multiple_commands_from_file`. First is a key binding entry. Note that file name can either be `Packages/<package name>/<macro name>` or an absolute path.

    {
        "keys": ["f11"], "command": "run_multiple_commands_from_file",
        "args": {
            "file_name": "Packages/User/test.macro"
        }
    }


Below is the content of `test.macro`

    [{
        "context": "window",
        "command": "next_view"
    }, {
        "context": "view",
        "command": "insert",
        "args": {
            "characters": "qwerty"
        },
        "delay": 1000
    }]

## Notes

Thank you to sashabe and nilium from the ST forum.
