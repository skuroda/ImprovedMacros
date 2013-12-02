#http://www.sublimetext.com/forum/viewtopic.php?f=5&t=8677&sid=6152a4d1c6d6bf2b92893b69b8b34490&start=10
# run_multiple_commands.py
import sublime, sublime_plugin

# Takes an array of commands (same as those you'd provide to a key binding) with
# an optional context (defaults to view commands) & runs each command in order.
# Valid contexts are 'text', 'window', and 'app' for running a TextCommand,
# WindowCommands, or ApplicationCommand respectively.
class RunMultipleCommandsCommand(sublime_plugin.TextCommand):
  def exec_command(self, command):
    if not 'command' in command:
      raise Exception('No command name provided.')

    args = None
    if 'args' in command:
      args = command['args']

    # default context is the view since it's easiest to get the other contexts
    # from the view
    context = self.view
    if 'context' in command:
      context_name = command['context']
      if context_name == 'window':
        context = context.window()
      elif context_name == 'app':
        context = sublime
      elif context_name == 'text':
        pass
      else:
        raise Exception('Invalid command context "'+context_name+'".')

    if 'delay' in command:
      delay = command['delay']
    else:
      delay = 0

    # skip args if not needed
    if args is None:
      sublime.set_timeout(lambda: context.run_command(command['command']),delay)
    else:
      sublime.set_timeout(lambda: context.run_command(command['command'], args),delay)

  def run(self, edit, commands = None):
    if commands is None:
      return # not an error
    for command in commands:
      # sublime.set_timeout(lambda: self.perform_action(view),2500)
      self.exec_command(command)
