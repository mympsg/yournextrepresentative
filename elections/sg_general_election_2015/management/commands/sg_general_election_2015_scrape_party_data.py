from __future__ import print_function

import bs4
from django.core.management.base import BaseCommand
from django.utils.text import slugify
import json
import requests


def make_organization(id,
                      name,
                      classification='',
                      contact_details=[],
                      dissolution_date=None,
                      founding_date=None,
                      identifiers=[],
                      links=[],
                      memberships=[],
                      other_names=[],
                      posts=[],
                      register="Singapore"):
    slug = slugify(name)

    return locals()


class Command(BaseCommand):
    help = "Scrape party information from eld.gov.sg"

    def handle(self, *args, **options):
        url = "http://www.eld.gov.sg/partyabbrev.html"
        response = requests.get(url)

        if response.status_code != 200:
            raise CommandError("Could not get URL %s" % url)

        parser = bs4.BeautifulSoup(response.text)

        def gen_parties():
            for row in parser.select("table tr")[1:]:
                col = row.find_all('td')
                abbrev = col[0].getText()
                fullname = col[1].getText()

                # skip over independent candidate
                if abbrev == '-':
                    continue

                yield make_organization(name=fullname, id=abbrev,
                                 classification="Party")

        print(json.dumps(list(gen_parties()), indent=4,
                         separators=(',', ': ')))
