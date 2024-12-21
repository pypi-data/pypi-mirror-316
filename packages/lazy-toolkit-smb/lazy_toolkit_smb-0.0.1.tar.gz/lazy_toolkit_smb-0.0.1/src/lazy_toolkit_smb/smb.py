import os
from io import BufferedReader, BufferedWriter, TextIOWrapper
from logging import Logger

from smbclient import (ClientConfig, copyfile, mkdir, open_file, remove,
                       rename, rmdir, scandir)
from smbclient.path import exists, isdir
from smbprotocol.exceptions import SMBOSError


class SmbOperator:
    """Wrapper for SMB operations
    """

    # SMB is a Windows-based protocol, so the path separator is '\' by default
    SeparatorSmb: str = '\\'
    SeparatorPOSIX: str = '/'
    SeparatorStrip: str = '/\\'

    def __init__(self, server: str, username: str, password: str, smb_root: str, logger: Logger | None = None):
        # SMB root path, e.g.: \\192.168.1.1\myRoot
        self.smb_root_path: str = f'\\\\{server}\\{smb_root}'
        self.logger: Logger | None = logger

        # Register server, smbclient.ClientConfig is a global singleton config for all SMB operations
        try:
            ClientConfig(client_guid=None, username=username, password=password)
        except Exception as e:
            if self.logger:
                self.logger.error(f'Failed to register SMB session on server {server}: {e}')
            raise e

        if self.logger:
            self.logger.info(f'Registered SMB session on server: {server}, SMB sharing root: {smb_root}')

    """
    Path operations
    """

    def isdir(self, path: str) -> bool:
        """Check if given relative path is an existing directory
        """
        if not path:
            return False

        return isdir(os.path.join(self.smb_root_path, path))

    def mkdir(self, path: str) -> bool:
        """Make a directory

        Args:
            path (str): The path to the directory, relative to the root. If the path is nested, then the parent folder
            of the directory MUST exist. To create nested directory with non-existed parent folder, use `mkpath` instead.
        """
        if not path:
            return False

        try:
            mkdir(os.path.join(self.smb_root_path, path))
            return True
        except SMBOSError as e:
            if e.errno == 17:
                # Directory already exists
                return True

            if self.logger:
                self.logger.error(f'Failed to create folder "{path}": {e}')
            return False

    def ensure_dir(self, path: str) -> bool:
        """Ensure a directory exists
        - If the directory does not exist, create it
        """
        if not path:
            return False

        if self.isdir(path):
            return True

        return self.mkdir(path)

    def mkpath(self, path: str, path_sep: str = SeparatorPOSIX) -> bool:
        """Make a path of directories
        - If the parent folder of the directory does not exist, create it
        """
        if not path:
            return False

        path_splitted: list[str] = path.split(path_sep)
        curpath: str = ''
        for folder in path_splitted:
            curpath = os.path.join(curpath, folder)
            if not self.mkdir(curpath):
                if self.logger:
                    self.logger.error(f'Failed to create path "{path}", failed at create folder "{curpath}"')
                return False

        return True

    def ensure_path(self, path: str, path_sep: str = SeparatorPOSIX) -> bool:
        """Ensure a path exists
        - If the path does not exist, create it
        """
        if not path:
            return False

        if self.isdir(path):
            return True

        return self.mkpath(path, path_sep)

    def rmdir(self, path: str) -> bool:
        """Delete a directory

        Args:
            path (str): The path to the directory, relative to the root. Only empty directory can be deleted
        """
        if not path:
            return True

        try:
            rmdir(os.path.join(self.smb_root_path, path))
            return True
        except Exception as e:
            if self.logger:
                self.logger.error(f'Failed to remove folder "{path}": {e}')
            return False

    def listdir(self,
                path: str,
                include_files: bool = False,
                include_dirs: bool = False,
                name_only: bool = True) -> list[str]:
        """List directory content

        Args:
            path (str): The path to the directory, relative to the root
            include_files (bool, optional): Whether to include files in the list. Defaults to True.
            include_dirs (bool, optional): Whether to include directories in the list. Defaults to False.
            name_only (bool, optional): Whether to list only file names. Defaults to True, otherwise list full path
        """
        res: list[str] = list()
        if not include_dirs and not include_files:
            return res

        try:
            for item in scandir(os.path.join(self.smb_root_path, path)):
                if (include_files and item.is_file()) or (include_dirs and item.is_dir()):
                    res.append(item.name) if name_only else res.append(item.path)
            return res
        except Exception as e:
            if self.logger:
                self.logger.error(f'Failed to list directory content "{path}": {e}')
            return res

    """
    File operations
    """

    def isfile(self, path: str) -> bool:
        """Check if given relative path is a file
        - There is no `smbclient.isfile` method so check if the path exists and is NOT a directory
        """
        if not path:
            return False

        if exists(os.path.join(self.smb_root_path, path)):
            return not self.isdir(path)
        return False

    def read_file(self, path: str, byte_mode: bool = False) -> bytes | str | None:
        """Read a remote file's content and return it

        Args:
            r_target_path (str): The path to the file
            byte_mode (bool, optional): Whether to read the file in bytes. Defaults to False.
        """
        if not self.isfile(path):
            return None

        try:
            mode: str = 'rb' if byte_mode else 'r'
            with open_file(os.path.join(self.smb_root_path, path), mode=mode) as f_reader:
                # The type of `f_reader` depends on if `byte_mode` is True or False
                # - If `byte_mode` then it is BufferedReader, otherwise is TextIOWrapper
                typed_reader: BufferedReader | TextIOWrapper = f_reader  # type: ignore
                file_content_str: bytes | str | None = typed_reader.read()
                return file_content_str
        except Exception as e:
            if self.logger:
                self.logger.error(f'Failed to read file "{path}": {e}')
            return None

    def create_file(self,
                    path: str,
                    content: bytes | str,
                    byte_mode: bool = True,
                    overwrite: bool = True) -> bool:
        """Create a remote file with content

        Args:
            r_target_path (str): The path to the file
            content (bytes | str): The content to write to the file
            byte_mode (bool, optional): Whether to write the content in bytes. Defaults to False.
                - If `byte_mode`, then type of content should be provided as bytes
            overwrite (bool, optional): Whether to overwrite the file if it already exists. Defaults to True.
        """
        if self.isfile(path):
            if not overwrite:
                if self.logger:
                    self.logger.warning(f'Cannot create file "{path}": file already exists')
                return False

        overwrite_msg: str = '(overwrite) ' if overwrite else ''
        try:
            mode: str = 'wb' if byte_mode else 'w'
            with open_file(os.path.join(self.smb_root_path, path), mode=mode) as f_writer:
                # The type of `f_writer` depends on if `byte_mode` is True or False
                # - If `byte_mode` then it is BufferedWriter, otherwise is TextIOWrapper
                typed_writer: BufferedWriter | TextIOWrapper = f_writer  # type: ignore
                typed_writer.write(content)  # type: ignore

            return True

        except Exception as e:
            if self.logger:
                self.logger.error(f'Failed to create {overwrite_msg}file "{path}": {e}')
            return False

    def create_file_from_local(self,
                               local_file_path: str,
                               path: str,
                               byte_mode: bool = True,
                               overwrite: bool = False) -> bool:
        """Create a remote file with the content of given source file on local

        Args:
            f_source_path (str): The path to the file on local machine
            r_target_path (str): The path to the file on SMB server, relative to the SMB_ROOT
            byte_mode (bool, optional): Whether to write the content in bytes. Defaults to False.
                - If `byte_mode`, then type of content should be provided as bytes
            overwrite (bool, optional): Whether to overwrite the file if it already exists. Defaults to False.
        """
        overwrite_msg: str = '(overwrite) ' if overwrite else ''
        try:
            r_mode: str = 'rb' if byte_mode else 'r'
            res: bool = self.create_file(path, open(local_file_path, r_mode).read(), byte_mode, overwrite)
            return res
        except Exception as e:
            if self.logger:
                self.logger.error(
                    f'Failed to create {overwrite_msg}file "{path}" from local file "{local_file_path}" as source content: {e}')
            return False

    def append_to_file(self, path: str, content: bytes | str, byte_mode: bool = False) -> bool:
        """Append content to a remote file

        Args:
            r_target_path (str): The path to the file
            content (bytes | str): The content to write to the file
            byte_mode (bool, optional): Whether to write the content in bytes. Defaults to False.
                - If `byte_mode`, then type of content should be provided as bytes
        """
        try:
            mode: str = 'ab' if byte_mode else 'a'
            with open_file(os.path.join(self.smb_root_path, path), mode=mode) as f_writer:
                typed_writer: BufferedWriter | TextIOWrapper = f_writer  # type: ignore
                typed_writer.write(content)  # type: ignore

            return True

        except Exception as e:
            if self.logger:
                self.logger.error(f'Failed to append content to file "{path}": {e}')
            return False

    def delete_file(self, path: str) -> bool:
        try:
            remove(os.path.join(self.smb_root_path, path))
            return True
        except FileNotFoundError as e:
            # File not found, do nothing
            return True
        except Exception as e:
            if self.logger:
                self.logger.error(f'Failed to delete file "{path}": {e}')
            return False

    def rename_file(self, old_path: str, new_path: str) -> bool:
        try:
            rename(os.path.join(self.smb_root_path, old_path), os.path.join(self.smb_root_path, new_path))
            return True
        except Exception as e:
            if self.logger:
                self.logger.error(f'Failed to rename file {old_path} -> {new_path}: {e}')
            return False

    def backup_file(self, path: str) -> bool:
        """Backup a remote file by copying it to a new file with a different name
        - E.g.: "xxx/file.txt" -> "xxx/file.txt.bak"
        """
        if not self.isfile(path):
            return False

        try:
            copyfile(os.path.join(self.smb_root_path, path), os.path.join(self.smb_root_path, f'{path}.bak'))
            return True
        except Exception as e:
            if self.logger:
                self.logger.error(f'Failed to backup file "{path}": {e}')
            return False

    def has_backup(self, path: str) -> bool:
        """Check if a backup file exists for a given file
        """
        return self.isfile(f'{path}.bak')

    def delete_backup(self, path: str) -> bool:
        """Delete the backup file of a given file
        """
        return self.delete_file(f'{path}.bak')

    def recover_backup(self, path: str) -> bool:
        """Recover a backup file to its original file
        """
        # Ensure the original file does not exist before recovering
        self.delete_file(path)
        return self.rename_file(f'{path}.bak', path)
