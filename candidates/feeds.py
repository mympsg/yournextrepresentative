import re

from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.utils.feedgenerator import Atom1Feed
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from .models import LoggedAction

lock_re = re.compile(r'^(?:Unl|L)ocked\s*constituency (.*) \((\d+)\)$')

class RecentChangesFeed(Feed):
    title = _("YourNextMP recent changes")
    description = _("Changes to YNMP candidates")
    link = "/feeds/changes.xml"
    feed_type = Atom1Feed

    def items(self):
        return LoggedAction.objects.order_by('-updated')[:50]

    def item_title(self, item):
        m = lock_re.search(item.source)
        if m:
            return u"{0} - {1}".format(
                m.group(1),
                item.action_type
            )
        else:
            return u"{0} - {1}".format(
                item.popit_person_id,
                item.action_type
            )

    def item_description(self, item):
        updated = _(u"Updated at {0}").format(str(item.updated))
        description = u"{0}\n\n{1}\n".format(item.source, updated)

        return description

    def item_link(self, item):
        # As a hack for the moment, constituencies are just mentioned
        # in the source message:
        m = lock_re.search(item.source)
        if m:
            return reverse('constituency', kwargs={
                'post_id': m.group(2),
                'ignored_slug': slugify(m.group(1))
            })
        else:
            if item.popit_person_id:
                return reverse('person-view', args=[item.popit_person_id])
            else:
                return '/'
