from pathlib import Path
import os
import zipfile
from datetime import datetime
from tkinter.filedialog import askopenfilename


class FileManager:
    @staticmethod
    def check_shelve_file(folder_path, file_name):
        dat_status_file_path = folder_path / Path(file_name + '.dat')
        bak_status_file_path = folder_path / Path(file_name + '.bak')
        dir_status_file_path = folder_path / Path(file_name + '.dir')
        return dat_status_file_path.is_file() and bak_status_file_path.is_file() and dir_status_file_path.is_file()

    @staticmethod
    def check_and_create_folder(folder_path):
        print('\n---------check_and_create_folder-------------------------')
        print('\n checking if the folder exists....')
        # check if the folder exists
        if folder_path.is_dir():  # returns true if the path exists and is a folder
            print('\nthe folder' + str(folder_path) + ', exists')
        else:
            # if the path does not exist or is not a folder then create the folder
            print('\nthe folder' + str(folder_path) + ', does NOT exists, creating folder....')
            os.makedirs(folder_path)
            print('\nDone.')

    @staticmethod
    def get_shelve_files(folder):
        dat_files = list(folder.glob('*.dat'))
        bak_files = list(folder.glob('*.bak'))
        dir_files = list(folder.glob('*.dir'))
        return dat_files, bak_files, dir_files

    def delete_shelf_files(self, folder):
        # get the  shelf files in the folder
        print('\n---------delete_shelve_files-------------------------')
        print('\ngetting shelve files.....')
        dat_files, bak_files, dir_files = self.get_shelve_files(folder)

        if len(dat_files) > 0 and len(bak_files) > 0 and len(dir_files) > 0:
            print('\nshelve files found, deleting them...')
            for dat_file in dat_files:
                os.unlink(dat_file)
                print('\n', dat_file, ' deleted')
            for bak_file in bak_files:
                os.unlink(bak_file)
                print('\n', bak_file, ' deleted')
            for dir_file in dir_files:
                os.unlink(dir_file)
                print('\n', dir_file, ' deleted')
            print('Done.')
        else:
            print('shelve files NOT found!, finishing the program')

    @staticmethod
    def get_unused_file_name(folder, basename, extension):
        number = 1
        while True:
            file_name = Path(folder) / Path(basename + str(number) + extension)
            if file_name.exists():
                print('the ' + str(file_name) + ' file exists, exploring more names')
                number += 1
            else:
                return file_name

    def backup_all_shelve_files_to_zip_files(self, origin_folder, destination_folder, basename):
        print('\n---------backup_to_zip-------------------------')
        # check if there are shelf files in the origin folder
        print('\n getting shelve files.....')
        dat_files, bak_files, dir_files = self.get_shelve_files(origin_folder)
        # check there is more than 1 shelve file
        if len(dat_files) > 0 and len(bak_files) > 0 and len(dir_files) > 0:
            print('\nthere are shelve files in the directory:\n ' + str(origin_folder) + '\ncopying them.....')

            # name the zipfile correctly
            # get the number correctly
            zip_filename = \
                self.get_unused_file_name(folder=destination_folder, basename=basename, extension='.zip')
            # create the zipfile
            print(f'Creating {zip_filename}...')
            backup_zip = zipfile.ZipFile(zip_filename, 'w')
            print('Done.')
            # zip all the shelf files
            for dat_file in dat_files:
                backup_zip.write(dat_file, dat_file.name)
                print('\n', dat_file, ' moved')
            for bak_file in bak_files:
                backup_zip.write(bak_file, bak_file.name)
                print('\n', bak_file, ' moved')
            for dir_file in dir_files:
                backup_zip.write(dir_file, dir_file.name)
                print('\n', dir_file, ' moved')
            backup_zip.close()
            print('Done.')
        else:
            print('\nthere are no shelve files in the directory:\n ' + str(origin_folder) + '\nending program...')

    @staticmethod
    def unzip_to_folder(zip_file_path):
        zip_file_path = Path(zip_file_path)
        # file name without extension
        zip_file_name = zip_file_path.stem
        folder_path = zip_file_path.parent
        unzipped_folder_path = folder_path / zip_file_name
        zip_object = zipfile.ZipFile(zip_file_path)
        # extract all the files from the folder
        zip_object.extractall(unzipped_folder_path)
        print('all files from ', str(zip_file_path), 'extracted in ', str(unzipped_folder_path))
        print('Done.')
        return unzipped_folder_path

'''    def get_program_status(self, folder_path):
        if self.check_shelve_file(folder_path, 'status'):
            status_shelf_file = shelve.open(str(folder_path / Path('status')))
            program_running = status_shelf_file['running']
            status_shelf_file.close()
            return program_running
        else:
            program_running = False
            return program_running'''


'''def set_program_status(self, folder_path, value):
    if self.check_shelve_file(folder_path, 'status'):
        status_shelf_file = shelve.open(str(folder_path / Path('status')))
        status_shelf_file['running'] = value
        status_shelf_file.close()
    else:
        print('\nFile does not exist, creating one')
        status_shelf_file = shelve.open(str(folder_path / Path('status')))
        status_shelf_file['running'] = value
        status_shelf_file.close()
    print('\nvalue settled')
    print('\nDone.')'''