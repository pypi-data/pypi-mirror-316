import paramiko
import os
import getpass
import yaml
from .sftp_put import SftpUploadTransport


def config_parser(sub_parsers):
    p = sub_parsers.add_parser("deploy", help="deployment helper")
    p.add_argument("relative_paths", nargs="+", help="path1 path2 ...")
    p.set_defaults(func=execute)

def execute(args):
    workspaceFolder = os.getcwd()
    config_file = os.path.join(workspaceFolder, ".vscode/rsync.yaml")
    if not os.path.exists(config_file):
        raise FileNotFoundError("Not found config '{}'".format(config_file))
    with open(config_file, "r") as f:
        conf = yaml.safe_load(f)
    assert "host" in conf
    assert "remote_root" in conf
    assert "local_root" in conf and conf["local_root"] == workspaceFolder
    
    deploy(local_root=conf['local_root'],
           remote_root=conf['remote_root'],
           host=conf['host'],
           relative_paths=args.relative_paths,
           password=conf.get('password', None),
           port=conf.get('port', 22),
           exclude=conf.get('exclude', None)
           )

def deploy(local_root, remote_root, host=None, relative_paths=None, password=None, port=22, exclude=None):
    client = SftpUploadTransport(host, password, port, exclude)
    if relative_paths is None:
        relative_paths = ['./']
    if relative_paths[0] in ['./', '.']:
        relative_paths = os.listdir('./')
    
    for rpath in relative_paths:
        os.path.exists(rpath), f"not exist: {rpath}"
        relpath = os.path.relpath(os.path.abspath(rpath), local_root)
        remote_root = os.path.dirname(os.path.join(remote_root, relpath))
        client.put([relpath], remote_root, True)