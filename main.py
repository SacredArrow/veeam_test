import filecmp
import os
import shutil
import time
import sys

class Logger:
    def __init__(self, path):
        self.log_file = open(path, "w")

    def log(self, info):
        print(info)
        self.log_file.write(info + "\n")


def copy(files, base_folder, target_folder):
    for file in files:
        base_path = os.path.join(base_folder, file)
        target_path = os.path.join(target_folder, file)
        if os.path.isfile(base_path) or os.path.islink(base_path):
            logger.log(f"Copying file {file} from {base_path} to {target_path}")
            shutil.copy(base_path, target_path)
        elif os.path.isdir(base_path):
            logger.log(f"Copying directory {file} from {base_path} to {target_path}")
            shutil.copytree(base_path, target_path)
        else:
            error = ValueError(base_path + " is neither file nor directory!")
            logger.log(str(error))
            raise error


def delete(files, target_folder):
    for file in files:
        path = os.path.join(target_folder, file)
        if os.path.isfile(path) or os.path.islink(path):
            logger.log(f"Deleting file {file} from {path}")
            os.remove(path)
        elif os.path.isdir(path):
            logger.log(f"Deleting folder {file} from {path}")
            shutil.rmtree(path)
        else:
            error = ValueError(path + " is neither file nor directory!")
            logger.log(str(error))
            raise error


def synchronize_folders(base_folder, target_folder):
    comparison = filecmp.dircmp(base_folder, target_folder)

    # If there are files/dirs that are present only in target folder, delete them
    if comparison.right_only:
        delete(comparison.right_only, target_folder)

    # If there are absent files/dirs just copy them
    if comparison.left_only:
        copy(comparison.left_only, base_folder, target_folder)

    # If some files are present in both folders but are different, overwrite them
    if comparison.diff_files:
        copy(comparison.diff_files, base_folder, target_folder)

    # If there are shared dirs, run this function recursively
    if comparison.common_dirs:
        for dir in comparison.common_dirs:
            synchronize_folders(os.path.join(base_folder, dir), os.path.join(target_folder, dir))




if __name__ == '__main__':
    if len(sys.argv[1:]) != 4:
        raise ValueError("Specify base folder, target folder, logging file and synchronization interval as "
                         "command-line arguments!")
    base_folder, target_folder, log_file, synchronization_interval = sys.argv[1:]
    logger = Logger(log_file)
    if not os.path.isdir(base_folder):
        error = ValueError("Base path is not a folder or doesn't exist!")
        logger.log(str(error))
        raise error
    if not os.path.isdir(target_folder):
        os.mkdir(target_folder)
    synchronization_interval = float(synchronization_interval)

    while True:
        try:
            synchronize_folders(os.path.abspath(base_folder), os.path.abspath(target_folder))
        except PermissionError as e:
            logger.log("Unsufficient permissions! Try to run this program as administrator.")
            logger.log(str(e))
            raise e
        time.sleep(synchronization_interval)


