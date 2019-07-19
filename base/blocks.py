from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.core.blocks import (
    CharBlock, ChoiceBlock, RichTextBlock, StreamBlock, StructBlock, TextBlock,
)

from wagtail.core import blocks
from wagtail_blocks.blocks import HeaderBlock, ListBlock, ImageTextOverlayBlock, CroppedImagesWithTextBlock, \
    ListWithImagesBlock, ThumbnailGalleryBlock, ChartBlock, MapBlock, ImageSliderBlock

from django.db import models


class ImageBlock(StructBlock):
    """
    Custom `StructBlock` for utilizing images with associated caption and
    attribution data
    """
    image = ImageChooserBlock(required=True)
    caption = CharBlock(required=False)
    attribution = CharBlock(required=False)

    class Meta:
        icon = 'image'
        template = "blocks/image_block.html"


class HeadingBlock(StructBlock):
    """
    Custom `StructBlock` that allows the user to select h2 - h4 sizes for headers
    """
    heading_text = CharBlock(classname="title", required=True)
    size = ChoiceBlock(choices=[
        ('', 'Select a header size'),
        ('h2', 'H2'),
        ('h3', 'H3'),
        ('h4', 'H4')
    ], blank=True, required=False)

    class Meta:
        icon = "title"
        template = "blocks/heading_block.html"


class BlockQuote(StructBlock):
    """
    Custom `StructBlock` that allows the user to attribute a quote to the author
    """
    text = TextBlock()
    attribute_name = CharBlock(
        blank=True, required=False, label='e.g. Mary Berry')

    class Meta:
        icon = "fa-quote-left"
        template = "blocks/blockquote.html"

###




class ColumnBlock(blocks.StreamBlock):
    heading = blocks.CharBlock(classname="título completo")
    paragraph = blocks.RichTextBlock()
    image = ImageChooserBlock()

    class Meta:
        template = 'blocks/custom/column_block.html'


class TwoColumnBlock(blocks.StructBlock):
    left_column = ColumnBlock(icon='arrow-left', label='Left column content')
    right_column = ColumnBlock(icon='arrow-right', label='Right column content')

    class Meta:
        template = 'blocks/custom/two_columns_block.html'
        icon = 'grip'
        label = 'Dos columnas'


class IconColumnBlock(blocks.StreamBlock):
    heading = blocks.CharBlock(classname="título completo")
    paragraph = blocks.RichTextBlock()
    image = ImageChooserBlock()
    icon = CharBlock(required=False)

    class Meta:
        template = 'blocks/custom/icon_column_block.html'


class ThreeColumnBlock(blocks.StructBlock):
    left_column = IconColumnBlock(icon='placeholder', label='Left column content')
    center_column = IconColumnBlock(icon='placeholder', label='Right column content')
    right_column = IconColumnBlock(icon='placeholder', label='Right column content')

    class Meta:
        template = 'blocks/custom/three_columns_block.html'
        icon = 'group'
        label = 'Tres columnas'


class CarouselImageBlock(blocks.StructBlock):
    """
    Custom `StructBlock` for utilizing images with associated caption and
    attribution data
    """
    image = ImageChooserBlock(required=True)
    caption = CharBlock(required=False)
    attribution = CharBlock(required=False)

    class Meta:
        icon = 'image'
        template = "blocks/custom/carousel_image_block.html"


class CarouselBlock(blocks.StreamBlock):
    image = CarouselImageBlock(icon='cogs', label='Imagen de carrusel')

    class Meta:
        template = 'blocks/custom/carousel_block.html'
        icon = 'cog'
        label = 'Carrusel'



class HeadBandBlock(StructBlock):
    """
    Custom `StructBlock` that allows the user to select h2 - h4 sizes for headers
    """
    heading_text = CharBlock(classname="title", required=True)
    size = ChoiceBlock(choices=[
        ('', 'Select a header size'),
        ('h2', 'H2'),
        ('h3', 'H3'),
    ], blank=True, required=False)
    text = CharBlock(classname="text", required=True)
    cta_text  = CharBlock(classname="text", required=False)

    class Meta:
        icon = "title"
        template = "blocks/custom/head_band_block.html"




class HeadingBlock(StructBlock):
    """
    Custom `StructBlock` that allows the user to select h2 - h4 sizes for headers
    """
    heading_text = CharBlock(classname="title", required=True)
    size = ChoiceBlock(choices=[
        ('', 'Select a header size'),
        ('h2', 'H2'),
        ('h3', 'H3'),
        ('h4', 'H4')
    ], blank=True, required=False)

    class Meta:
        icon = "title"
        template = "blocks/heading_block.html"



class HeroSlideBlockImage(blocks.StructBlock):
    """
    Custom `StructBlock` for utilizing images with associated caption and
    attribution data
    """
    image = ImageChooserBlock(required=False)
    title = CharBlock(required=False)
    caption = CharBlock(required=False)
    cta_text = blocks.CharBlock(required=False)
    cta_link = blocks.PageChooserBlock(required=False)

    class Meta:
        icon = 'image'
        template = "blocks/custom/hero_slide_block_image.html"


class HeroSlideBlock(blocks.StreamBlock):
    image = HeroSlideBlockImage(icon='image', label='Imagen Hero')

    class Meta:
        template = 'blocks/custom/hero_slide_block.html'
        label = 'Hero Slide'

###


# StreamBlocks
class BaseStreamBlock(StreamBlock):
    """
    Define the custom blocks that `StreamField` will utilize
    """
    heading_block = HeadingBlock()
    paragraph_block = RichTextBlock(
        icon="fa-paragraph",
        template="blocks/paragraph_block.html"
    )
    image_block = ImageBlock()
    block_quote = BlockQuote()
    embed_block = EmbedBlock(
        help_text='Insert an embed URL e.g https://www.youtube.com/embed/SGJFWirQ3ks',
        icon="fa-s15",
        template="blocks/embed_block.html")





class ExtraStreamBlock(BaseStreamBlock):
    """
    Este bloque extiende a BaseStreamBlock, para hacer lo mismo que BaseStreamBlock pero meter cosas nuevas
    """
    doscolumnas_block = TwoColumnBlock()
    threecolumn_block = ThreeColumnBlock()
    carousel_block = CarouselBlock()
    headband_block = HeadBandBlock()
    map_block = MapBlock()


class FormStreamBlock(BaseStreamBlock):
    """
    Este bloque extiende a BaseStreamBlock, para hacer lo mismo que BaseStreamBlock pero meter cosas nuevas
    """
    paragraph_block = RichTextBlock(
        icon="fa-paragraph",
        template="blocks/form_paragraph_block.html"
    )
    headband_block = HeadBandBlock(
        icon="fa-heading",
        template="blocks/custom/form_head_band_block.html"
    )


