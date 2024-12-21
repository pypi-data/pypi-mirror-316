""" callsign_regex.py
Copyright (C) 2024 Martin J Levy - W6LHI/G8LHI - @mahtin - https://github.com/mahtin
"""

import sys
import argparse

import re

# sys.path.insert(0, os.path.abspath('..'))

from itu_appendix42 import ItuAppendix42, ItuAppendix42Error, __version__

def callsign_regex():
    """ callsign_regex """

    parser = argparse.ArgumentParser(
                    prog='callsign-regex',
                    epilog='Produce a valid optimized regex from the ITU Table of International Call Sign Series (Appendix 42 to the RR).\n' + \
                           'Based on https://www.itu.int/en/ITU-R/terrestrial/fmd/Pages/glad.aspx files.\n' + \
                           'For more information, see github repository - https://github.com/mahtin/callsign-regex\n' + \
                           'Copyright (C) 2024 Martin J Levy - W6LHI/G8LHI - @mahtin - https://github.com/mahtin'
                    )

    parser.add_argument('-V', '--version', action='store_true', default=False,  help='dump version number')
    parser.add_argument('-v', '--verbose', action='store_true',  default=False, help='verbose output')
    parser.add_argument('-F', '--force', action='store_true',  default=False, help='force rebuild of cached regex')
    parser.add_argument('-R', '--regex', action='store_true',  default=False, help='dump regex (to be used in code)')
    parser.add_argument('-f', '--forward', action='store_true',  default=False, help='dump table (showing callsign to country table)')
    parser.add_argument('-r', '--reverse', action='store_true',  default=False, help='dump reverse table (showing country to callsign table)')
    parser.add_argument('prefix', help='[prefix|country] ...', nargs=argparse.REMAINDER)

    args = parser.parse_args()
    #args, unknownargs = parser.parse_known_args()

    if args.version:
        print('Version: %s' % (__version__))
        sys.exit(0)

    if not args.force and not args.regex and not args.forward and not args.reverse and len(args.prefix) == 0:
        # at least one is required
        parser.print_help(sys.stderr)
        sys.exit(1)

    try:
        ituappendix42 = ItuAppendix42(force=args.force, verbose=args.verbose)
    except ItuAppendix42Error as e:
        sys.exit('ItuAppendix42() error')

    if args.regex:
        print(ituappendix42.regex())
        sys.exit(0)
    if args.forward:
        print(ituappendix42.dump())
        sys.exit(0)
    if args.reverse:
        print(ituappendix42.rdump())
        sys.exit(0)

    if len(args.prefix) > 0:
        # try to lookup all the remaining command line args one-by-one
        forward = ituappendix42.forward()
        reverse = ituappendix42.reverse()
        for prefix in args.prefix:
            for k in forward:
                v = forward[k]
                if re.match(k, prefix):
                    cc, country_name = v['cc'], v['name']
                    print('forward:', prefix, k, cc, country_name)
                    break
            for k in reverse:
                vv = reverse[k]
                country = vv['name']
                for v in vv['prefix']:
                    if re.match(v, prefix):
                        cc = k
                        print('reverse:', prefix, v, cc, country)
                        break

    sys.exit(0)
