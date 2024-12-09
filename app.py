import util
import secrets
import argparse

def main():
    parser = argparse.ArgumentParser(description='a tool to auto send requests to google form')
    subparser = parser.add_subparsers(dest = 'cmd', required=1, help='subcommand')

    parser_gen = subparser.add_parser('init', help='generate config')
    parser_gen.add_argument('url', type=str, help='google form\'s url')
    parser_gen.add_argument('-o', '--output', type=str, default=secrets.token_urlsafe(5).lower(), help='times you want to repeat')
    parser_gen.set_defaults(func=util.generate_config)

    parser_post = subparser.add_parser('run', help='send requests to form')
    parser_post.add_argument('config', type=str, help='filename of config at ./config/')
    parser_post.add_argument('-t', '--time', type=int, default=1, help='times you want to repeat')
    parser_post.add_argument('-d', '--delay', type=float, default=0.01, help='times you want to repeat')
    parser_post.set_defaults(func=util.send_request)

    args = parser.parse_args()
    res = args.func(args)

    print(res)

main()