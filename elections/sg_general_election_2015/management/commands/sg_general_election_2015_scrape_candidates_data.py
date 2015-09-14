from __future__ import print_function

import bs4
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.text import slugify
import itertools
import json
import requests
import sys


class Command(BaseCommand):
    help = "Scrape candidate and constituency information from eld.gov.sg"

    @staticmethod
    def get_candidates():
        """
        Scrape candidate data from eld website

        @returns {candidate: party, ...}
        """
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
                    [name.strip()
                     for name in
                     span.get_text().strip().split('\n')]
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

    def get_person_id(self, name):
        """
        Automatically assign ID based on names. Unique full names assumed.

        @param name Name to look up or assign
        @returns ID associated with this popolo.person instance
        """
        return slugify(name)

    def gen_persons_list(self):
        """
        Generate list of popolo.person entries

        @returns List of popolo.person models
        """
        popolo_persons = [
            {
                "fields": {
                    "name": person,
                },

                "model": "popolo.person",
                "pk": self.get_person_id(person)
            }

            for person in self.candidates
        ]

        return popolo_persons

    def gen_elections_list(self):
        """
        Generate list of elections.election entries

        @returns List of elections.election dicts
        """
        self.election_ids = dict(itertools.izip(settings.ELECTIONS,
                                                itertools.count(1)))
        elections = [
            {
                "fields": {
                    "name": v['name'],
                    "slug": slugify(v['name']),
                    "searchable": True
                },
                "model": "elections.election",
                "pk": self.election_ids[k]
            }

            for k, v in settings.ELECTIONS.items()
        ]

        return elections

    def gen_candidates_list(self):
        """
        Generate list of election.candidate entries

        @returns list of election.candidate lists
        """
        active_election_tup = filter(lambda (k, v): v['current'],
                                     settings.ELECTIONS.items())
        active_election_id = self.election_ids[active_election_tup[0][0]]

        return [
            {
                "fields": {
                    "election": active_election_id,
                },
                "model": "elections.candidate",
                "pk": self.get_person_id(name),
            }

            for name in self.candidates
        ]

    def handle(self, *args, **options):
        """
        Management command entry point
        """
        self.candidates = self.get_candidates()

        person_list = self.gen_persons_list()
        elections_list = self.gen_elections_list()
        candidates_list = self.gen_candidates_list()

        json.dump(person_list + elections_list + candidates_list, sys.stdout,
                  indent=4,
                  separators=(',', ': '))
