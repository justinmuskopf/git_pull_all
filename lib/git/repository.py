import os

from lib.domain.directory import Directory
from lib.git.command import GitCommand, GitStatusCommand, GitPullCommand
from lib.git.logger import GitLogger
from lib.git.status_parser import GitStatusParser


class NotAGitRepositoryError(NotADirectoryError):
    def __init__(self, dpath):
        super().__init__(f'{dpath} is not a valid Git repository!')


class GitRepository(Directory):
    ID, REPO_COUNT = 0, 0

    def _log(self, call, msg):
        call(f' [REPO {self.id}] {self.name}: ' + msg)

    def __init__(self, absolute_path: str):
        super().__init__(absolute_path)
        if not self._is_git_repo():
            raise NotAGitRepositoryError(absolute_path)

        GitRepository.ID += 1
        GitRepository.REPO_COUNT += 1

        self.status_cmd = GitStatusCommand()
        self.pull_cmd = GitPullCommand()

        self._setup()
        self.updated = False

    def _setup(self):
        split_em_up = self.absolute_path.split(os.sep)
        self.id = GitRepository.ID
        self.name = split_em_up[-2]
        self.absolute_dir = os.sep.join(split_em_up[:-2])

        self._log(GitLogger.info, f'Registering Git Repository located at {self.absolute_dir}')

    def _is_git_repo(self):
        return self.contains_dir('.git')

    def _update_if_needed(self):
        if not self.updated:
            self.update_status()

    def get_branch(self):
        self._update_if_needed()
        return self.status.branch()

    def is_dirty(self):
        self._update_if_needed()
        return self.status.dirty()

    def update_status(self):
        self._log(GitLogger.debug, 'Getting status!')
        status_output = self.status_cmd.run(self.absolute_path)
        self.status = GitStatusParser(status_output)
        self.updated = True

    def pull(self):
        self._update_if_needed()

        self._log(GitLogger.debug, f'Pulling branch: {self.get_branch()}!')
        pull_output = self.pull_cmd.run(self.absolute_path)
