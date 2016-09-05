
class PlatformCount(object):
    def __init__(self):
        self.count = 0

    @property
    def pfCount(self):
        """Getter: I'm the pfCount property."""
        return self.count

    @pfCount.setter
    def pfCount(self, x):
        """Setter: I'm the pfCount setter."""
        self.count = x

# if __name__ == '__main__':
#     pc = PlatformCount()
#     print pc.pfCount
#     pc.pfCount = "sweet 1"
#     print pc.pfCount

