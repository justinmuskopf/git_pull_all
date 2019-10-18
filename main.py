from lib.domain.logger import LoggerLevels, Logger
from lib.repo_routiner import RepoRoutiner

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Traverse, update, and get the status of local Git repositories!\n' +
                                     'By default only runs STATUS on repositories in current directory.\n' +
                                     'Please see -pm, -pa, and -pd for information on the PULL action.')
    parser.add_argument('-pd', '--pull-dirty',
                        action='store_true',
                        help='Perform PULL action on MODIFIED repositories.')
    parser.add_argument('-pm', '--pull-master',
                        action='store_true',
                        help='Perform PULL action on repositories that are on the MASTER branch (See -pd to learn about pulling MODIFIED repositories).')
    parser.add_argument('-pa', '--pull-all',
                        action='store_true',
                        help='Perform PULL action on repositories that are on ANY branch. (Implies -pm, See -pd to learn about pulling MODIFIED repositories)')
    parser.add_argument('-i', '--ignore',
                        default=[],
                        nargs='*',
                        help='A list of directories to ignore. Empty by default')
    parser.add_argument('-l', '--log-level',
                        default=LoggerLevels.INFO,
                        help='The logging level. Options are: [DEBUG, INFO, WARN, ERROR], with decreasing output in that order.')
    parser.add_argument('-d', '--dirs',
                        default=['.'],
                        nargs='*',
                        help='A list of base directories to scan for Git repositories. Defaults to current directory.')

    args = parser.parse_args()

    Logger.LoggingLevel = args.log_level

    rr = RepoRoutiner(**vars(args))
    rr.routine()
