import os
import magic
from typing import List
import re
import yaml

class Device:
    def __init__(self, name, ip, username, password, port=22, IdentityFile=None, description=None):
        self.name = name
        self.ip = ip
        self.username = username
        assert isinstance(password, str)
        self.password = password
        self.port = int(port)
        self.IdentityFile = IdentityFile
        self.description = description

    @property
    def host(self):
        return self.username + '@' + self.ip

    def __repr__(self):
        string = str(self.name) + ':\n'
        string += '  ip: {}\n'.format(self.ip)
        string += '  username: {}\n'.format(self.username)
        if self.password:
            string += '  password: {}\n'.format(self.password)
        if self.port:
            string += '  port: {}\n'.format(self.port)
        if self.IdentityFile:
            string += '  IdentityFile: {}\n'.format(self.IdentityFile)
        if self.description:
            string += '  description: {}\n'.format(self.description)
        return string

class RemoteDeviceManager:
    def __init__(self):
        self.remote_devices: List[Device] = []
        self.default_port = 22
        self.remote_config_file = os.path.join(magic.config_root, '.remote_device.conf')

        if not os.path.exists(self.remote_config_file):
            # create a template of config file
            os.makedirs(magic.config_root, exist_ok=True)
            device = Device('sample', '192.168.1.10', 'username', 'password', 2008, '~/.ssh/id_rsa.pub', 'description')
            self.remote_devices.append(device)
            self.dump_device_conf()
        else:
            self.load_device_conf()

    def list_all_devices(self):
        msg_fmt = '{:<3} {:<25} {} \t {}'
        print(msg_fmt.format('Id', 'Name', 'ssh_cmd', ''))
        device_list = sorted(self.remote_devices, key=lambda x: x.name, reverse=False)
        for id, device in enumerate(device_list):
            if device.port == self.default_port:
                ssh_cmd = f"ssh {device.username}@{device.ip}"
            else:
                ssh_cmd = f"ssh -p {device.port} {device.username}@{device.ip}"
            if device.description is None:
                device.description = ''
            msg = msg_fmt.format(id, device.name[:25], ssh_cmd, device.description)
            print(msg)
        return device_list

    def get_device(self, key, port=22):
        """ get device by name, host """
        if key.isdigit():
            return self.remote_devices[int(key)]
        for device in self.remote_devices:
            if key == device.name:
                return device 
            if key == device.host and port == device.port:
                return device
        return None

    def dump_device_conf(self):
        # dump device config to remote_device.pt
        all_device_conf = {}
        with open(self.remote_config_file, 'w+') as f:
            for device in self.remote_devices:
                ssh_cmd = 'ssh'
                if device.port != self.default_port:
                    ssh_cmd += ' -p {}'.format(device.port)
                ssh_cmd += ' {}@{}'.format(device.username, device.ip)
                device_conf = {'ssh_cmd': ssh_cmd}
                if device.password:
                    device_conf['password'] = device.password
                if device.description:
                    device_conf['info'] = device.description
                if device.IdentityFile:
                    device_conf['IdentityFile'] = device.IdentityFile
                all_device_conf[device.name] = device_conf
            yaml.dump(all_device_conf, f)

    def load_device_conf(self):
        with open(self.remote_config_file, 'r') as f:
            all_device_conf = yaml.safe_load(f)
        for machine, conf in all_device_conf.items():       
            stat, results = self.parse_ssh_command(conf['ssh_cmd'])
            if not stat:
                raise RuntimeError("failed to load conf: {}".format(machine))
            device = Device(
                name=machine,
                ip=results['ip'],
                username=results['user'],
                password=conf.get('password'),
                port=results.get('port', self.default_port),
                description=conf.get('info'),
                IdentityFile=conf.get('IdentityFile')
            )
            assert len(device.name), 'device name is empty'
            assert len(device.ip), 'device ip is empty'
            assert len(device.username), 'device username is empty'
            for device_registered in self.remote_devices:
                if device.name == device_registered.name:
                    raise RuntimeError("device already exists, name: ".format(device.name))
            self.remote_devices.append(device)

        if not self.remote_devices:
            print('[WARN] {} is empty'.format(self.remote_config_file))

    def parse_ssh_command(self, command):
        # 定义一个匹配模式，用于解析SSH命令
        pattern = r'ssh\s+-p\s*(\d+)\s*([\w-]+)@([\d.]+)'
        match = re.search(pattern, command)
        if match:
            port = match.group(1)
            user = match.group(2)
            ip = match.group(3)
            return True, {'port': port, 'user': user,'ip': ip}
        else:
            # 如果没有指定端口，则尝试匹配不带端口的模式
            pattern_no_port = r'ssh\s+([\w-]+)@([\d.]+)'
            match_no_port = re.search(pattern_no_port, command)
            if match_no_port:
                user = match_no_port.group(1)
                ip = match_no_port.group(2)
                return True, {'user': user, 'ip': ip}
            else:
                return False, {}