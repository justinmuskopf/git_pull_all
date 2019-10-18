from os import sep, listdir
from os.path import isdir, isfile


class Directory:
    def __init__(self, absolute_path: str):
        absolute_path = self._get_validated_path(absolute_path)
        if not isdir(absolute_path):
            raise NotADirectoryError(absolute_path)

        if not (absolute_path.endswith(sep)):
            absolute_path += sep

        self.absolute_path = absolute_path

    @classmethod
    def _get_validated_path(cls, path: str):
        if sep is '/' and '\\' in path:
            return path.replace('\\', '/')
        elif sep is '\\' and '/' in path:
            return path.replace('/', '\\')

        return path

    def _form_path(self, extension):
        return self.absolute_path + extension

    def list(self):
        return listdir(self.absolute_path)

    def list_dirs(self):
        return [self._form_path(d) for d in self.list() if self.contains_dir(d)]

    def contains(self, extension: str, call):
        absolute_path = self._form_path(extension)

        return call(absolute_path)

    def contains_dir(self, dirname: str):
        return self.contains(dirname, isdir)

    def contains_file(self, filename: str):
        return self.contains(filename, isfile)
