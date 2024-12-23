import argparse


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    wordnet_parser = subparsers.add_parser(
        "wordnet", help="Analyze direct animal and physical adjective synsets"
    )
    wordnet_parser.add_argument(
        "--limit", type=int, default=5, help="Number of examples to show (0 for all)"
    )

    deep_parser = subparsers.add_parser(
        "wordnet-deep",
        help="Recursively analyze all animal and physical adjective synsets",
    )
    deep_parser.add_argument(
        "--limit", type=int, default=5, help="Number of examples to show (0 for all)"
    )

    adj_parser = subparsers.add_parser(
        "adjectives",
        help="Analyze adjective synsets",
    )
    adj_parser.add_argument(
        "--limit", type=int, default=5, help="Number of examples to show (0 for all)"
    )

    adjanimal_parser = subparsers.add_parser(
        "adj-animal",
        help="Generate random adjective-animal combinations",
    )
    adjanimal_parser.add_argument(
        "--limit", type=int, default=5, help="Number of combinations to generate"
    )

    return parser


def parse_args() -> argparse.Namespace:
    parser = init_argparse()
    return parser.parse_args()


def show_help() -> None:
    parser = init_argparse()
    parser.print_help()
