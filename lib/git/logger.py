from lib.domain.logger import Logger


class GitLogger(Logger):
    @staticmethod
    def _repo_str(repo_num, num_repos):
        return f'({repo_num}/{num_repos})'
