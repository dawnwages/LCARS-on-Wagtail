from django.utils.html import escape
from wagtail.core import hooks
from wagtail.core.rich_text import LinkHandler

class NoFollowExternalLinkHandler(LinkHandler):
    identifier = 'external'

    @classmethod
    def expand_db_attributes(cls, attrs):
        href = attrs["href"]
        return '<a href="%s" rel="nofollow">' % escape(href)

@hooks.register('register_rich_text_features')
def register_external_link(features):
    features.register_link_type(NoFollowExternalLinkHandler)