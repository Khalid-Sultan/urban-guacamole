import subprocess

def extract(path):
    return subprocess.run(['ls', '-la', 'grep', path], capture_output=True, text=True)
