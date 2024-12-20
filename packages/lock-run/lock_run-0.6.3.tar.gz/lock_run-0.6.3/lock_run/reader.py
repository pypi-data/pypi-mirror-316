import handler_data_files
import os


class ReaderProject:
    def __init__(self, root_dir: str):
        self.root_dir = root_dir

        self.all_files = []


    def get_files_from_directory(self, current_path: str = "")  -> list:
        files = os.listdir(self.root_dir + current_path)
        for element in files:
            file_path = self.root_dir + current_path + element
            if os.path.isfile(file_path):
                self.all_files.append(file_path)
            else:
                self.get_files_from_directory(current_path=current_path + element + "\\")


        return self.all_files

    def cipher_files(self, key: str):

        handler_object = handler_data_files.CipherFile(files_path=self.all_files, key=key, root_dir=self.root_dir)
        text, key, path = handler_object.handler()

        return text, key, path

    def anti_cipher_files(self, key: str):

        handler_object = handler_data_files.AntiCipherFile(files_path=self.all_files, key=key, root_dir=self.root_dir)
        text, key, path = handler_object.handler()

        return text, key, path, handler_object

    