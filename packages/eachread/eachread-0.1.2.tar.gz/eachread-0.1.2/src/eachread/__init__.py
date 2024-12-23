import eachread.cli
import eachread.wordnet.commands
import eachread.wordnet.data


def main() -> None:
    eachread.wordnet.data.ensure_nltk_data()
    args = eachread.cli.parse_args()

    if args.command == "wordnet":
        eachread.wordnet.commands.cmd_wordnet(args.limit)
    elif args.command == "wordnet-deep":
        eachread.wordnet.commands.cmd_wordnet_deep(args.limit)
    elif args.command == "adjectives":
        eachread.wordnet.commands.cmd_adjectives(args.limit)
    elif args.command == "adj-animal":
        eachread.wordnet.commands.cmd_adjanimal(args.limit)
    else:
        eachread.cli.show_help()
