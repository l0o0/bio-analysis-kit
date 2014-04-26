#!/bin/env python
# 2014-4-18 created by Linxzh
# to combine additional fqfile with specific fqfile

import os
import argparse


# arguments
parser = argparse.ArgumentParser(description='Merge the fqfiles of the same\
sample produced by different lane', prog = 'Fqfile Merger', usage='')
parser.add_argument('',
