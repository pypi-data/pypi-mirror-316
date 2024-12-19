import os
import subprocess
import sys
import tomllib
from importlib import util
from pathlib import Path
from typing import TYPE_CHECKING
# ======================================================================
# Hinting types
if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import TypeAlias
    from typing import Self
    PipType: TypeAlias = Callable[[list[str] | None], int]
else:
    PipType = Self = object
# ======================================================================
# Parameters
ENV_VAR_PREFIX = 'REPO_'
# ======================================================================
def git(*args: str, capture_output: bool = False):
    return subprocess.run(('git', *args), capture_output = capture_output)
# ======================================================================
class working_directory:
    def __init__(self, path: Path) -> None:
        self.new = path
    def __enter__(self) -> Self:
        self.old = Path.cwd()
        os.chdir(self.new)
        return self
    def __exit__(self, *_) -> None:
        os.chdir(self.old)
# ======================================================================
def clone(remote: str, subrepo: str, path_subrepo: Path) -> None:

    if path_ref := os.environ.get(ENV_VAR_PREFIX + subrepo.upper()):
        print('\nCLONING USING REFERENCE\n')
        if not git('clone', '--reference-if-able', str(Path(path_ref) / '.git'),
                   '--dissociate', remote, str(path_subrepo)).returncode:
            return
    print('\nCLONING FROM UPSTREAM\n')
    git('clone', remote, str(path_subrepo))
# ======================================================================
def set_envvar(name: str, path: Path):
    envvar_name = ENV_VAR_PREFIX + name
    match sys.platform:
        case 'win32':
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Environment',
                                access = winreg.KEY_WRITE) as key:
                winreg.SetValueEx(key, envvar_name, 0, winreg.REG_SZ, str(path))
        case 'linux':
            with open(os.path.expanduser('~/.bashrc'), 'a') as f:
                f.write(f'export {envvar_name}="{path}"\n')
# ======================================================================
def install_package(path_package: Path, args: set[str], pip: PipType):

    path_pyproject = path_package / 'pyproject.toml'
    param = str(path_package)

    print(f'Installing {param}')
    try:
        with open(path_pyproject, mode = 'rb') as f:
            options = set(tomllib.load(f)['tool']['setuptools']['dynamic']['optional-dependencies'].keys())
        options &= args
        if options:
            param += f'[{",".join(options)}]'
    except FileNotFoundError:
        param += f'[{",".join(args)}]'

    pip(['install', '-e', param])
# ======================================================================
def _install_packages(path_cwd: Path,
                        patterns: list[str],
                        args: set[str],
                        pip: PipType) -> set[str]:
    for pattern in patterns:
        for path_pyproject in path_cwd.glob(pattern + '/pyproject.toml'):
            install_package(path_pyproject.parent, args, pip)
    return args
# ======================================================================
def install(args: set[str],
            flags: set[str],
            cloned_subrepos: dict[str, Path]) -> None:
    from pip._internal.cli.main import main as pip

    path_cwd = Path.cwd()
    # ------------------------------------------------------------------
    try:
        with open(path_cwd / 'install.toml', mode = 'rb') as f:
            config = tomllib.load(f)
    except FileNotFoundError:
        try:
            install_package(path_cwd, args, pip)
        except Exception:
            pass
        return
    # ------------------------------------------------------------------
    # Installing requirements lists
    if dependencies := config.get('dependencies'):
        # Installing dependency lists
        if path_required := dependencies.get('required'):
            # Required dependencies
            pip(['install', '-r', str(Path(path_required))])

        if optional := dependencies.get('optional'):
            # Optional dependencies
            for option, path_optional in optional.items():
                if option in args:
                    pip(['install', '-r', str(Path(path_optional))])
    # ------------------------------------------------------------------
    # Installing packages
    if packages := config.get('packages'):
        if paths_required := packages.get('required'):
            args = _install_packages(path_cwd, paths_required, args, pip)
        if optional := packages.get('optional'):
            for option, paths_optional in optional.items():
                if option in args:
                    optlen = len(option) + 1
                    subargs = {arg[optlen:] for arg in args
                               if arg.startswith(option + '-')}
                    _install_packages(
                        path_cwd, paths_optional, subargs, pip)
    # ------------------------------------------------------------------
    # Installing dev tools
    if '--dev' in flags:
        subprocess.run(['pre-commit', 'install', '--install-hooks'])
    # ------------------------------------------------------------------
    # Installing subrepos
    if not (subrepos_config := config.get('subrepos')):
        return
    if (subrepos_required := subrepos_config.get('required')) is None:
        subrepos = {}
    else:
        subrepos = {key: (value[0], set(value[1]), set(value[2]))
                    for key, value in subrepos_required.items()}

    if subrepos_optional := subrepos_config.get('optional'):
        for arg in args:
            body, _, flag = arg.rpartition('-')
            if info := subrepos_optional.get(body):
                # Arg in optional repos
                if (subrepo_info := subrepos.get(info[0])) is None:
                    # Subrepo included for the first time
                    subrepo_info = (info[1][0],
                                    set(info[1][1]),
                                    set(info[1][2]) | flags)
                    subrepos[info[0]] = subrepo_info
                if flag:
                    subrepo_info[2].add(flag)

    path_subrepos = path_cwd / '.subrepos'
    path_subrepos.mkdir(exist_ok = True)

    for remote, (target, subrepo_args, subrepo_flags) in subrepos.items():

        if (path_subrepo := cloned_subrepos.get(remote)) is None:
            subrepo = _name_from_remote(remote)

            print(f"Installing '{subrepo}'")
            if (path_subrepo := path_subrepos / subrepo).exists():

                print(f"Repository '{subrepo}' already exists")
                with working_directory(path_subrepo):
                    git('fetch')
                    if target:
                        git('checkout', target)
                    git('pull')
            else:
                clone(remote, subrepo, path_subrepo)
                with working_directory(path_subrepo):
                    if target:
                        git('checkout', target)

            cloned_subrepos[remote] = path_subrepo

        try:
            spec = util.spec_from_file_location('install',
                                                path_subrepo / 'install.py')
            installer = util.module_from_spec(spec) # type: ignore
            spec.loader.exec_module(installer) # type: ignore
            print(f"Running install script for '{subrepo}'")
            installer.install(subrepo_args, subrepo_flags, cloned_subrepos)
        except Exception:
            install_package(path_subrepo, args, pip)
# ======================================================================
def _name_from_remote(remote: str):
    return remote.split('/', 1)[1].split('.git', 1)[0]
# ======================================================================
def main(cli_args: list[str] | None = None,
         path_repo: Path | None = None) -> int:
    """Runs the installation for this repository."""
    if cli_args is None:
        cli_args = sys.argv[1:]
    if path_repo is None:
        path_repo = Path.cwd()
    # ------------------------------------------------------------------
    # arguments processing
    flags: set[str] = set()
    args: set[str] = set()

    for arg in cli_args:
        if arg.startswith('--'):
            flags.add(arg)
        else:
            args.add(arg)

    if flags:
        _args = args.copy()
        for flag in flags:
            args.update(arg + flag[1:] for arg in _args)

        args.update(f[2:] for f in flags)
    # ------------------------------------------------------------------
    with working_directory(path_repo):

        remote = git('remote', '-v', capture_output = True
                     ).stdout.split(b' ', 2)[1].decode('utf-8')
        name = _name_from_remote(remote)

        set_envvar(name.upper(), path_repo)

        git('config', 'pull.rebase', 'true')

        subprocess.run((sys.executable,
                        '-m', 'pip', 'install', '--upgrade', 'pip'))

        install(args, flags, {remote: path_repo})
    return 0
