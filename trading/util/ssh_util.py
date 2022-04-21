
import paramiko


class SSHConnection(object):

    def __init__(self, host=None, port=None, username=None, pwd=None):
        self.__host = host
        self.__port = port
        self.__username = username
        self.__pwd = pwd
        self.__transport = None
        self.__k = None

    def connect(self):
        # 创建连接对象
        transport = paramiko.Transport((self.__host, self.__port))
        transport.connect(username=self.__username, password=self.__pwd)
        self.__transport = transport

    def close(self):
        # 关闭连接
        self.__transport.close()

    def upload(self, local_path, target_path):
        """
        本地上传文件到服务器
        :param local_path: 本地文件地址
        :param target_path: 目标文件路径
        """
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        sftp.put(local_path, target_path)

    def download(self, remote_path, local_path):
        """
        服务器下载文件到本地
        :param remote_path: 服务器文件路径
        :param local_path: 本地目标路径
        """
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        sftp.get(remote_path, local_path)

    def cmd(self, command):
        """
        执行指定命令
        :param command: 命令
        :return:输入，输出，错误
        """
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh._transport = self.__transport
        # 执行命令，标准输入，输出，错误
        stdin, stdout, stderr = ssh.exec_command(command)
        # 获取命令结果
        outputs = stdout.read()
        return outputs
