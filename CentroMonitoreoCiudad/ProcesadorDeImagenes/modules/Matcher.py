import os
from os import walk
from ProcesadorDeImagenes.modules.LBPH_wrapper import LBPHWrapper
import sys
sys.path.insert(0, '../')
import Utils.const as CONST
class Matcher:
    def __init__(self):
        self.lbph_wrapper = LBPHWrapper(50,100)
        self.files = []
        self.train = []
        self.labels = []
        print(os.path.dirname(os.path.abspath(__file__)))
        basedir=os.path.dirname(os.path.abspath(__file__))
        personsDirectory = basedir+"../../"+ CONST.PERSONIMAGECONTAINERFOLDER
        for (dirpath, dirnames, filenames) in walk(personsDirectory):
            self.files.extend(filenames)
            break
        current_label = 0
        for filename in self.files:
            current_file = open(filename, 'r')
            self.train.append(self.lbph_wrapper.bytes_to_img(current_file.read()))
            self.labels.append(current_label)
            current_label +=1
            current_file.close()
        self.lbph_wrapper.train(self.train,self.labels)
    def predict(self, image_filepath):
        source_file = open(image_filepath, 'r')
        result_label = self.lbph.predict(self.lbph.bytes_to_img(source_file.read()))
        source_file.close()
        if not result_label == None:
            return self.files[result_label]
        return None
