__package__ = 'HlightReaxMD'
__date__ = '2024-11-15'
__author__ = 'W.-Y.Li, RFUE'
__email__ = 'bestleeimpact@163.com'
__version__ = '1.0'
__description__ = (
    'A package designed for analyzing ReaxFF molecular dynamics data and displacement cascade processes.'
    )
__all__ = [__package__, __version__, __author__]


def display_banner():
    print(
        ' __  __   ___                __      __    ____                                     ____      '
        )
    print(
        "/\\ \\/\\ \\ /\\_ \\    __        /\\ \\    /\\ \\__/\\  _`\\                           /'\\_/`\\/\\  _`\\    "
        )
    print(
        '\\ \\ \\_\\ \\\\//\\ \\  /\\_\\     __\\ \\ \\___\\ \\ ,_\\ \\ \\_\\ \\     __     __     __  _/\\      \\ \\ \\/\\ \\  '
        )
    print(
        " \\ \\  _  \\ \\ \\ \\ \\/\\ \\  /'_ `\\ \\  _ `\\ \\ \\/\\ \\ ,  /   /'__`\\ /'__`\\  /\\ \\/'\\ \\ \\__\\ \\ \\ \\ \\ \\ "
        )
    print(
        '  \\ \\ \\ \\ \\ \\_\\ \\_\\ \\ \\/\\ \\_\\ \\ \\ \\ \\ \\ \\ \\_\\ \\ \\\\ \\ /\\  __//\\ \\_\\.\\_\\/>  </\\ \\ \\_/\\ \\ \\ \\_\\ \\'
        )
    print(
        '   \\ \\_\\ \\_\\/\\____\\\\ \\_\\ \\____ \\ \\_\\ \\_\\ \\__\\\\ \\_\\ \\_\\ \\____\\ \\__/.\\_\\/\\_/\\_\\\\ \\_\\\\ \\_\\ \\____/'
        )
    print(
        '    \\/_/\\/_/\\/____/ \\/_/\\/___,\\ \\/_/\\/_/\\/__/ \\/_/\\/ /\\/____/\\/__/\\/_/\\//\\/_/ \\/_/ \\/_/\\/___/ '
        )
    print(
        '                          /\\____/                                                         '
        )
    print(
        f'                          \\_/__/    {__package__} v {__version__} made by {__author__}            '
        )
    print()
    print(__description__)
    print('=' * 100)


display_banner()
