import rs1101.random_string as rs
import argparse

# import logging
# from rs1101.logging_config import setup_logger

# logger = setup_logger(logging.DEBUG)


def add_length(parser):
    parser.add_argument(
        "-l",
        "--length",
        help="length of the generated random string.",
        type=int,
    )


def add_candidate(parser):
    parser.add_argument(
        "-c",
        "--candidate",
        help="""candidate characters,
        u for uppercase,
        l for lowercase,
        d for digist,
        p for punctuation,
        h[H] for hex
        a for all printable.""",
        choices=rs.candidate_dict.keys(),
        nargs="+",
        action="extend",
    )


def add_strength(parser):
    parser.add_argument(
        "-s",
        "--strength",
        help="evaluate the strength of an random string.",
        action="store_true",
    )


def add_empty(parser):
    parser.add_argument(
        "-e",
        "--empty",
        help="end of nargs",
        action="store_true",
    )


def cli_strength(args):
    if args.strength:
        print(f"strength:{rs.strength(args.length,len(args.candidate))}")


def cli_rs2int(args):
    x = rs.rs2int(args.astring)
    print(x)
    cli_strength(args)


def cli_int2rs(args):
    s = rs.int2rs(args.x, length=args.length, candidate=args.candidate)
    print(s)
    args.length = len(s)
    cli_strength(args)


def cli_rs(args):
    s = rs.random_string(args.length, args.candidate)
    print(s)
    args.length = len(s)
    cli_strength(args)


def cli_main():
    parser = argparse.ArgumentParser(description="""functions about random strings""")
    subparsers = parser.add_subparsers(help="actions")
    add_length(parser)
    add_candidate(parser)
    add_strength(parser)

    # PART rs
    parser_rs = subparsers.add_parser(
        "gen",
        # parents=[parser],
        add_help=False,
        help="""Generate a random string.""",
    )
    parser_rs.set_defaults(func=cli_rs)

    # PART rs2int
    parser_rs2int = subparsers.add_parser(
        "rs2int",
        # parents=[parser],
        add_help=False,
        help="""Convert a random string to an integer.""",
    )
    parser_rs2int.add_argument("astring", help="a string.", type=str)
    parser_rs2int.set_defaults(func=cli_rs2int)

    # PART int2rs
    parser_int2rs = subparsers.add_parser(
        "int2rs",
        # parents=[parser],
        add_help=False,
        help="""Convert an integer to a random string.""",
    )
    parser_int2rs.add_argument("x", help="integer.", type=int)
    parser_int2rs.set_defaults(func=cli_int2rs)

    parser_lst = [parser, parser_rs, parser_rs2int, parser_int2rs]
    for p in parser_lst:
        add_empty(p)

    # PART run
    # args = parser.parse_args("int2rs 1234".split())
    args = parser.parse_args()
    # print(args)
    # sPART generate candidate
    if args.candidate is None:
        args.candidate = rs.candidate_default
    args.candidate = rs.g_candidate(args.candidate)
    if "func" not in args:
        args.func = cli_rs
        # logger.debug(f"set args.func, {args=}")
    if args.func != cli_int2rs and args.length is None:
        args.length = 12
    args.func(args)


if __name__ == "__main__":
    cli_main()
