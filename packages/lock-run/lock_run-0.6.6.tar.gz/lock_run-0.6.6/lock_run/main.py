
from sealpy.read import CipherReader

try:
    import reader
    import handler_code
    import utilitiles
except:
    from . import reader
    from . import handler_code
    from . import utilitiles
import argparse

def generate_key(key_len: int = 32):
    key = CipherReader.generate_key(key_len=key_len)
    print(key)
    return key

def cipher_code(root_dir: str, key: str):
    fix_root = utilitiles.refactor_path(path=root_dir)

    worker = handler_code.Worker(key=key, root_dir=fix_root)
    text, key_code, path = worker.cipher_file()

    print(f"Project was ciphered in {path} with key: {key_code}")

    return text, key_code, path

def run_file(root_dir: str, key: str, file_path: str):
    fix_root = utilitiles.refactor_path(path=root_dir)

    worker = handler_code.Worker(key=key, root_dir=fix_root)
    print(f"run {file_path} from {root_dir}")

    worker.run_cpython(file_path=file_path)

def cipher_code_cui():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--root_dir", type=str, help="root of project", required=True)
    parser.add_argument("--key", type=str, help="cipher key", required=True)

    args = parser.parse_args()

    cipher_code(root_dir=args.root_dir, key=args.key)

def run_code_cui():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--root_dir", type=str, help="root of project", required=True)
    parser.add_argument("--key", type=str, help="cipher key", required=True)
    parser.add_argument("--file_path", type=str, help="file path", required=True)


    args = parser.parse_args()

    run_file(root_dir=args.root_dir, key=args.key, file_path=args.file_path)

def gen_key_cui():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--key_len", type=int, help="key len", required=False)
    args = parser.parse_args()
    if args.key_len is not None:
        key_len = args.key_len
    else:
        key_len = 32
    generate_key(key_len=key_len)

