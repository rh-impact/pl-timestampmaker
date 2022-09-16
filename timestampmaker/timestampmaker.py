#
# timestampmaker ds ChRIS plugin app
#
# (c) 2022 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#

from chrisapp.base import ChrisApp
import subprocess

Gstr_title = r"""
 _   _                     _                                        _
| | (_)                   | |                                      | |
| |_ _ _ __ ___   ___  ___| |_ __ _ _ __ ___  _ __  _ __ ___   __ _| | _____ _ __
| __| | '_ ` _ \ / _ \/ __| __/ _` | '_ ` _ \| '_ \| '_ ` _ \ / _` | |/ / _ \ '__|
| |_| | | | | | |  __/\__ \ || (_| | | | | | | |_) | | | | | | (_| |   <  __/ |
 \__|_|_| |_| |_|\___||___/\__\__,_|_| |_| |_| .__/|_| |_| |_|\__,_|_|\_\___|_|
                                             | |
                                             |_|
"""

Gstr_synopsis = """

(Edit this in-line help for app specifics. At a minimum, the
flags below are supported -- in the case of DS apps, both
positional arguments <inputDir> and <outputDir>; for FS and TS apps
only <outputDir> -- and similarly for <in> <out> directories
where necessary.)

    NAME

       timestampmaker

    SYNOPSIS

        docker run --rm fnndsc/pl-timestampmaker timestampmaker                     \\
            [-h] [--help]                                               \\
            [--json]                                                    \\
            [--man]                                                     \\
            [--meta]                                                    \\
            [--savejson <DIR>]                                          \\
            [-v <level>] [--verbosity <level>]                          \\
            [--version]                                                 \\
            <inputDir>                                                  \\
            <outputDir>

    BRIEF EXAMPLE

        * Bare bones execution

            docker run --rm -u $(id -u)                             \
                -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
                fnndsc/pl-timestampmaker timestampmaker                        \
                /incoming /outgoing

    DESCRIPTION

        `timestampmaker` ...

    ARGS

        [-h] [--help]
        If specified, show help message and exit.

        [--json]
        If specified, show json representation of app and exit.

        [--man]
        If specified, print (this) man page and exit.

        [--meta]
        If specified, print plugin meta data and exit.

        [--savejson <DIR>]
        If specified, save json representation file to DIR and exit.

        [-v <level>] [--verbosity <level>]
        Verbosity level for app. Not used currently.

        [--version]
        If specified, print version number and exit.
"""


class TimestampMaker(ChrisApp):
    """
    Create timestamps for the ChRIS project(s).
    """

    PACKAGE = __package__
    TITLE = "A ChRIS plugin for Timestamp Creation"
    CATEGORY = ""
    TYPE = "ds"
    ICON = ""  # url of an icon image
    MIN_NUMBER_OF_WORKERS = 1  # Override with the minimum number of workers as int
    MAX_NUMBER_OF_WORKERS = 1  # Override with the maximum number of workers as int
    MIN_CPU_LIMIT = (
        2000  # Override with millicore value as int (1000 millicores == 1 CPU core)
    )
    MIN_MEMORY_LIMIT = 8000  # Override with memory MegaByte (MB) limit as int
    MIN_GPU_LIMIT = 0  # Override with the minimum number of GPUs as int
    MAX_GPU_LIMIT = 0  # Override with the maximum number of GPUs as int

    # Use this dictionary structure to provide key-value output descriptive information
    # that may be useful for the next downstream plugin. For example:
    #
    # {
    #   "finalOutputFile":  "final/file.out",
    #   "viewer":           "genericTextViewer",
    # }
    #
    # The above dictionary is saved when plugin is called with a ``--saveoutputmeta``
    # flag. Note also that all file paths are relative to the system specified
    # output directory.
    OUTPUT_META_DICT = {}

    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
        Use self.add_argument to specify a new app argument.
        """

        self.add_argument(
            "-f",
            "--format",
            dest="format",
            default="%Y-%m-%d %H:%M:%S",
            optional=True,
            type=str,
            help="Time format string",
        )
        self.add_argument(
            "-t",
            "--time",
            dest="time",
            type=str,
            optional=True,
            default="",
            help="ISO 8601 or RFC 2616 string. By default, retrieves from file's metadata",
        )
        self.add_argument(
            "-fs",
            "--font-size",
            dest="font_size",
            default="32",
            type=str,
            optional=True,
            help="Size of the font used in the timestamp",
        )
        self.add_argument(
            "-ff",
            "--font-family",
            dest="font_family",
            default="DejaVu Sans",
            choices=(
                "Century Schoolbook",
                "DejaVu Sans",
                "Lato",
            ),
            optional=True,
            type=str,
            help="Font to use",
        )
        self.add_argument(
            "-fc",
            "--font-color",
            dest="font_color",
            default="white",
            optional=True,
            type=str,
            help="Name or color code of the font",
        )
        self.add_argument(
            "-bc",
            "--background-color",
            dest="background",
            default="black",
            optional=True,
            type=str,
            help="Name or color code of the background",
        )
        self.add_argument(
            "-tz",
            "--time-zone",
            dest="timezone",
            default="",
            optional=True,
            type=str,
            help="IANA time zone. By default, retrieves from media file's metadata",
        )
        self.add_argument(
            "-co",
            "--coordinate-origin",
            dest="origin",
            choices=(
                "top-left",
                "top-right",
                "bottom-left",
                "bottom-right",
            ),
            default="top-left",
            optional=True,
            type=str,
            help="Quadrant of video where timestamp will appear",
        )
        self.add_argument(
            "-x-coordinate",
            dest="x",
            default="32",
            optional=True,
            type=str,
            help="X coordinate of the timestamp",
        )
        self.add_argument(
            "-y-coordinate",
            dest="y",
            default="32",
            optional=True,
            type=str,
            help="Y coordinate of the timestamp",
        )
        self.add_argument(
            "-fp",
            "--font-padding",
            dest="font_padding",
            default="8",
            optional=True,
            type=str,
            help="Padding around font in timestamp",
        )
        self.add_argument(
            "-r",
            "--require",
            dest="require",
            default="",
            optional=True,
            type=str,
            help="Comma-separated Ruby libs",
        )

    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """
        print(Gstr_title)
        print("Version: %s" % self.get_version())

        try:
            assert options.background != options.font_color
        except AssertionError:
            raise Exception(
                "Background color can not be the same as the foreground color"
            )
        cmd = [
            "timestamp",
            "--format",
            options.format,
        ]
        if options.time != "":
            cmd.extend(
                [
                    "--time",
                    options.time,
                ]
            )
        cmd.extend(
            [
                "--font-size",
                options.font_size,
                "--font-family",
                options.font_family,
                "--font-color",
                options.font_color,
                "--background-color",
                options.background,
            ]
        )
        if options.timezone != "":
            cmd.extend(
                [
                    "--time-zone",
                    options.timezone,
                ]
            )
        cmd.extend(
            [
                "--coordinate-origin",
                options.origin,
                "-x",
                options.x,
                "-y",
                options.y,
                "--font-padding",
                options.font_padding,
            ]
        )
        if options.require != "":
            cmd.extend(
                [
                    "--require",
                    options.require,
                ]
            )
        print(
            f'Running Command: {" ".join(map(str, cmd))} {options.inputdir} {options.outputdir}'
        )
        subprocess.run(cmd, check=True)

    def show_man_page(self):
        """
        Print the app's man page.
        """
        print(Gstr_synopsis)
