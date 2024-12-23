import os

from paramiko import SSHClient, SSHConfig, AutoAddPolicy



class CmdHelper:
    def __init__(self, host: str = 'selfhosthelper', user: str = '', password: str = ''):
        self.host: str = host
        self.user: str = user
        self.password: str = password
        self.default_ssh_conf: SSHConfig = self.load_ssh_config()
        self.client: SSHClient = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())

    @staticmethod
    def load_ssh_config(default_ssh_config_path: str = "~/.ssh/config") -> SSHConfig:
        ssh_config = SSHConfig()
        user_config_file = os.path.expanduser(default_ssh_config_path)
        if os.path.exists(user_config_file):
            with open(user_config_file) as f:
                ssh_config.parse(f)
        return ssh_config

    def connect(self):
        config = self.default_ssh_conf.lookup(self.host)

        assert config, 'You must set host to your ~/.ssh/config'

        if not self.user and 'user' in config:
            self.user = config['user']

        if self.host == 'selfhosthelper':
            self.host = config['hostname']

        if config and 'identityfile' in config:
            self.client.load_system_host_keys()
            self.key_filename = config['identityfile'][0]

        try:
            if self.password:
                self.client.connect(self.host, username=self.user, password=self.password)
            elif self.user and self.key_filename:
                self.client.connect(self.host, username=self.user, key_filename=self.key_filename)
            else:
                self.client.connect(self.host)
            print(f"Connected to {self.host}")
        except Exception as e:
            print(f"Connection failed: {e}")
            exit(1)

    def execute_command(self, command) -> (int, str, str):
        try:
            self.connect()
            print(f'Send command: {command}')
            if command.startswith('su ') or command.startswith('sudo -i'):
                raise NameError('You should implement it.')
                stdin, stdout, stderr = self.client.exec_command(command)
                stdin.write(f'{self.password}\n')
                stdin.flush()
                data = stdout.read.splitlines()
                for line in data:
                    if line.split(':')[0] == 'AirPort':
                        print(line)

            else:
                stdin, stdout, stderr = self.client.exec_command(command)
            exit_status = stdout.channel.recv_exit_status()
            output = stdout.read().decode()
            error = stderr.read().decode()
            print("Exit status:", str(exit_status))
            print("Output:", output)
            print("Error:", error)
            return exit_status, output, error
        except Exception as e:
            print(f"Command execution failed: {e}")
            return 1, None, str(e)
        finally:
            self.disconnect()

    def disconnect(self):
        self.client.close()
        print(f"Disconnected from {self.host}")

    def run_cmd(self, command) -> (int, str, str):
        exit_status, output, error = self.execute_command(command)
        return exit_status, output, error

    def run_locally(self, cmd):
        os.system(cmd)


if __name__ == "__main__":
    runner = CmdHelper()
    status, out, err = runner.execute_command('ifconfig')
