import os
from subprocess import Popen, PIPE

class ComposeManager:
    def __init__(self, base_dir):
        self.base_dir = base_dir

    def build(self, dir, env=None):
        cmd = "sudo docker compose up --build --detach"
        return self._run_command_from_dir(cmd, dir, env)
    
    def stop(self, dir, env=None):
        cmd = "sudo docker compose down"
        return self._run_command_from_dir(cmd, dir, env)

    def _run_command_from_dir(self, cmd, dir, env):
        proc = Popen(cmd,
            cwd=os.path.join(self.base_dir, dir),
            stdout=PIPE,
            stderr=PIPE,
            env=env,
            shell=True)
        
        proc.wait()

        stdout, stderr = proc.communicate()
        
        return (proc.returncode, stdout, stderr)
    
if __name__ == '__main__':
    base_dir = '/home/user/source/repos'
    dir = 'scoreserver'

    cm = ComposeManager(base_dir)

    rc, stdout, stderr = cm.build(dir)
    print(rc, stdout, stderr)
    assert(rc==0)

    rc, stdout, stderr = cm.stop(dir)
    print(rc, stdout, stderr)
    assert(rc==0)