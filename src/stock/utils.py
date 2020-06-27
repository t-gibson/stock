"""
Util functions and classes.
"""


def get_random_ws(workspace_path: str, length: int = 8) -> str:
    import os
    import random
    import string

    letters = string.ascii_lowercase
    dn = ''.join(random.choice(letters) for _ in range(length))
    return os.path.join(workspace_path, dn)


# TODO: move to a more performant approach
# See: https://stackoverflow.com/questions/6028000/how-to-read-a-static-file-from-inside-a-python-package
def resource_filename(resources_name) -> str:
    """
    Get the absolute path of a resource file of the package.
    """
    import pkg_resources

    return pkg_resources.resource_filename(__name__, resources_name)
