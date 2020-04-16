# empty comment line. delete me, and put sum imports, when time comes


class Logger:
    def __init__(self, filename):
        self.filename = filename
        self.file = open(self.filename, 'w')
        self.file.write('')
        self.file.close()

    def clear(self):
        if self.file.closed:
            self.file = open(self.filename, 'w')
        elif self.file.mode == 'r':
            self.file.close()
            self.file = open(self.filename, 'w')
        self.file.write('')
        self.file.close()



