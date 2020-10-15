import os
from shutil import copy,copyfile
import pandas as pd
import warnings
from datetime import datetime


class FileManager(object):
    """docstring for DataProvider."""
    imported_list = []
    def __init__(self, app_dir):
        super(FileManager, self).__init__()
        self._init_directories(app_dir)
        

    def _init_directories(self, app_dir):
        """Initialization of the data directory and its subdirectories
        
        Arguments:
            appdir {str} -- The absolute path to the application root directory. All the data files will be managed under app_dir/data
        
        Raises:
            NotADirectoryError: [description]
        """
        if app_dir is None or not os.path.exists(app_dir):
            raise NotADirectoryError("Please set a valid directory path for your application")
        self.app_dir = app_dir
        self.raw_path = self._set_data_directory("raw")
        self.interim_path = self._set_data_directory("interim")
        self.processed_path = self._set_data_directory("processed")
        self.external_path =self. _set_data_directory("external")


    def save_file(self,data:pd.DataFrame, filename:str, stage="I", ext=".csv", version=None, **kwargs):
        """save a dataframe into a .csv file
        
        Arguments:
            data {Dataframe} -- a Pandas dataframe
            filename {str} -- the file name
        
        Keyword Arguments:
            stage {str} -- The data folder: (I)nterim, (P)rocessed, (R):Raw or (E)xternal (default: {"I"})
            version {int} -- the file version (default: {None})
        """
        # logger = settings.get_logger(__name__)
        try:
            if str(stage).upper().startswith("R"):
                warnings.warn("You can not save files to the RAW directory. It will be saved in the interim folder instead.\n")
                stage = "I"
            filepath = self.get_file_path(filename, stage, version)
            data.to_csv(filepath, **kwargs)
            return filepath
        except Exception:
            # logger.error(err)
            raise


    def load_file(self,filename:str, stage="I", version=None, **kwargs):
        """Loads a csv or txt file into a dataframe
        
        Arguments:
            filename {string} -- the filename to load
        
        Keyword Arguments:
            stage {str} -- The data folder: (I)nterim, (P)rocessed, (R):Raw or (M)odel (default: {"I"})
            version {int} -- The file version specified when saved (default: {1})
            sep {str} -- the separator in the file (default: {";"})
            ext {str} -- the extension of the file (default: {"csv"})
            Index {list} -- the columns to set as index to the dataframe
        
        Returns:
            Dataframe -- returns a pandas dataframe
        """
        # logger = settings.get_logger(__name__)
        try:
            filepath = self.get_file_path(filename, stage, version)
            df = pd.read_csv(filepath, **kwargs)
            return df
        except pd.errors.ParserError:
            raise Exception("The provided file:%s is not a valid csv/text file.  Please check the used separator using 'sep=' "%filepath) from None

        except UnicodeDecodeError as uni:
            o = b'\x00\x00'
            raise UnicodeDecodeError("'utf-8' codec can't decode the file. Convert the file into 'utf-8' or try with parameter encoding='ISO-8859-1' \n"
            ,o,0,0,"") from None
        except Exception:
            raise 


    def save_feather(self,df:pd.DataFrame, filename:str, stage="I", version=None, **kwargs):
        try:
            if str(stage).upper().startswith("R"):
                warnings.warn("You cannot save files to the RAW directory. It will be saved in the interim folder instead.\n")
                stage = "I"

            filepath = self.get_file_path(filename, stage, version)
            
            save = df.copy()

            if isinstance(df.index, pd.DatetimeIndex):
                save.columns = [datetime.strftime(c, "%Y-%m-%d") for c in df.columns]
            else:
                save.columns = [str(c) for c in df.columns]
            #feather index requirements
            save.reset_index().to_feather(filepath, **kwargs)
            return filepath

        except Exception:
            # logger.error(err)
            raise

    def load_feather(self,filename:str, stage="I", version=None, index_col=[0], date_columns=False, **kwargs):
        try:
            filepath = self.get_file_path(filename, stage, version)
            df = pd.read_feather(filepath, **kwargs)
            df.set_index(list(df.columns[index_col]), inplace=True)
            if date_columns:
                df.columns = pd.to_datetime(df.columns)
            return df
        except Exception:
            # logger.error(err)
            raise


    def get_file_path(self,filename, stage, version=None):
            stage = str(stage).upper().strip()[0]
            folder = {
                "R": self.raw_path,
                "I": self.interim_path,
                "P": self.processed_path,
                "E": self.external_path
            }.get(stage, self.interim_path)

            fullname = "%s_v%d" % (filename, version) if version else "%s" % (filename)

            return os.path.join(folder,fullname)

    def list_files(self,stage):
        """Return files of a given stage

        Args:
            stage (str): the stage of which files will be listed

        Returns:
            list[str]: list of file names in the given stage
        """
        folder = {
                "R": self.raw_path,
                "I": self.interim_path,
                "P": self.processed_path,
                "E": self.external_path
            }.get(stage, self.interim_path)
        files = os.listdir(folder)
        return files

    def _set_data_directory(self, foldername):
        """Returns the path of the given subdirectory. Creates it if it doesnt exist yet
        
        Arguments:
            foldername {str} -- The subdirectory folder name
        
        Returns:
            str -- The complete path to the created folder
        """
        path = os.path.join(self.app_dir, "data", foldername)

        if not os.path.exists(path):
            os.makedirs(path)

        return path
        
    @staticmethod
    def check_for_files(src, expected_files):
        """Check if the given directory contains given expected files

        Args:
            src (str): path to the directory
            expected_files (list[str]): list of file names to check for

        Returns:
            bool: True if all given files are present, False instead
        """
        all_good = True
        for expected_file in expected_files:
            file_path = os.path.join(src,expected_file)
            all_good = all_good and os.path.isfile(file_path)
        return all_good

    @classmethod
    def copy_files(cls,src, dest, listed = None, extensions = None, force_copy = False):
        """Copy the listed files from source directory to the destination

        Args:
            src (str): path to the source directory
            dest (str): path to the destination directory
            listed (List[str], optional): filter to copy only on the given list. Defaults to None.
            extensions (List[str], optional): restrict only to the given extensions. Defaults to None.
            force_copy (bool, optional): force copy if files exist. Defaults to False.

        Raises:
            fnf: File not found exception

        Returns:
            int: count of files copied
        """
        try:
            if not os.path.exists(dest):
                os.makedirs(dest)
            src_files = os.listdir(src)
            #! file names are not case sensitive
            if listed is not None:
                listed = [str(l).lower() for l in listed]
            count = 0
            for file_name in src_files:
                full_file_name = os.path.join(src, file_name)
                full_dist_name = os.path.join(dest, file_name)
                if (os.path.isfile(full_file_name)):
                        if extensions is not None and os.path.splitext(file_name)[1] not in extensions:
                            continue
                        if listed is not None and file_name.lower() not in listed:
                            continue
                        if not os.path.exists(full_dist_name) or os.stat(full_file_name).st_mtime - os.stat(full_dist_name).st_mtime > 1  or bool(force_copy):
                            copyfile(full_file_name, full_dist_name)
                            cls.imported_list.append(full_file_name)
                            count = count + 1           
            return count
        except FileNotFoundError as fnf:
            raise fnf
        except Exception:
            raise