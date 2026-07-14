from core.models import Change


class ChangeManager:

    def __init__(self):

        self._changes = []

    def add(self, change: Change):

        self._changes.append(change)

    def clear(self):

        self._changes.clear()

    def all(self):

        return list(self._changes)

    def count(self):

        return len(self._changes)