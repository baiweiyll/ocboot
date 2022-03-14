# encoding: utf-8
import logging
import subprocess

from . import logger


logger = logger.new(__name__)


class StderrException(Exception):
    pass


class SSHClient(object):

    def __init__(self, host, user, private_key_f, port=22):
        self.host = host
        self.port = port
        self.user = user
        self.private_key_file = private_key_f
        self.client = self.new_ssh_client()

    def get_host(self):
        return self.host

    def get_user(self):
        return self.user

    def get_port(self):
        return self.port

    def get_private_key_file(self):
        return self.private_key_file

    def new_ssh_client(self):

        def cli_w(cmd):
            user_host = "%s@%s" % (self.get_user(), self.get_host())
            args = ["ssh",
                    "-o", "LogLevel=error",
                    "-o", "StrictHostKeyChecking=no",
                    "-o", "UserKnownHostsFile=/dev/null",
                    "-o", "ForwardX11=no",
                    "-i", self.get_private_key_file(),
                    user_host]
            print("%s" % ' '.join(args))
            ssh = subprocess.Popen(args,
                                   shell=False,
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
            stdout, stderr = ssh.communicate(cmd.encode('utf-8'))
            out = stdout.decode('utf-8')
            err = stderr.decode('utf-8')
            return out, err

        return cli_w

    # def new_ssh_client(self):
    #     import paramiko
    #
    #     k = paramiko.RSAKey.from_private_key_file(self.private_key_file)
    #     c = paramiko.SSHClient()
    #     c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #     c.connect(
    #         hostname=self.host,
    #         port=self.port,
    #         username=self.user,
    #         pkey=k,
    #         banner_timeout=60,
    #         timeout=60)
    #     return c

    def exec_command(self, command):
        command = '%s %s' % ('[ -s /etc/kubernetes/admin.conf ] && export KUBECONFIG=/etc/kubernetes/admin.conf || :;', command)
        logger.info("exec_command: %s" % command)
        # _, stdout, stderr = self.client.exec_command(command)
        out, err = self.client(command)
        if err:
            raise StderrException(err)
        return out
