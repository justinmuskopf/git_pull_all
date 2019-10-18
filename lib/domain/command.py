import subprocess


class Command:
    def __init__(self, command: str or [str], shell: bool = False):
        self.command = command
        self.shell = shell

    def _call_it(self, to_call):
        return to_call(self.command, shell=self.shell)

    def run_silently(self):
        self._call_it(subprocess.call)

    def run(self, output_over_status_code: bool = False) -> int or str:
        if output_over_status_code:
            return str(self._call_it(subprocess.check_output), 'utf-8')
        else:
            return self._call_it(subprocess.call)
