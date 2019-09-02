from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

# Create your models here.


from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Collection, Page, PageManager, PageQuerySet
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase, TagBase, Tag as TaggitTag
from base.blocks import ExtraStreamBlock
from wagtail.snippets.models import register_snippet



# from .blocks import BaseStreamBlock, ExtraStreamBlock, HeroSlideBlock, FormStreamBlock

from base.models import HomePage, StandardPage
from django.db.models import Q

register_snippet(Collection)



class DifusionCulturalHomePage(HomePage):
    def get_nuevos_bisnietos(self):
        return Page.objects.filter(Q(depth__gte=5))[:6]



class DifusionCulturalArticulo(StandardPage):
    pass


class DifusionCulturalCartelera(Page):
    subpage_types = ['DifusionCulturalDependencia']
    parent_page_types = ['DifusionCulturalHomePage']


    def get_nietos(self):
        return Page.objects.descendant_of(self, inclusive=False).not_child_of(self)

    def get_nuevos_nietos(self):
        return Page.objects.descendant_of(self, inclusive=False).not_child_of(self)[:2]


class DifusionCulturalPaginaCategoria(Page):
    subpage_types = ['DifusionCulturalPagina']
    parent_page_types = ['DifusionCulturalHomePage']



class DifusionCulturalPagina(Page):
    introduccion = models.CharField(max_length=250)
    cuerpo = StreamField(
        ExtraStreamBlock(), verbose_name="Page body", blank=True
    )
    imagen = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Imagen de portada'
    )
    galeria = models.ForeignKey(
        Collection,
        limit_choices_to=~models.Q(name__in=['Root']),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text='Select the image collection for this gallery.'
    )

    search_fields = Page.search_fields + [
        index.SearchField('introduccion'),
        index.SearchField('cuerpo'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('introduccion'),
        StreamFieldPanel('cuerpo'),
        ImageChooserPanel('imagen'),
        FieldPanel('galeria'),

    ]






class DifusionCulturalDependencia(Page):
    subpage_types = ['DifusionCulturalNoticia']
    parent_page_types = ['DifusionCulturalCartelera']

'''
@register_snippet
class DifusionCulturalEtiqueta(TaggitTag):
    class Meta:
        proxy = True
'''


class DifusionCulturalNoticiaQuerySet(PageQuerySet):
    def ultimos(self):
        return self.order_by('-fecha')


#DifusionCulturalNoticiaManager = PageManager.from_queryset(DifusionCulturalNoticiaQuerySet)

class DifusionCulturalNoticiaManager(PageManager):
    def ultimos(self):
        return self.order_by('-fecha')


class DifusionCulturalNoticia(Page):
    fecha = models.DateField("Fecha de publicación")
    introduccion = models.CharField(max_length=250)
    cuerpo = StreamField(
        ExtraStreamBlock(), verbose_name="Page body", blank=True
    )
    imagen = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Imagen de portada'
    )
    galeria = models.ForeignKey(
        Collection,
        limit_choices_to=~models.Q(name__in=['Root']),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text='Select the image collection for this gallery.'
    )
    # etiquetas = ClusterTaggableManager(through=DifusionCulturalEtiqueta, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('introduccion'),
        index.SearchField('cuerpo'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('fecha'),
        FieldPanel('introduccion'),
        StreamFieldPanel('cuerpo'),
        ImageChooserPanel('imagen'),
        FieldPanel('galeria'),
        #FieldPanel('etiquetas'),
    ]

    objects = DifusionCulturalNoticiaManager()


