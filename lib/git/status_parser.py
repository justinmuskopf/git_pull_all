
class GitStatusError(ValueError):
    def __init__(self, message: str = None):
        message = message or 'An unknown parsing error occurred!'
        super().__init__(message)


class GitStatusParser:
    def __init__(self, status_output: str):
        self.status_output = status_output

    @staticmethod
    def get_branch_from_output(output: str):
        if 'On branch' not in output:
            raise GitStatusError('No branch in status!')

        first_line = output.split('\n')[0]
        first_line_words = first_line.split(' ')

        # The first line of output should be
        # "On branch master" or similar
        if len(first_line_words) is not 3:
            raise GitStatusError()

        return first_line_words[2].strip()

    @staticmethod
    def is_dirty(output: str):
        return 'modified:' in output

    def branch(self):
        return self.get_branch_from_output(self.status_output)

    def dirty(self):
        return self.is_dirty(self.status_output)
