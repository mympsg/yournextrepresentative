from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.utils.translation import ugettext as _

from pygeocoder import Geocoder, GeocoderError
import requests

# We use this both for validation of address and the results of the
# lookup, so the MapIt and geocoder lookups should be cached so we
# don't make double requests:

def check_address(address_string, country=None):
    tidied_address = address_string.strip()
    if country is not None:
        tidied_address += ', ' + country
    try:
        location_results = Geocoder.geocode(tidied_address)
    except GeocoderError:
        message = _(u"Failed to find a location for '{0}'")
        raise ValidationError(message.format(tidied_address))
    lat, lon = location_results[0].coordinates
    mapit_lookup_url = '{base_url}point/4326/{lon},{lat}'.format(
        base_url=settings.MAPIT_BASE_URL,
        lon=lon,
        lat=lat,
    )
    mapit_lookup_url += '?type=' + ','.join(settings.MAPIT_TYPES)
    mapit_lookup_url += '&generation={0}'.format(
        settings.MAPIT_CURRENT_GENERATION
    )
    mapit_result = requests.get(mapit_lookup_url)
    mapit_json = mapit_result.json()
    if 'error' in mapit_json:
        message = _(u"The area lookup returned an error: '{error}'")
        raise ValidationError(message.format(error=mapit_json['error']))
    sorted_mapit_results = sorted(
        mapit_json.items(),
        key=lambda t: (t[1]['type'], int(t[0]))
    )
    if not sorted_mapit_results:
        message = _(u"The address '{0}' appears to be outside the area this site knows about")
        raise ValidationError(message.format(tidied_address))
    types_and_areas = ','.join(
        '{0}-{1}'.format(a[1]['type'],a[0]) for a in
        sorted_mapit_results
    )
    area_slugs = [slugify(a[1]['name']) for a in sorted_mapit_results]
    ignored_slug = '-'.join(area_slugs)
    return {
        'type_and_area_ids': types_and_areas,
        'ignored_slug': ignored_slug,
    }
