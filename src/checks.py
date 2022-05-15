from shutil import which


def is_installed(name):
    return which(name) is not None


def initial_checks():
    """
    return: a tuple containing a status code and a message
    """
    if  not is_installed("grep"):
        return False, "grep is not installed or in $PATH!"

    return True, "Checks Complete"
