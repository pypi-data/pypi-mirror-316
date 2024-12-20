try:
    import reader
except:
    from . import reader
import os

class Worker:
    def __init__(self, key, root_dir):
        self.key = key
        self.root_dir = root_dir

    def run_cpython(self, file_path):
        reader_project = reader.ReaderProject(root_dir=self.root_dir)
        reader_project.get_files_from_directory()

        text, key, path, handler_object = reader_project.anti_cipher_files(key=self.key)

        python_path = f"{path}/{file_path}"

        os.system(f"cd {path} && python {file_path}")

        handler_object.del_folder()
        

    def cipher_file(self):

        reader_project = reader.ReaderProject(root_dir=self.root_dir)
        reader_project.get_files_from_directory()
        
        text, key, path = reader_project.cipher_files(key=self.key)

        return text, key, path

    

    
    
