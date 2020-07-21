import argparse


# print(args)


parser = argparse.ArgumentParser(prog=__file__, description='Process some integers.')
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')

args = parser.parse_args(args=args)
print(args.accumulate(args.integers))
