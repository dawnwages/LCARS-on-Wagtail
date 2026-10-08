from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.api import APIField
from wagtail.images.blocks import ImageChooserBlock as DefaultImageChooserBlock


class ImageChooserBlock(DefaultImageChooserBlock):
    def get_api_representation(self, value, context=None):
        if value:
            return {
                'id': value.id,
                'title': value.title,
                'large': value.get_rendition('width-1000').attrs_dict,
                'thumbnail': value.get_rendition('fill-120x120').attrs_dict,
            }


class RichTextBlock(blocks.RichTextBlock):
    def get_api_representation(self, value, context=None):
        if value:
            return {
                'value': value,
            }


class CorePage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = StreamField([
        ("heading", blocks.CharBlock(classname="full title", icon="title")),
        ("paragraph", blocks.RichTextBlock(icon="pilcrow", features=['h2', 'h3', 'h4', 'h5', 'h6', 'bold', 'italic', 'link',
                              'ol', 'ul', 'document-link', 'embed', 'code', 'blockquote'])),
        ("image", ImageChooserBlock(icon="image")),
    ], use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body')
    ]

    api_fields = [
        APIField('date'),
        APIField('intro'),
        APIField('body'),
    ]



