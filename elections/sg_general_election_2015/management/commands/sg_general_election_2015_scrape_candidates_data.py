from __future__ import print_function

import bs4
from django.core.management.base import BaseCommand
from django.utils.text import slugify
import json
import requests


class Command(BaseCommand):
    help = "Scrape candidate and constituency information from eld.gov.sg"

    def get_candidates(self):
        url = "http://www.eld.gov.sg/election_results_2015.html"
        response = requests.get(url)

        if response.status_code != 200:
            raise CommandError("Could not get URL %s" % url)

        parser = bs4.BeautifulSoup(response.text)
        tables = parser.select(".tableStyleResult")

        all_candidates = dict()

        for table in tables:
            for row in table.select('tbody > tr'):
                cells = row.find_all('td')
                candidate_main_cell = cells[0]
                party_main_cell = cells[1]

                candidate_sets = [
                    span.get_text().strip().split('\n')
                    for span in candidate_main_cell.find_all('span')
                ]
                parties = [
                    link.get_text()
                    for link in party_main_cell.find_all('a')
                ]

                all_candidates.update({
                    candidate: party
                    for candidate_set, party in zip(candidate_sets, parties)
                    for candidate in candidate_set
                })

        return all_candidates

    def handle(self, *args, **options):
        candidates = sef.get_candidates()
