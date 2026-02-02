import os
from os.path import expanduser as eu, dirname, exists, join as pjoin
from time import time
from subprocess import run
import shutil
import sys

backup = False


def _makedirs(dirs):
    # Create the folder in case it doesn't exist.
    try:
        os.makedirs(dirs)
    except OSError as e:
        if e.errno != 17:  # 17 means directory already exists
            raise


def link_with_backup(source, link_name, method="symlink"):
    link_name = eu(link_name)
    source = eu(source)
    print('Installing ' + source + ' -> ' + link_name)

    _makedirs(dirname(link_name))

    def _dolink():
        if method == "symlink":
            os.symlink(source, link_name)
        elif method == "hardlink":
            os.link(source, link_name)
        elif method == "copy":
            shutil.copy(source, link_name)
        else:
            raise ValueError("Bug!!")

    try:
        _dolink()
    except OSError:
        if backup:
            os.rename(link_name, f'{link_name}.{int(time())}.dotfiles_backup')
        else:
            # Try to remove this thing. Non-empty directories don't work yet.
            try:
                os.remove(link_name)
            except OSError as e:
                os.rmdir(link_name)
        _dolink()


def here(f):
    import inspect
    me = inspect.getsourcefile(here)
    return pjoin(os.path.dirname(os.path.abspath(me)), f)


def here_to_home(name, toname=None, method="symlink"):
    link_with_backup(here('_' + name), '~/.' + (toname if toname else name), method=method)


def main(mode):
    if mode != 'server':
        global backup
        backup = input('Delete existing files (no backs them up)? [y/N]: ') not in ('y', 'Y')

    # Install zsh if needed
    print("Setting up zsh...")
    run([here('setup_zsh.sh')], check=True)

    # Things I install on all machines (lin/mac laptops, servers)
    here_to_home('tmux.conf')
    here_to_home('zsh_custom')

    # Add more files here as you add them to your repo:
    # here_to_home('vimrc')


if __name__ == '__main__':
    if len(sys.argv) == 2:
        assert sys.argv[1] in ('server', 'linux', 'mac')
        main(sys.argv[1])
    else:
        print("Specify install mode: server, linux, mac")
