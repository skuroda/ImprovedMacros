# http://www.sublimetext.com/forum/viewtopic.php?f=5&t=8677&sid=6152a4d1c6d6bf2b92893b69b8b34490&start=10
# run_multiple_commands.py

import sublime
import sublime_plugin
import json
import codecs
import os

# Takes an array of commands (same as those you'd provide to a key binding) with
# an optional context (defaults to view commands) & runs each command in order.
# Valid contexts are 'text', 'window', and 'app' for running a TextCommand,
# WindowCommands, or ApplicationCommand respectively.

# Should be inherited by something that extends WindowCommand
class RunMultipleCommandsBase(object):

    DELAY_KEY = "delay"
    VALID_CONTEXT = ["text", "window", "app"]

    def __init__(self, window):
        super(RunMultipleCommandsBase, self).__init__(window)

    # Precondition - Command contains a command and a valid context
    def exec_command(self, command):
        args = None
        if 'args' in command:
            args = command['args']

        # default context is the view since it's easiest to get the other contexts
        # from the view
        context = self.get_context(command)

        if args is None:
            context.run_command(command['command'])
        else:
            context.run_command(command['command'], args)

    def get_context(self, command):
        context = self.window.active_view()
        if 'context' in command:
            context_name = command['context']
            if context_name == 'app':
                context = sublime
            elif context_name == 'window':
                context = self.window
        return context

    def run_multiple_commands(self, commands, validate_context):
        if self.is_validate_arguments(commands, validate_context):
            cmd_len = len(commands)
            for i in range(cmd_len):
                command = commands[i]
                if self.is_delayed_command(command):
                    self.delayed_command(commands, i)
                    break
                else:
                    self.exec_command(command)
        pass

    def get_file_content(self, file_name):
        content = None
        if os.path.exists(file_name):
            with codecs.open(file_name, "r") as file_obj:
                content = file_obj.read()
        return content

    def from_json(self, content):
        if content is not None:
            try:
                return json.loads(content)
            except ex:
                pass
        return None

    def delayed_command(self, commands, index):
        new_commands = commands[index:]
        delay = new_commands[0][self.DELAY_KEY]
        new_commands[0][self.DELAY_KEY] = 0
        args = {"commands": new_commands}
        print(new_commands)
        print(delay)
        sublime.set_timeout(
            lambda: self.window.run_command("run_multiple_commands_delayed", args), delay)

    def is_delayed_command(self, command):
        return self.DELAY_KEY in command and command[self.DELAY_KEY] > 0

    def is_validate_arguments(self, commands, validate_context):
        if commands is not None:
            if len(commands) > 0:
                if not validate_context or self.is_valid_command_and_context(commands):
                    return True
        return False

    def is_valid_command_and_context(self, commands):
        for command in commands:
            if 'command' not in command:
                sublime.error_message("One or more commands are missing a command name")
                return False
            if 'context' in command:
                context_name = command['context']
                if context_name not in self.VALID_CONTEXT:
                    return False
                    sublime.error_message('Invalid command context "%s".' % context_name)

        return True


class RunMultipleCommandsFromFile(sublime_plugin.WindowCommand, RunMultipleCommandsBase):

    def __init__(self, window):
        super(RunMultipleCommandsFromFile, self).__init__(window)

    def run(self, file_name=None):
        if file_name is not None:
            content = self.get_file_content(file_name)
            commands = self.from_json(content)
        self.run_multiple_commands(commands, True)

    def get_file_content(self, file_name):
        content = None
        if os.path.exists(file_name):
            with codecs.open(file_name, "r") as file_obj:
                content = file_obj.read()
        return content

    def from_json(self, content):
        if content is not None:
            try:
                return json.loads(content)
            except ex:
                pass
        return None

class RunMultipleCommands(sublime_plugin.WindowCommand, RunMultipleCommandsBase):

    def __init__(self, window):
        super(RunMultipleCommands, self).__init__(window)

    def run(self, commands=None):
        self.run_multiple_commands(commands, True)

class RunMultipleCommandsDelayed(sublime_plugin.WindowCommand, RunMultipleCommandsBase):

    def __init__(self, window):
        super(RunMultipleCommandsDelayed, self).__init__(window)

    def run(self, commands):
        print(commands)
        self.run_multiple_commands(commands, False)