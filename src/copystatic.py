import os  #for things like listingd dirs, joining paths, check if smth is a file
import shutil #for copying files and removing directory trees

def copy_files_recursive(source_dir_path, dest_dir_path):
    if os.path.exists(dest_dir_path):
        shutil.rmtree(dest_dir_path)
    
    os.mkdir(dest_dir_path)
        
    for item in os.listdir(source_dir_path):
        full_source = os.path.join(source_dir_path, item)
        full_dest = os.path.join(dest_dir_path, item)
        if os.path.isfile(full_source):
            print(f" * {full_source} -> {full_dest}")
            shutil.copy(full_source, full_dest)
        else:
            print(f"recursing into: {full_source}")
            copy_files_recursive(full_source, full_dest)
