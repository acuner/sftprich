# -*- coding: utf-8 -*-
import paramiko
from sftprich import SftpRich
import os
from rich.progress import (
    TextColumn,
    DownloadColumn,
    BarColumn,
    Progress,
    TaskID,
    TimeRemainingColumn,
    TransferSpeedColumn,
)
from concurrent.futures import ThreadPoolExecutor

zpdir = 'c:\\julia\\zipdeal\\'
id_rsa = 'c:\\Users\\hdusr\\.ssh\\id_rsa'

attr = {
    'host': 'dsj-oa.cmsc.tech',  
    'port': 29022, # 服务端口号, 根据环境自行设置
    'user': 'ywy',
    'target': '/home/ywy/julia/alpha/',
}


def ftp(local, remoter, proc:Progress, xthRar: TaskID):
    private_key = paramiko.RSAKey.from_private_key_file(id_rsa)
    trp = paramiko.Transport((attr['host'], attr['port']))
    trp.connect(username=attr['user'], pkey=private_key)

    sftp = SftpRich.from_transport(trp)
    sftp.richer(proc, xthRar)
    sftp.put(local, remoter)
    sftp.close()

if __name__ == '__main__':
    # 本地路径rar文件的选择，xx 文件名的长度
    rars = [k for k in os.listdir(zpdir) if k[:10]=='myrar.part' and k[-4:]=='.rar']

    progress = Progress(
        TextColumn("[bold blue]uploading {task.fields[filename]}", justify="right"),
        # TextColumn("[bold blue]uploading", justify="right"),
        # BarColumn(bar_width=None),
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.1f}%",
        ".",
        DownloadColumn(),
        ".",
        TransferSpeedColumn(),
        ".",
        TimeRemainingColumn(),
    )
    with progress:
        with ThreadPoolExecutor(len(rars)) as p:
            for xth in range(len(rars)):
                aLocal = zpdir+'myrar.part'+str(xth+1).zfill(2)+'.rar'
                aRemoter = attr['target'] + 'myrar.part'+str(xth+1).zfill(2)+'.rar'
                tsk = progress.add_task('uploading...', filename=aLocal.split('\\')[-1], start=False)
                p.submit(ftp, aLocal, aRemoter, progress, tsk)
