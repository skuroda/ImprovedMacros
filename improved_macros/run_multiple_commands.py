# http://www.sublimetext.com/forum/viewtopic.php?f=5&t=8677&sid=6152a4d1c6d6bf2b92893b69b8b34490&start=10
# run_multiple_commands.py


import sublime
import sublime_plugin
import json

# Takes an array of commands (same as those you'd provide to a key binding) with
# an optional context (defaults to view commands) & runs each command in order.
# Valid contexts are 'text', 'window', and 'app' for running a TextCommand,
# WindowCommands, or ApplicationCommand respectively.
class RunMultipleCommandsCommand(sublime_plugin.WindowCommand):

    DELAY_KEY = "delay"
    VALID_CONTEXT = ["text", "window", "app"]

    # Precondition - Command contains a command and a valid context
    def exec_command(self, command):
        args = None
        if 'args' in command:
            args = command['args']

        # default context is the view since it's easiest to get the other contexts
        # from the view
        context = self.window
        if 'context' in command:
            context_name = command['context']
            if context_name == 'app':
                context = sublime
            elif context_name == 'window':
                pass
            else:
                context = context.active_view()


        if args is None:
            context.run_command(command['command'])
        else:
            context.run_command(command['command'], args)


    def run(self, commands=None, file_name=None, validate_context=True):
        if file_name is not None:
            commands = self.read_command_file(file_name)
        if self.is_validate_arguments(commands, validate_context):
            cmd_len = len(commands)
            for i in range(cmd_len):
                command = commands[i]
                if self.is_delayed_command(command):
                    self.delayed_command(commands, i)
                    break
                else:
                    self.exec_command(command)

    def read_command_file(self, file_name):
        content = "foo" # Read JSON file
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
        args = {"commands": new_commands, "validate_context": False}
        print(new_commands)
        sublime.set_timeout(
            lambda: self.window.run_command("run_multiple_commands", args), delay)

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
