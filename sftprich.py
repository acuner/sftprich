# -*- coding: utf-8 -*-
from paramiko import SFTPClient
from paramiko.channel import Channel
from paramiko.sftp_attr import SFTPAttributes
import os
from rich.progress import Progress, TaskID

class SftpRich(SFTPClient):
    def __init__(self, sock: Channel) -> None:
        super().__init__(sock)
        self.proc = None
        self.task = None

    def richer(self, proc:Progress, task:TaskID):
        self.proc = proc
        self.task = task

    def _transfer(self, reader, writer, file_size):
        size = 0
        self.proc.start_task(self.task)
        while True and not self.proc.finished:
            data = reader.read(32768)
            writer.write(data)
            size += len(data)
            if len(data) == 0:
                break
            self.proc.update(self.task, completed=size, total=file_size)
            # self.proc.update(task, advance=len(data), total=file_size)

        return size

    def put(self, localpath, remotepath, confirm=True):
        file_size = os.stat(localpath).st_size
        with open(localpath, "rb") as fl:
            with self.file(remotepath, "wb") as fr:
                fr.set_pipelined(True)
                size = self._transfer(reader=fl, writer=fr, file_size=file_size)
            if confirm:
                s = self.stat(remotepath)
                if s.st_size != size:
                    raise IOError("size mismatch in put!  {} != {}".format(s.st_size, size))
            else:
                s = SFTPAttributes()
            return s
