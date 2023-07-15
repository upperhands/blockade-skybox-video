import argparse
import json
import platform
import shutil
import os
import subprocess
import sys


DESCRIPTION: str = """
Use configuration file ([--config-file, -cf]) to set your defaults.
Precedence is given to config file when there are
conflicting arguments!
"""

CONFIG_KEYS: set[str] = {
    'input',
    'output',
    'width',
    'height',
    'duration',
    'fps',
    'format',
    'constant-rate-factor',
    'codec',
    'start-angle',
    'end-angle',
    'start-focal-length',
    'mid-focal-length',
    'end-focal-length',
    'blender',
    'save-config-file',
    'path-to-script'
}

RENDER_COMMAND: str = '"{}" -b -P {} -- --blockade-config-file {}'


def isExecutable(path: str) -> bool:
    """
    Checks if path is executable.
    :param path: path to check
    """
    return shutil.which(path) \
        or subprocess.run(
        f'which {path}', shell=True, check=True).returncode == 0


def getDefaultBlender() -> str:
    """
    Returns the default blender executable for the current operating system
    :return: default blender executable
    """
    operating_system: str = platform.system()
    if operating_system == 'Linux':
        return 'blender'
    elif operating_system == 'Windows':
        return 'blender.exe'
    else:
        raise NotImplementedError(
            f"Unsupported operating system {platform}")


def get_parser() -> argparse.ArgumentParser:
    """
    Returns the parser
    :return: parser
    """
    parser = argparse.ArgumentParser(prog='Blockade Skybox Video Converter',
                                     description=DESCRIPTION)
    parser.add_argument('--input', '-i', required=True, type=str,
                        help='path to image')
    parser.add_argument('--config-file', '-cf', required=False, type=str,
                        default=None, help='configuration file')
    parser.add_argument('--output', '-o', required=False, type=str,
                        default='output.mp4', help='output video (mp4)')
    parser.add_argument('--width', required=False, type=int,
                        default=1080, help='width of output video')
    parser.add_argument('--height', required=False, type=int,
                        default=1920, help='height of output video')
    parser.add_argument('--fps', required=False, type=int,
                        default=30, help='fps of output video')
    parser.add_argument('--duration', '-d', required=False, type=int,
                        default=60,
                        help='duration of output video (in seconds)')
    parser.add_argument('--format', required=False, type=str,
                        default='MPEG4', help='format of output video')
    parser.add_argument('--codec', required=False, type=str,
                        default='H264', help='codec of output video')
    parser.add_argument('--constant-rate-factor', '-crf', required=False,
                        type=str, default='HIGH', help='constant rate factor')
    parser.add_argument('--start-angle', '-sa', required=False, type=int,
                        default=0, help='start angle (degrees)')
    parser.add_argument('--end-angle', '-ea', required=False, type=int,
                        default=360, help='end angle (degrees)')
    parser.add_argument('--start-focal-length', '-sf', required=False,
                        type=int, default=20, help='start focal length')
    parser.add_argument('--mid-focal-length', '-mf', required=False,
                        type=int, default=30, help='mid focal length')
    parser.add_argument('--end-focal-length', '-ef', required=False,
                        type=int, default=20, help='end focal length')
    parser.add_argument('--save-config-file', '-scf', required=False,
                        type=str, default=None, help='save config file')
    parser.add_argument('--blender', '-B', required=False, type=str,
                        default=getDefaultBlender(),
                        help='path to blender executable')
    parser.add_argument('--path-to-script', '-P', required=False,
                        type=str, default=os.path.join(
                            os.path.dirname(
                                os.path.dirname(__file__)),
                            'blockade', 'main.py'
                        ),
                        help='path to script')
    return parser


def getConfigFromArgs(args: argparse.Namespace) -> dict:
    """
    Returns config as dict from args
    :param args: args
    :return: config
    """
    config: dict = json.load(open(args.config_file)) \
        if args.config_file else {}
    for key, value in args._get_kwargs():
        key = key.replace('_', '-')  # Due to argparse's parsing rules
        if key not in config and key in CONFIG_KEYS:
            config[key] = value
    return config


def getConfigFile(config: dict) -> str:
    """
    Returns path to config file
    :param config: config
    :return: path to config file
    """
    if config.get('save-config-file'):
        return config['save-config-file']

    operating_system: str = platform.system()

    if operating_system == 'Linux':
        config_dir: str = os.path.join(
            os.path.expanduser('~'), '.config', 'blockade-skybox-video')
    elif operating_system == 'Windows':
        app_data: str = os.environ.get('APPDATA')
        config_dir: str = os.path.join(app_data, 'blockade-skybox-video')
    else:
        raise NotImplementedError(
            f"Unsupported operating system {operating_system}")
        return

    if not os.path.exists(config_dir):
        create_dir: bool = input('Create config directory? (Y/n)? ') != 'n'
        if create_dir:
            print(f'Creating config directory: {config_dir}...')
            os.makedirs(config_dir)
        else:
            print('Directory not created, exiting...')
            sys.exit(1)

    return os.path.join(config_dir, 'config.json')


def writeConfig(path: str, config: dict) -> None:
    """
    Writes config to path
    :param path: path
    :param config: config
    """
    with open(path, 'w') as f:
        json.dump(config, f, indent=4)


def runRenderCommand(config: dict, path_to_video_config: str) -> None:
    """
    Runs render command
    :param config: config
    :param path_to_video_config: path to video config
    """
    blender: str = config['blender']
    config_path: str = path_to_video_config
    path_to_script: str = config['path-to-script']

    command: str = RENDER_COMMAND.format(
        blender,
        path_to_script,
        config_path
    )

    subprocess.run(
        command,
        shell=True,
    )


if __name__ == '__main__':
    parser: argparse.ArgumentParser = get_parser()
    args: argparse.Namespace = parser.parse_args()
    config: dict = getConfigFromArgs(args)
    path_to_video_config: str = getConfigFile(config)

    if not isExecutable(config['blender']):
        print('Blender not found, exiting...')
        sys.exit(1)

    print(f'Your configuration is getting written to {path_to_video_config}!')
    writeConfig(path_to_video_config, config)

    runRenderCommand(config, path_to_video_config)
