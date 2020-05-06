from pathlib import Path


class FileHandler:
    @staticmethod
    def __check_path_traversal(
        root_dir: str or Path, relative_path: str or Path
    ) -> Path:
        """
        Check if relative path tries to reach upper directories (like "../../file")
        :param root_dir: root directory
        :param relative_path: relative to root directory
        :return: full path root_dir/relative_path
        """
        full_path = Path(root_dir).joinpath(relative_path)
        # Expect (AttributeError, ValueError) if "relative path" is not relative to root directory
        full_path.resolve().relative_to(root_dir.resolve())
        return full_path

    def upload_file(self, directory: str or Path, filename: str, body: bytes) -> None:
        """
        Upload file to directory/filename, filename will contain "body"
        :param directory: directory to upload file
        :param filename: filename to save file
        :param body: file contents
        :return: None
        """
        write_file = self.__check_path_traversal(directory, filename)
        with open(file=str(write_file), mode="wb") as file:
            file.write(body)

    def download_file(self, directory: str or Path, filename: str) -> bytes:
        """
        Returns file contents
        :param directory: directory where the file is located
        :param filename: name of the file to open
        :return: file contents
        """
        read_file = self.__check_path_traversal(directory, filename)
        with open(file=str(read_file), mode="rb") as file:
            return file.read()

    def delete_file(self, directory: str or Path, filename: str) -> None:
        """
        Delete file from particular directory by filename
        :param directory: directory where the file is located
        :param filename: name of the file to delete
        :return: None
        """
        delete_file = self.__check_path_traversal(directory, filename)
        delete_file.unlink()

    @staticmethod
    def list_files(directory: str or Path, pattern: str) -> list:
        """
        List all files in some directory
        :param directory: directory to list files
        :param pattern: pattern to match files, like "*.html" or "*.json"
        :return: list of files
        """
        return [str(file.name) for file in Path(directory).glob(pattern)]
