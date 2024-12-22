import winzy
import sys
from winzy_head_tail.head import head_command
from winzy_head_tail.tail import tail_command


def create_parser_head(subparser):
    parser = subparser.add_parser(
        "head", description="Mimics head command using python"
    )
    parser.add_argument(
        "files",
        metavar="FILE",
        nargs="*",
        help="File(s) to process. Reads from stdin if none provided.",
    )
    parser.add_argument(
        "-n", type=int, help="Number of lines to display (default: 10)."
    )
    parser.add_argument(
        "-c", type=int, help="Number of bytes to display (overrides -n)."
    )
    return parser


def create_parser_tail(subparser):
    parser = subparser.add_parser(
        "tail", description="Mimics tail command using python"
    )
    parser.add_argument(
        "files",
        metavar="FILE",
        nargs="*",
        help="File(s) to process. Reads from stdin if none provided.",
    )
    parser.add_argument(
        "-n", type=int, help="Number of lines to display (default: 10)."
    )
    parser.add_argument(
        "-c", type=int, help="Number of bytes to display (overrides -n)."
    )
    return parser


class WinzyPluginHead:
    """ Mimics head command using python """

    __name__ = "head"

    @winzy.hookimpl
    def register_commands(self, subparser):
        self.parser = create_parser_head(subparser)
        self.parser.set_defaults(func=self.run)

    def run(self, args):
        # Check if piped input is available
        if not args.files and sys.stdin.isatty():
            self.parser.error("At least one FILE is required, or use piped input.")

        head_command(filenames=args.files if args.files else None, n=args.n, c=args.c)

    def hello(self, args):
        # this routine will be called when "winzy head is called."
        print("Hello! This is an example ``winzy`` plugin.")


head_plugin = WinzyPluginHead()


class WinzyPluginTail:
    """ Mimics tail command using python """

    __name__ = "tail"

    @winzy.hookimpl
    def register_commands(self, subparser):
        self.parser = create_parser_tail(subparser)
        self.parser.set_defaults(func=self.run)

    def run(self, args):
        # Check if piped input is available
        if not args.files and sys.stdin.isatty():
            self.parser.error("At least one FILE is required, or use piped input.")

        tail_command(filenames=args.files if args.files else None, n=args.n, c=args.c)


tail_plugin = WinzyPluginTail()
