import os


def list_folder_content(directory: str,
                        include_files: bool = False,
                        include_dirs: bool = False,
                        ascend: bool | None = None,
                        remove_ext: bool = False) -> list[str]:
    """List content of given directory

    Args:
        directory (str): The directory to list content
        include_files (bool, optional): If include files in the result. Defaults to False.
        include_dirs (bool, optional): If include directories in the result. Defaults to False.
        ascend (bool | None, optional): How to sort the result, if None then no sorting, otherwise True for ascending and False for descending
        remove_ext (bool, optional): If the file extension should be removed (if `include_files`)
    """
    if not include_dirs and not include_files or not os.path.isdir(directory):
        return list()

    res: list[str] = [
        item if not remove_ext else os.path.splitext(item)[0] for item in os.listdir(directory)
        if (include_files and os.path.isfile(os.path.join(directory, item))) or
           (include_dirs and os.path.isdir(os.path.join(directory, item)))
    ]

    if ascend is not None:
        if ascend:
            return sorted(res)
        return sorted(res, reverse=True)
    return res
