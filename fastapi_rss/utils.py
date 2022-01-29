import locale
import subprocess


def git_config(key: str, _global=True):
    cmd = ['git', 'config']
    if _global:
        cmd.append('--global')
    cmd.append(key)
    return subprocess.check_output(cmd).decode('utf8').strip('\n')


def get_locale_code():
    return locale.getdefaultlocale()[0].lower()


def to_camelcase(string):
    string = string.split('_')
    for i, el in enumerate(string):
        if i == 0:
            continue
        string[i] = el.capitalize()
    return ''.join(string)
