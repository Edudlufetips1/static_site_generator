import shutil, os

def copy_files_recursive(static, public):
    if not os.path.exists(public):
       os.mkdir(public) 
   
    for filename in os.listdir(static):
        from_path = os.path.join(static, filename)
        target_path = os.path.join(public, filename)
        print(f"{from_path} -> {target_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, target_path)
        else:
            copy_files_recursive(from_path, target_path)