#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    'cmd',
    nargs='+',

)

args = parser.parse_args()
print(args.cmd)
