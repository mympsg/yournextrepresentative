from datetime import date

# Documentation for fields in ELECTIONS from Mark Longsair
# --------------------------------------------------------
#
# for_post_role - this is the name of the Post that the
# candidates in this election are trying to get elected to
# (e.g. 'Member of Parliament')
#
# candidate_membership_role - this is normally just 'Candidate',
# unless this is a primary election, in which case you'd use
# 'Primary Candidate'.  This is used when the code is looking for
# Memberships of the Post that represent people standing as a
# candidate for that Post.
#
# winner_membership_role - once the election is over, users in
# the 'Result Recorders' group can click on a button that says
# "This candidate won!".  If that's used, then a new Membership
# of the Post will be created for that candidate with the role
# given by this setting.  Normally that will just be None,
# meaning that the Membership should have no role specified - the
# default interpretation of a Membership of a role is that that
# person is fulfilling that role.
#
# election_date - a Python datetime.date object indicating the
# day on which votes are cast in the election.
#
# candidacy_start_date - When someone is added as a candidate, a
# Membership of that Post (typically with role 'Candidate') is
# created. candidacy_start_date is a Python datetime.date that
# describes when the start_date of that Membership should be.
# It's a bit artificial to make this the same for all candidates
# in the election, but in the countries we've used the code in so
# far it has been rare to actually know the date when someone
# becomes a candidate, and having a start_date on these
# Memberships makes certain queries against the API that use date
# ranges work properly. We normally set this date to the day
# after the previous election.
#
# organization_id - This is the ID of the Organization that the
# candidates would be serving in if they are elected.  e.g. in
# the UK elections this would be "House of Commons"
#
# name - This is the name of the election, as it would be
# normally described. This shouldn't be prefixed with 'The',
# since most of the uses of the election name on the site prefix
# it with a 'The' anyway.  For example, this value might be '2015
# General Election'
#
# current - This is a boolean value indicating if this election
# and candidates from it should be shown on various pages.
#
# use_for_candidate_suggestions - If this is set to True, then on
# the page for a Post, the candidates from this election will be
# offered as possibile candidates for this election in an "Are
# these candidates standing again?" section, so you can quickly
# say "Yes, they are" or "No, they aren't".
#
# party_membership_start_date / party_membership_end_date - These
# are similar to candidacy_start_date in being rather artificial;
# these are the start and end dates of party Memberships that are
# created when you set the party that a candidate is standing
# for.  We usually (artificially) set the start_date to the day
# after the previous election of the same type and the end_date
# to date(9999, 12, 31) for current elections.
#
# mapit_types - a list of 3-letter type codes for the area types
# that these Posts might be associated with.
#
# mapit_generation - the ID of the MapIt generation that the
# areas that these Posts might be associated with are from.
#
# post_id_format - this is a Python format string that is used to
# find the ID of the Post in this election for a particular
# area. If you include '{area_id}' then that will be replaced by
# the area ID.


ELECTIONS = {
    '2015': {
        'for_post_role': 'Member of Parliament',
        'candidate_membership_role': 'Candidate',
        'winner_membership_role': None,
        'election_date': date(2015, 9, 11),
        'candidacy_start_date': date(2014, 9, 1),
        'organization_id': 'sgp',
        'organization_name': 'Singapore Parliament',
        'name': '2015 General Election',
        'current': True,
        'use_for_candidate_suggestions': True,
        'party_membership_start_date': date(2014, 9, 1),
        'party_membership_end_date': date(9999, 12, 31),
        'mapit_types': ['WMC'],
        'mapit_generation': 22,
        'post_id_format': '{area_id}',
    }
}

MAPIT_BASE_URL = 'http://mapit.mysociety.org/'
