# -*- coding: utf-8 -*-

"""
ipsh main cli script
"""

import argparse
import logging
import sys

from . import __version__
from . import interpreters
from . import interactive
from . import i18n


_ = i18n.get_gettext()

COMMAND_DEMO = "demo"
COMMAND_SHOWKEYS = "showkeys"


def get_arguments(*args: str, test_context: bool = False) -> argparse.Namespace:
    """Get commandline arguments"""
    i18n.translate_argparse()
    main_parser = argparse.ArgumentParser(
        prog="ipsh", description=_("interactive pseudo shell command line interface")
    )
    main_parser.set_defaults(loglevel=logging.INFO)
    main_parser.add_argument(
        "-d",
        "--debug",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        help=_("debug mode (loglevel DEBUG)"),
    )
    main_parser.add_argument(
        "--version",
        action="version",
        version=__version__,
        help=_("print version and exit"),
    )
    subparsers = main_parser.add_subparsers(required=True)
    demo_parser = subparsers.add_parser(
        COMMAND_DEMO, help=_("demonstrate a pseudo shell")
    )
    demo_parser.set_defaults(command=COMMAND_DEMO)
    demo_parser.add_argument(
        "-s",
        "--simple",
        action="store_true",
        help=_("show the simplest form using a dummy interpreter"),
    )
    showkeys_parser = subparsers.add_parser(
        COMMAND_SHOWKEYS,
        help=_("loop and show key codes until Ctrl-C or Ctrl-D is pressed"),
    )
    showkeys_parser.set_defaults(command=COMMAND_SHOWKEYS)
    if not test_context or not args:
        args_to_parse: list[str] | None = None
    else:
        args_to_parse = list(args)
    #
    return main_parser.parse_args(args=args_to_parse)


def configure_logging(level: int = logging.INFO) -> None:
    """Configure the root logger"""
    formatter = logging.Formatter("[%(levelname)s] %(message)s")
    root_logger = logging.getLogger()
    stream_handlers = [
        handler
        for handler in root_logger.handlers
        if isinstance(handler, logging.StreamHandler)
    ]
    if stream_handlers:
        current_handler = stream_handlers[0]
    else:
        current_handler = logging.StreamHandler()
        root_logger.addHandler(current_handler)
    #
    current_handler.setFormatter(formatter)
    current_handler.setLevel(level)
    root_logger.setLevel(level)


def run_shell_demo(simple: bool = False) -> None:
    """Run a PseudoShell demo"""
    if simple:
        interpreter = interpreters.BaseInterpreter()
        description = _("a simple PseudoShell demo")
    else:
        interpreter = interpreters.ArgumentBasedInterpreter()
        description = _("a PseudoShell demo with an argparse based interpreter")
    #
    logging.info(_("Running %s"), description)
    interactive.PseudoShell(prompt=" > ", interpreter=interpreter).run()


def run_showkeys() -> None:
    """Run the showkeys subcommand:
    Print the characters of each pressed key
    until Ctrl-C or Ctrl-D is pressed
    """
    logging.info(_('Running the "showkeys" subcommand'))
    logging.info(_("Exit with Ctrl-C or Ctrl-D"))
    while True:
        key = interactive.getkey()
        print([hex(ord(char)) for char in key])
        if key in (interactive.CTRL_C, interactive.CTRL_D):
            break
        #
    #


def run(*args: str, test_context: bool = False) -> int:
    """Run the main program"""
    arguments = get_arguments(*args, test_context=test_context)
    configure_logging(level=arguments.loglevel)
    if arguments.command == COMMAND_DEMO:
        run_shell_demo(simple=arguments.simple)
    elif arguments.command == COMMAND_SHOWKEYS:
        run_showkeys()
    #
    return 0


def app():
    """app function"""
    sys.exit(run())
