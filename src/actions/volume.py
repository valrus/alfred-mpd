from __future__ import unicode_literals
from __future__ import print_function

import argparse

from util import increment_volume, alfred_json, volume_bar


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('delta', type=int)
    args = parser.parse_args()

    volume = increment_volume(args.delta)
    print(alfred_json(str(volume), variables={'bar': volume_bar(volume)}))


if __name__ == '__main__':
    main()
