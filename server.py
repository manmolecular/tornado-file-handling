#!/usr/bin/env python3

from mimetypes import guess_type
from pathlib import Path

import tornado.options
from tornado import web, ioloop
from tornado.log import gen_log

from core.filehandler import FileHandler as FileHelper


class Config:
    file_directory = Path("files")


class FileHandler(web.RequestHandler):
    file_helper = FileHelper()

    def set_default_headers(self) -> None:
        self.set_header("Content-Type", "application/json")

    def __error(self, error_msg: str):
        """
        Define error messages
        :param error_msg: error message
        :return: None
        """
        self.set_status(500)
        gen_log.error(error_msg)
        self.write({"status": "error", "description": error_msg})

    def __success(self, success_msg: str):
        """
        Define success messages
        :param success_msg: success message
        :return: None
        """
        gen_log.info(success_msg)
        self.write({"status": "success", "description": success_msg})

    async def post(self):
        """
        Upload files from user
        :return: None
        """
        files_meta = [
            file_meta
            for files_content in self.request.files.values()
            for file_meta in files_content
        ]
        err_files = []
        for file_meta in files_meta:
            filename = file_meta.get("filename")
            file_body = file_meta.get("body")
            try:
                self.file_helper.upload_file(
                    Config.file_directory,
                    filename,
                    file_body,
                )
            except (AttributeError, ValueError) as path_err:
                gen_log.error(f"Wrong path and/or filename: {str(path_err)}")
                err_files.append(filename)
                continue
            except Exception as file_err:
                gen_log.error(f"File error: {str(file_err)}")
                err_files.append(filename)
                continue
        if err_files:
            self.__error(f"The following files have not been uploaded: {', '.join(err_files)}")
            return
        self.__success("Files uploaded successfully")

    async def get(self):
        """
        Serve files from server
        :return: None
        """
        filename = self.get_argument("filename", None)
        if not filename:
            file_list = self.file_helper.list_files(Config.file_directory, "*")
            self.write(dict(files=file_list))
            return
        try:
            # fmt: off
            file = self.file_helper.download_file(Config.file_directory, filename)
            content_type = guess_type(url=filename, strict=False)[0] or "application/force-download"
            self.set_header("Content-Type", content_type)
            self.set_header("Content-Disposition", f"attachment; filename={filename}")
            self.write(file)
            # fmt: on
        except (AttributeError, ValueError) as path_err:
            self.__error(error_msg=f"Wrong path and/or filename: {str(path_err)}")
            return
        except Exception as file_err:
            self.__error(error_msg=f"File error: {str(file_err)}")
            return

    async def delete(self):
        """
        Delete some file on server
        :return: None
        """
        filename = self.get_argument("filename", None)
        try:
            self.file_helper.delete_file(Config.file_directory, filename)
        except Exception as file_err:
            self.__error(error_msg=f"File error: {str(file_err)}")
            return
        self.__success(success_msg=f"File {filename} has been deleted")


def make_app():
    Config.file_directory.mkdir(parents=True, exist_ok=True)
    # fmt: off
    return web.Application(
        handlers=[
            (r"/api/file", FileHandler)
        ]
    )
    # fmt: on


if __name__ == "__main__":
    tornado.options.parse_command_line()
    gen_log.info("Server running")

    app = make_app()
    app.listen(8888)

    ioloop.IOLoop.current().start()
