import json
from os.path import join
import re

from django.core.management.base import BaseCommand

from candidates.static_data import data_directory

def get_max_party_id(party_data):
    """Find the highest numeric ID from party IDs of the party:1234 form"""
    max_id = -1
    for party in party_data:
        party_id = party['id']
        m = re.search(r'party:(\d+)', party_id)
        if not m:
            continue
        int_party_id = int(m.group(1))
        max_id = max(max_id, int_party_id)
    return max_id

class Command(BaseCommand):

    help = "Fix parties with duplicate IDs in all-parties-from-popit.json"

    def handle(self, **options):
        json_filename = join(data_directory, 'all-parties-from-popit.json')
        with open(json_filename) as f:
            data = json.load(f)
        max_party_id = get_max_party_id(data)
        print "got max_party_id:", max_party_id
        next_party_id = max_party_id + 1
        seen_party_ids = set()
        new_party_data = []
        for party in data:
            party_id = party['id']
            if party_id in seen_party_ids:
                party['id'] = 'party:{0}'.format(next_party_id)
                next_party_id += 1
            seen_party_ids.add(party['id'])
            new_party_data.append(party)
        output_json_filename = json_filename + '.updated'
        print "Writing a file with unique IDs to", output_json_filename
        with open(output_json_filename, 'w') as f:
            json.dump(new_party_data, f, indent=4, sort_keys=True)
