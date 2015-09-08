from datetime import date

ELECTIONS = {
    '2015': {
        'for_post_role': 'Member of Parliament',
        'candidate_membership_role': 'Candidate',
        'winner_membership_role': None,
        'election_date': date(2015, 9, 11),
        'candidacy_start_date': date(2015, 9, 1),
        'organization_id': 'commons',
        'name': '2015 General Election',
        'current': True,
        'party_membership_start_date': date(2010, 5, 7),
        'party_membership_end_date': date(9999, 12, 31),
        'mapit_types': ['WMC'],
        'mapit_generation': 22,
        'post_id_format': '{area_id}',
    }
}

MAPIT_BASE_URL = 'http://mapit.mysociety.org/'
