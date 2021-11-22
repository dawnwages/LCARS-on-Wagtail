from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.api import APIField
from wagtail.images.blocks import ImageChooserBlock as DefaultImageChooserBlock
from wagtail.images.api.fields import ImageRenditionField


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
    ])

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        StreamFieldPanel('body')
    ]

    api_fields = [
        APIField('date'),
        APIField('intro'),
        APIField('body'),
        APIField('image'),
        APIField('image_thumbnail', serializer=ImageRenditionField('fill-100x100', source='image')),
    ]



