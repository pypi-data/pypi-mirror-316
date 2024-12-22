import paramiko
import os
import getpass
from .remote_manager import RemoteDeviceManager
from .sftp_client import SftpClient

class SftpUploadTransport:
    def __init__(self, host, password=None, port=22,
                 exclude=None, IdentityFile=None):
        self.sftp = SftpClient(host, password, port, timeout=10, IdentityFile=IdentityFile)
        # exclude hints
        self.enable_exclude_hint = True if exclude else False
        self.exclude_file_list = []  # 绝对路径
        self.exclude_paths = []
        if self.enable_exclude_hint:
            for hint in exclude:
                assert len(hint) >= 2, 'too short hint'
                if os.path.isfile(hint):
                    self.exclude_file_list.append(os.path.abspath(hint))
                else:
                    self.exclude_paths.append(hint)
            info_str = "exclude:"
            for p in self.exclude_file_list:
                info_str += "\n  " + p
            for p in self.exclude_paths:
                info_str += "\n  " + p
            print(info_str)

    def check_exclude_file(self, local_file_path, file):
        """priority is file list > path > extension """
        if not self.enable_exclude_hint:
            return 0
        if local_file_path in self.exclude_file_list:
            return 1
        for path_regex in self.exclude_paths:
            key, ext = path_regex, None
            if "*" in path_regex:
                key, ext = path_regex.split("*")
                # print(key, ext, local_file_path)
            if key in local_file_path:
                if ext:
                    _, extension = os.path.splitext(file)
                    if extension == ext:
                        return 1
                else:
                    return 1
        return 0

    def put(self, local_paths, remote_root, allow_creating_remote_dir=False):
        if allow_creating_remote_dir:
            self.sftp.create_remote_directory(remote_root)
        else:
            if not self.sftp.exists(remote_root):
                self.sftp.close()
                print("[Error] remote not exists:", remote_root)
                exit(1)  # Did not exit as expected

        assert isinstance(local_paths, list)
        for path in local_paths:
            path = path.rstrip('/')  # drop right slash of path
            # path is a file
            if os.path.isfile(path):
                root, file = os.path.split(path)
                remote_file_path = os.path.join(remote_root, file)
                self.sftp.upload(path, remote_file_path)
            elif os.path.isdir(path):
                path = os.path.abspath(path)
                for root, dirs, files in os.walk(path):
                    for file in files:
                        local_file_path = os.path.join(root, file)
                        if self.check_exclude_file(local_file_path, file):
                            continue
                        remote_file_path = os.path.join(remote_root,
                                                        os.path.relpath(local_file_path, os.path.dirname(path)))
                        self.sftp.create_remote_directory(os.path.dirname(remote_file_path))
                        self.sftp.upload(local_file_path, remote_file_path)
            else:
                print('[Error] not exist:', path)
                
def config_parser(sub_parsers):
    p = sub_parsers.add_parser("put", help="copy files to remote with sftp")
    p.add_argument('remote', type=str, help='remote_name, usrname@ip_address')
    p.add_argument('paths', nargs='+', help='path1 path2 ..., the last is remote_root')
    p.add_argument('--password', type=str, help='specify or [input]')
    p.add_argument('-p', '--port', type=int, help='remote port', default=22)
    p.add_argument('--exclude', nargs='+', type=str, default=None, help='paths, files or extensions to filter')
    p.set_defaults(func=execute)

def execute(args):
    """api for copy files by sftp transformer"""
    assert len(args.paths) >= 2, 'need at least one local path and  one remote path separately'
    remote_manager = RemoteDeviceManager()
    device = remote_manager.get_device(args.remote, args.port)
    host, password, port, IdentityFile = args.remote, args.password, args.port, None
    if device is not None:
        host, password, port, IdentityFile = device.host, device.password, device.port, device.IdentityFile
    transport = SftpUploadTransport(
        host=host,
        password=password,
        port=port,
        exclude=args.exclude,
        IdentityFile=IdentityFile)
    transport.put(local_paths=args.paths[:-1], remote_root=args.paths[-1])
