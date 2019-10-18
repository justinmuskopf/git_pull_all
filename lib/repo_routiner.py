from lib.domain.directory import Directory
from lib.git.logger import GitLogger
from lib.git.repository import GitRepository


class RepoRoutiner:
    @staticmethod
    def _log(call, msg):
        call(f'[RepoRoutiner]: {msg}')

    def __init__(self, **kwargs):
        self.pull_master = kwargs['pull_master']
        self.pull_all = kwargs['pull_all']
        self.pull_dirty = kwargs['pull_dirty']
        self.ignore_dirs = kwargs['ignore']
        self.repos: [GitRepository] = self._get_all_repos_from_dirs(kwargs['dirs'])

        self.can_pull = self.pull_all or self.pull_master

    def should_ignore(self, dname):
        return dname in self.ignore_dirs

    # Will raise NotADirectoryError if dpath is invalid
    def _get_repos_from_dir(self, dpath: str) -> [GitRepository]:
        repos = []
        for d in Directory(dpath).list_dirs():
            if dpath in self.ignore_dirs:
                continue
            try:
                repos.append(GitRepository(d))
            except NotADirectoryError:
                continue

        return repos

    def _get_all_repos_from_dirs(self, dirs: [str]):
        repos = []
        for d in dirs:
            repos += self._get_repos_from_dir(d)

        return repos

    def should_pull(self, repo: GitRepository):
        if not self.can_pull:
            return False

        is_dirty = repo.is_dirty()
        branch = repo.get_branch()

        if is_dirty and not self.pull_dirty:
            self._log(GitLogger.warn, f'Cannot pull repo {repo.name}/{branch} because it is dirty!')
            return False

        if self.pull_all:
            return True

        if self.pull_master:
            if branch == 'master':
                return True
            else:
                self._log(GitLogger.warn, f'Cannot pull repo {repo.name}/{branch} because it is not on master!')

        return False

    def routine(self):
        for repo in self.repos:
            if self.should_pull(repo):
                repo.pull()
