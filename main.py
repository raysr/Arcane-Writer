import sys
from PyQt5.QtWidgets import *
from writer import Writer

class AppWriter(QWidget):
    def __init__(self):
        super(AppWriter, self).__init__()
        self.container = QVBoxLayout()
        self.setLayout(self.container)
        self.lister = QListWidget()

        self.generated = QPlainTextEdit()
        self.pickfile = QPushButton()
        self.pickfile.setText("Pick files")

        self.generatedtext = QLabel()
        self.generatedtext.setText("Generated Text")

        self.generatetext = QPushButton()
        self.generatetext.setText("Generate Text")

        self.train = QPushButton()
        self.train.setText("Train")


        self.container.addWidget(self.lister)
        self.container.addWidget(self.pickfile)
        self.container.addWidget(self.train)
        self.container.addWidget(self.generatetext)
        self.container.addWidget(self.generatedtext)
        self.container.addWidget(self.generated)

        self.pickfile.clicked.connect(lambda: self.func_pickfile())
        self.train.clicked.connect(lambda: self.func_train())
        self.generatetext.clicked.connect(lambda: self.func_generate())

        self.files = []
        self.resize(800, 600)
        self.move(300, 300)
        self.setWindowTitle('Arcane Writer')
        self.show()

    def func_pickfile(self):
        self.fileDialog = QFileDialog(self)
        fis = self.fileDialog.getOpenFileNames()
        self.files+=fis[0]
        for i in fis[0]:
            self.lister.addItem(str(i))

    def func_train(self):
        self.writer = Writer(self.files)

    def func_generate(self):
        dep = self.writer.generate_text("The",10, 10)
        print(" GENERATED : "+str(dep))
        self.generate.appendPlainText(str(dep))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    aw = AppWriter()
    sys.exit(app.exec_())


