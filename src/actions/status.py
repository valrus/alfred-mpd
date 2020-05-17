from __future__ import unicode_literals
from __future__ import print_function

from util import open_mpd_client, alfred_json, format_time


def main():
    with open_mpd_client() as client:
        data = client.currentsong()
        data.update(client.status())
    data.update({
        'duration': format_time(data['duration']) if data.get('duration') else 'N/A',
        'elapsed': format_time(data['elapsed']) if data.get('elapsed') else 'N/A',
        'lastmodified': data.get('last-modified', 'N/A'),
    })
    print(alfred_json(data.get('title', ''), variables=data))


if __name__ == '__main__':
    main()
