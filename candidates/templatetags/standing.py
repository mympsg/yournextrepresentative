from slugify import slugify

from django import template
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def constituency_in_year(value, year):
    print "got value:", value
    if year not in value:
        result = u'<span class="constituency-value-unknown">No definite information</span>'
    elif not value[year]:
        result = u'<span class="constituency-value-not-standing">Not standing in {0}</span>'
        result = result.format(year)
    else:
        link = u'<a href="{cons_url}">{cons_name}</a>'.format(
            cons_url=reverse(
                'constituency',
                kwargs={
                    'mapit_area_id': value[year]['post_id'],
                    'ignored_slug': slugify(value[year]['name']),
                }
            ),
            cons_name=value[year]['name']
        )
        result = u'<span class="constituency-value-standing-link">{0}</span>'.format(
            link
        )
    return mark_safe(result)
