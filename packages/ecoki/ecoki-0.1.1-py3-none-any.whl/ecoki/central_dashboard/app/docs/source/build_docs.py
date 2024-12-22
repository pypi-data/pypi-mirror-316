import os
import subprocess

def build_docs():
    subprocess.check_call(['poetry', 'run', 'sphinx-build', '-b', 'html', './source/', '_build/html'])
    #subprocess.check_call(['poetry', 'run', 'sphinx-build', '-b', 'html', '.', '_build/html'])

if __name__ == '__main__':
    build_docs()
