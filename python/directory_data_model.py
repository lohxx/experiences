import os


class Directory:
    def __init__(self, path):
        self.path = path

    @property
    def exists(self):
        return os.path.exists(self.path)

    @property
    def children(self):
        return os.listdir(self.path)

    def __len__(self):
        return len(self.children)

dir = Directory('.')

print(dir.exists)
print(len(dir))