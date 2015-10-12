import argparse
import os
import os.path
import sys

import requests

__author__ = 'Horacio Hoyos'
__copyright__ = 'Copyright , Nagasu Technologies'
__version__ = "0.1.2"


def deploy_updatesite(args):
    opts = vars(args)
    files = args.l
    if not args.o:
        opts['o'] = opts['u']
    push_base_uri = 'https://api.bintray.com/content/{o}/{r}/'.format(**opts)
    if args.p == 'publish':
        opts['d'] = 'false'
        if files:
            if os.path.exists(files):
                for path, dirs, files in os.walk(files):
                    relpath = os.path.relpath(path, args.l)
                    if os.path.basename(path) == "features":
                        print("Processing features dir files...")
                    elif os.path.basename(path) == "plugins":
                        print("Processing plugin dir  files...")
                    elif os.path.basename(path) == "binary":
                        print("Processing binary dir files...")
                    files = [f for f in files if not f[0] == '.']   # Don´t push hidden files
                    for f in files:
                        print("Processing {} file...".format(f))
                        p2file = open(os.path.join(path, f), 'rb')
                        if os.path.basename(f) == "content.jar" or os.path.basename(f) == "artifacts.jar":
                            print("Uploading p2 metadata file directly to the repository")
                            push_uri = push_base_uri + '{};publish=0'.format(os.path.basename(f))
                            if opts['m'] == "upload":
                                response = requests.put(push_uri, auth=(args.u, args.k), data=p2file)
                                response.raise_for_status()
                            else:
                                response = requests.delete(push_uri, auth=(args.u, args.k), data=p2file)
                                if response.status_code != 200:
                                    print(response.content)
                        else:
                            print("Uploading package file directly to the repository")
                            push_pck_uri = push_base_uri
                            push_pck_uri += '{n}/{e}/'.format(**opts)
                            if relpath != ".":
                                push_pck_uri += '{}/'.format(relpath)
                            push_uri = push_pck_uri + '{};publish=0'.format(os.path.basename(f))
                            if opts['m'] == "upload":
                                response = requests.put(push_uri, auth=(args.u, args.k), data=p2file)
                                response.raise_for_status()
                            else:
                                response = requests.delete(push_uri, auth=(args.u, args.k), data=p2file)
                                if response.status_code != 200:
                                    print(response.content)

            else:
                raise ValueError("The supplied path does not exist.")
    else:
        opts['d'] = 'true'

    print("Publishing the new version")
    if opts['m'] == "upload":
        payload = {'discard': '{d}'.format(**opts)}
        publish_uri = push_base_uri + '{n}/{e}/publish'.format(**opts)
        response = requests.post(publish_uri, auth=(args.u, args.k), data=payload)
        response.raise_for_status()


def parse_arguments(arguments):
    parser = argparse.ArgumentParser(description='This script can be used to manage an Eclipse p2 Updatesite in Bintray.',
                                     add_help=True)
    parser.add_argument('p', action="store", help='Publish all unpublished content for the given package and version,'
                                                  ' including the last upload. If discard, any unpublished content will'
                                                  ' be discarded and the upload/delete arguments will be ignored.',
                        choices=['publish', 'discard'])
    parser.add_argument('-m', action="store", dest="m", help='Whether the given files should be uploaded or deleted '
                                                             'from the repository.', default="upload",
                        choices=['upload', 'delete'])

    parser.add_argument('-u', action="store", dest="u", help='Bintray user')
    parser.add_argument('-k', action="store", dest="k", help='Bintray API Key')
    parser.add_argument('-o', action="store", dest="o", help='Repository owner, if other than user', default=None)
    parser.add_argument('-r', action="store", dest="r", help='Repository name')
    parser.add_argument('-n', action="store", dest="n", help='Package Name')
    parser.add_argument('-e', action="store", dest="e", help='Package Version')
    parser.add_argument('-l', action="store", dest="l", help='Path to repository location in local machine. If no path'
                                                             'is given only the publish (POST) request is sent.',
                        default=None)
    parser.add_argument('--version', action='version', version='%(prog)s ' +__version__)
    return parser.parse_args(arguments)


def main():
    """
    Sample Usage: pushToBintray.py -u username -k apikey -o owner -r repo -n package -e version -p pathToP2Repo
    :return:
    """
    args = parse_arguments(sys.argv[1:])
    deploy_updatesite(args)

if __name__ == "__main__":
    main()

