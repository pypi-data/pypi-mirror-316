import paramiko
import os
import getpass
import stat

class SftpClient:
    def __init__(self, host, password=None, port=22, timeout=10, IdentityFile=None):
        if "@" not in host:
            raise RuntimeError("correct host is user@ip")
        username, ip_address = host.split("@")
        if password == "input":
            password = getpass.getpass("{}'s password: ".format(host))
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        look_for_keys = password is None or len(password) == 0
        self.ssh.connect(
            hostname=ip_address,
            port=port,
            username=username,
            password=password,
            look_for_keys=look_for_keys,
            timeout=timeout,
            compress=True,
        )
        self.sftp = self.ssh.open_sftp()

    def upload(self, local_file, remote_file):
        # compare remote and local file state
        local_stat = os.stat(local_file)
        try:
            remote_stat = self.sftp.stat(remote_file)
            if local_stat.st_size == remote_stat.st_size and abs(local_stat.st_mtime - remote_stat.st_mtime) < 1.0:
                return
        except Exception as err:
            pass  # remote_file not exits, new file to upload
        print(f"upload: {local_file} -> {remote_file}")
        self.sftp.put(local_file, remote_file)
        self.sftp.utime(remote_file, (local_stat.st_atime, local_stat.st_mtime))
    
    def download(self, remote_file, local_file):
        # compare remote and local file state
        try:
            local_stat = os.stat(local_file)
            remote_stat = self.sftp.stat(remote_file)
            if remote_stat.st_size == local_stat.st_size and remote_stat.st_mtime <= local_stat.st_mtime:
                return
        except Exception as err:
            pass  # new file to download
        print(f"download: {remote_file} -> {local_file}")
        self.sftp.get(remote_file, local_file)
        
    def check_path_type(self, path):
        try:
            attr = self.sftp.stat(path)
            if stat.S_ISDIR(attr.st_mode):
                return 'folder'
            elif stat.S_ISREG(attr.st_mode):
                return 'file'
            else:
                print(f"[ERROR] remote path is not directory or file: {path}")
                return None
        except Exception as err:
            print(f"[ERROR] remote not exits: {path}")
            return None
        
    def create_remote_directory(self, remote_dir):
        try:
            self.sftp.stat(remote_dir)
        except Exception as err:
            path, folder = os.path.split(remote_dir)
            self.create_remote_directory(path)
            self.sftp.mkdir(remote_dir)
            
    def exists(self, remote_path):
        try:
            self.sftp.stat(remote_path)
            return True
        except Exception as err:
            return False
            
    def close(self):
        self.sftp.close()
        self.ssh.close()
    
    def __del__(self):
        try:
            self.close()
        except Exception as err:
            pass