import os
from pathlib import Path
import argparse
import colorama

import repochecker.git_info as git_info

def color_bool(b: bool) -> str:
    if b:
        return colorama.Fore.GREEN + str(b) + colorama.Fore.RESET
    else:
        return colorama.Fore.RED + str(b) + colorama.Fore.RESET

def format_branch(branch: str, upstream: str|None, behind: int, ahead: int):
    return (
        branch +
        (' -> ' + upstream if upstream != None else '') +
        (f' ahead {ahead}' if ahead != 0 else '') +
        (f' behind {behind}' if behind != 0 else '')
    )

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        prog='RepoChecker',
        description='Check git repository information of multiple directories and get a summary of what types of changes have not been pushed to upstream',
    )
    parser.add_argument('directory', type=Path)
    select_group = parser.add_mutually_exclusive_group()
    select_group.add_argument('-i', '--invert', action='store_true', help='print all unchanged repositories')
    select_group.add_argument('-a', '--all', action='store_true', help='print all directories')

    iterate_type_group = parser.add_mutually_exclusive_group()
    iterate_type_group.add_argument('-s', '--single', action='store_true', help='only check `directory`')
    iterate_type_group.add_argument('-r', '--recursive', action='store_true', help='check `directory` and all its subdirectories recursively')
    parser.add_argument('-d', '--recursion-depth', default=-1, type=int, help='how deep to recurse. Negative numbers mean no limit. A depth of 1 will check `directory` and its immediate children')

    parser.add_argument('-b', '--brief', action='store_true')

    args = parser.parse_args()

    # Get directories to check
    if not args.directory.exists():
        print(colorama.Fore.RED + f"Unable to find '{args.directory}'" + colorama.Fore.RESET)
        return

    directories: list[Path] = list()

    if args.single or (args.recursive and args.recursion_depth == 0):
        if args.directory.is_dir():
            directories = [args.directory.absolute()]
    elif args.recursive:
        for root, _, _ in os.walk(args.directory):
            if args.recursion_depth < 0 or root[len(str(args.directory)):].count(os.sep) <= args.recursion_depth:
                directories.append(Path(root))
    else:
        root = args.directory.absolute()
        directories = [root.joinpath(dir) for dir in os.listdir(root) if root.joinpath(dir).is_dir()]

    if len(directories) == 0:
        # No directories
        print(colorama.Fore.RED + 'Could not find any directories to check' + colorama.Fore.RESET)
        return


    for dir in directories:
        # Get directory info
        is_git_repo = git_info.is_repository(dir)

        info: git_info.DirectoryInfo|None = None
        if is_git_repo:
            try:
                info = git_info.get_info(dir)
            except Exception as e:
                print(colorama.Fore.RED + str(e) + colorama.Fore.RESET)
                continue

            if not args.all and (not info.has_issues() ^ args.invert):
                continue
        elif not args.all and args.invert:
            continue

        # Print directory info
        if args.brief:
            print(colorama.Fore.LIGHTBLACK_EX + f'git repo: {color_bool(is_git_repo).rjust(15)}  ' + (colorama.Fore.LIGHTBLACK_EX + f'unchanged: {color_bool(not info.has_issues()).rjust(15)}  ' if info != None else ' '*18) + colorama.Fore.RESET + str(dir))
        else:
            print()
            print(dir)
            print(colorama.Fore.LIGHTBLACK_EX + f' Is git repo: {color_bool(is_git_repo)}')
            if (info != None):
                print(colorama.Fore.LIGHTBLACK_EX + ' Current branch: ' + (colorama.Fore.CYAN + info.current_branch if info.current_branch != None else colorama.Fore.RED + 'None') + colorama.Fore.RESET)
                print(colorama.Fore.LIGHTBLACK_EX + ' Branches: ' + colorama.Fore.WHITE + ''.join([f'\n  {format_branch(*branch)}' for branch in info.branches]) + colorama.Fore.RESET)
                print(colorama.Fore.LIGHTBLACK_EX + f' No uncommited changes: {color_bool(info.has_no_uncommited_changes)}')
                print(colorama.Fore.LIGHTBLACK_EX + f' No unpushed commits: {color_bool(info.has_no_unpushed_commits)}')
                print(colorama.Fore.LIGHTBLACK_EX + f' No stashed changes: {color_bool(info.has_no_stashed_changes)}')
            print()

if __name__ == '__main__':
    colorama.just_fix_windows_console()
    main()