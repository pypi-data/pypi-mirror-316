from sealpy.read import CipherReader
import os
import shutil

class HandleFiles:
    def __init__(self, files_path: list[str], key: str, root_dir: str) -> None:
        self.files_path: str = files_path
        self.key = key
        self.root_dir = root_dir

    
    

    def handler(self, new_text: str, key: str, path: str) -> tuple[str, str, str]:
        return new_text, key, path

    def can_be_cipher(self) -> list:
        error_files: list = []
        for file in self.files_path:
            try:
                cipher_reader = CipherReader(file_path=file)

            except:

                error_files.append(file)
            
        return error_files
    
    def make_path(self, arr, with_start = True):
        path = ""
        for el in arr:
            if with_start:
                path += f"\\{el}"
            else:
                path += f"{el}\\"

        return path

    def path_handler(self, adder, minus: int = 2):
        splitter = self.root_dir.split("/")
        folder_name = f"{adder}{splitter[len(splitter) - minus]}"
        new_path = f"{self.make_path(arr=splitter[:-minus], with_start=False)}{folder_name}\\"
        return new_path

class CipherFile(HandleFiles):
    def __init__(self, files_path: list[str], key: str, root_dir: str):
        super().__init__(files_path=files_path, key=key, root_dir=root_dir)
    
    

    def handler(self) -> tuple[str, str]:
        error_files = self.can_be_cipher()

        file_adder = "C_"
        root_dir = self.path_handler(adder=file_adder)
        try:
            os.mkdir(root_dir)
        except:
            shutil.rmtree(root_dir)
            os.mkdir(root_dir)



        for file in self.files_path:
            current_path = os.path.relpath(file, self.root_dir)
            file_path = f"{root_dir}{current_path}"
            if file in error_files:
                shutil.copy2(file, file_path)
                
            else:
                cipher_reader = CipherReader(file_path=file)
                key, cipher_text = cipher_reader.cipher_file(key=self.key, save=False)
                with open(file_path, 'w', encoding="utf-8") as file_code:
                    file_code.write(cipher_text)

        return super().handler(new_text=cipher_text, key=key, path=root_dir)
    
class AntiCipherFile(HandleFiles):
    def __init__(self, files_path: list[str], key: str, root_dir: str):
        super().__init__(files_path=files_path, key=key, root_dir=root_dir)
    
    def handler(self) -> tuple[str, str]:
        error_files = self.can_be_cipher()
        file_adder = "."
        
        splitter = self.root_dir.split("/")
        folder_name = f"{file_adder}{splitter[len(splitter) - 2]}"

        root = os.environ['TEMP']
        root_dir = f'{root}\\{folder_name}'
        
        try:
            os.mkdir(root_dir)
        except:
            shutil.rmtree(root_dir)
            os.mkdir(root_dir)

        for file in self.files_path:
            current_path = os.path.relpath(file, self.root_dir)

            file_path = f"{root_dir}\\{current_path}"
            print(file_path)

            if file in error_files:
                shutil.copy(file, file_path)

            else:
                cipher_reader = CipherReader(file_path=file)
                key, anti_cipher_text = cipher_reader.anti_cipher_file(key=self.key, save=False)

                with open(file_path, 'w', encoding="utf-8") as file_code:
                    file_code.write(anti_cipher_text)


        self.new_root_dir = root_dir

        return super().handler(new_text=anti_cipher_text, key=key, path=root_dir)

    def del_folder(self):
        shutil.rmtree(self.new_root_dir)