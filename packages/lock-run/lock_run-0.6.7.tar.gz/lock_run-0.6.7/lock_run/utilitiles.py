def refactor_path(path: str):
    new_path = path
    new_path = new_path.replace("\\", "/")
    if new_path[len(new_path) - 1] != "/":
        new_path += "/"
    return new_path

