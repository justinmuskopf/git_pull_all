from subprocess import CalledProcessError

from lib.domain.command import Command
from lib.git.logger import GitLogger


class GitCommand(Command):
    GIT_CMD_FMT = 'git {}'
    GIT_DIR_CMD_FMT = 'git -C {} {}'

    def _log_error(self):
        GitLogger.error(f'Git Command "{self.command}" failed!')

    def __init__(self, command: str):
        self._git_cmd = command
        self._no_dir_cmd = self._get_no_dir_cmd()

        super().__init__(self._get_cmd(), shell=True)

    def _get_no_dir_cmd(self):
        return self.GIT_CMD_FMT.format(self._git_cmd)

    def _get_dir_cmd(self, dir_path: str = None):
        return self.GIT_DIR_CMD_FMT.format(dir_path, self._git_cmd)

    def _get_cmd(self, dir_path: str = None):
        return self._get_dir_cmd(dir_path) if dir_path else self._no_dir_cmd

    def run(self, dir_path: str = None, output_over_status_code: bool = True):
        self.command = self._get_cmd(dir_path)

        try:
            return super().run(output_over_status_code)
        except CalledProcessError as cpe:
            self._log_error()


class GitStatusCommand(GitCommand):
    def __init__(self):
        super().__init__('status')


class GitPullCommand(GitCommand):
    def __init__(self):
        super().__init__('pull')

