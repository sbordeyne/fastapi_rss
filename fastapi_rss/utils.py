"""
Utility functions for the fastapi_rss package
"""
import locale
import subprocess
from typing import Optional


def git_config(key: str, _global=True) -> str:
    """
    Checks git config for a key and returns the value

    :param key: The git config key to check
    :type key: str
    :param _global: whether to check in the local dir config or not,
                    defaults to True
    :type _global: bool, optional
    :return: The value of the git config key
    :rtype: str
    """
    cmd = ['git', 'config']
    if _global:
        cmd.append('--global')
    cmd.append(key)
    return subprocess.check_output(cmd).decode('utf8').strip('\n')


def get_locale_code() -> Optional[str]:
    """
    Returns the locale code of the current system

    :return: The locale code of the current system or None if not found
    :rtype: str | None
    """
    locale_code, encoding = locale.getlocale(locale.LC_CTYPE)
    del encoding
    if locale_code is not None:
        return locale_code.lower()
    return locale_code


def to_camelcase(string: str) -> str:
    """
    Turns a string into camelcasea

    :param string: The string to camelcase
    :type string: str
    :return: the camelcased string
    :rtype: str
    """
    string = string.split('_')
    for i, el in enumerate(string):
        if i == 0:
            continue
        string[i] = el.capitalize()
    return ''.join(string)
