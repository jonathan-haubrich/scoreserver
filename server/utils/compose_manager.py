import os
import re
from subprocess import Popen, PIPE
import tempfile

class ComposeManager:
    def __init__(self, base_dir):
        self.base_dir = base_dir

    def build(self, dir, env=None):
        cmd = "sudo docker compose up --build --detach"
        
        if env is not None:
            tmp_file = self._setup_env_file(env)
            cmd = f"sudo docker compose --env-file {tmp_file.name} up --build --detach"

        ret = self._run_command_from_dir(cmd, dir, env)

        tmp_file.close()

        return ret
    
    def stop(self, dir, env=None):
        cmd = "sudo docker compose down"
        return self._run_command_from_dir(cmd, dir, env)

    def port(self, dir, container):
        cmd = f"sudo docker port {container}"
        return self._run_command_from_dir(cmd, dir, None)

    def _run_command_from_dir(self, cmd, dir, env):
        print(cmd, dir, env)
        proc = Popen(cmd,
            cwd=os.path.join(self.base_dir, dir),
            stdout=PIPE,
            stderr=PIPE,
            env=env,
            shell=True)
        
        proc.wait()

        stdout, stderr = proc.communicate()
        
        return (proc.returncode, stdout, stderr)
    
    def _setup_env_file(self, env):
        # Create a temporary file in the current working directory
        tmp_file = tempfile.NamedTemporaryFile(mode='w')

        lines = [f"{key}={value}\n" for key, value in env.items()]

        tmp_file.writelines(lines)
        tmp_file.flush()

        return tmp_file
    
if __name__ == '__main__':
    base_dir = '/home/user/source/repos'
    dir = 'scoreserver'

    cm = ComposeManager(base_dir)

    rc, stdout, stderr = cm.build(dir, env={"USERNAME":"envuser","PASSWORD":"envpass"})
    print(rc, stdout.decode(), stderr)
    assert(rc==0)

    rc, stdout, stderr = cm.port(dir, "scoreserver-student")
    print(rc, stdout.decode(), stderr)

    output = stdout.decode()
    matches = re.search(r"\d+/tcp -> \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:(\d+)", output)
    port = matches.groups()[0]
    print(port)

    assert(rc==0)

    rc, stdout, stderr = cm.stop(dir)
    print(rc, stdout, stderr)
    assert(rc==0)