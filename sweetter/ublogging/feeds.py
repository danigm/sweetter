from django.conf import settings
from django.contrib.syndication.feeds import Feed
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

from ublogging.models import User
from ublogging import uapi


class PublicTimeline(Feed):
    title = "Sweetter 3.0 public timeline"
    link = settings.DOMAIN
    description = "Latest sweets"

    def items(self):
        sweetT = "%s: %s"
        sweets = uapi.public_timeline(paginated=False)[:20]
        for sweet in sweets:
            sweet.text = sweetT % (sweet.user.username, sweet.text)
        return sweets

    def item_link(self, item):
        return settings.DOMAIN + reverse('ublogging.views.sweet', kwargs={'sweetid':item.id})

    def item_author_name(self, item):
        return item.user.username

    def item_pubdate(self, item):
        return item.pub_date


class UserTimeline(Feed):
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return User.objects.get(username=bits[0])

    def title(self, obj):
        return "Sweetter 3.0 %s timeline" % obj.username

    def description(self, obj):
        return "Latest %s sweets" % obj.username

    def link(self, obj):
        return settings.DOMAIN + reverse("ublogging.views.user", kwargs={'user_name': obj.username})

    def items(self, obj):
        sweetT = "%s: %s"
        sweets = uapi.user_timeline(obj.username, paginated=False)[:20]
        for sweet in sweets:
            sweet.text = sweetT % (sweet.user.username, sweet.text)
        return sweets

    def item_link(self, item):
        return settings.DOMAIN + reverse('ublogging.views.sweet', kwargs={'sweetid':item.id})

    def item_author_name(self, item):
        return item.user.username

    def item_pubdate(self, item):
        return item.pub_date
