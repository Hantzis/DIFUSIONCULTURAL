from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

# Create your models here.


from wagtail.core.fields import StreamField
from wagtail.core.models import Collection, Page, PageManager, PageQuerySet
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase, TagBase, Tag as TaggitTag
from base.blocks import ExtraStreamBlock
from wagtail.contrib.routable_page.models import RoutablePageMixin, route


# from .blocks import BaseStreamBlock, ExtraStreamBlock, HeroSlideBlock, FormStreamBlock

from base.models import HomePage, StandardPage
from django.db.models import Q




class DifusionCulturalHomePage(HomePage):
    def get_nuevos_bisnietos(self):
        return Page.objects.filter(Q(depth__gte=5))[:6]

    parent_page_types = ['wagtailcore.Page']

    @classmethod
    def can_create_at(cls, parent):
        # You can only create one of these!
        return super(DifusionCulturalHomePage, cls).can_create_at(parent) \
               and not cls.objects.exists()

    class Meta:
        verbose_name = "Inicio"



class DifusionCulturalBlog(Page):
    subpage_types = ['DifusionCulturalArticulo']
    parent_page_types = ['DifusionCulturalHomePage']


    def get_nietos(self):
        return Page.objects.descendant_of(self, inclusive=False).not_child_of(self)

    def get_nuevos_nietos(self):
        return Page.objects.descendant_of(self, inclusive=False).not_child_of(self)[:2]


    @classmethod
    def can_create_at(cls, parent):
        # You can only create one of these!
        return super(DifusionCulturalBlog, cls).can_create_at(parent) \
               and not cls.objects.exists()

    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blog"




class DifusionCulturalArticulo(StandardPage):
    fecha = models.DateField("Fecha de publicación")
    autor = models.CharField(max_length=250)
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
    # acotaciones = models.CharField(verbose_name="Acotaciones", max_length=250)
    galeria = models.ForeignKey(
        Collection,
        limit_choices_to=~models.Q(name__in=['Root']),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text='Select the image collection for this gallery.'
    )
    #etiquetas = ClusterTaggableManager(through='DifusionCulturalNoticiaEtiqueta', blank=True)#viene de noticia: TODO: adaptar a ArticuloDeBlog

    search_fields = Page.search_fields + [
        index.SearchField('introduccion'),
        index.SearchField('cuerpo'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('fecha'),
        FieldPanel('introduccion'),
        FieldPanel('autor'),
        StreamFieldPanel('cuerpo'),
        ImageChooserPanel('imagen'),
        FieldPanel('galeria'),
    ]

    subpage_types = []
    parent_page_types = ['DifusionCulturalBlog']

    class Meta:
        verbose_name = "Artículo"
        verbose_name_plural = "Artículos"


class DifusionCulturalNota(Page):

    # Body section of the HomePage
    body = StreamField(
        ExtraStreamBlock(), verbose_name="Home content block", blank=True
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]

    subpage_types = []
    parent_page_types = ['DifusionCulturalHomePage','DifusionCulturalPagina','DifusionCulturalNota']

    class Meta:
        verbose_name = "Nota"
        verbose_name_plural = "Notas"



class DifusionCulturalCartelera(Page):
    subpage_types = ['DifusionCulturalDependencia']
    parent_page_types = ['DifusionCulturalHomePage']


    def get_nietos(self):
        return Page.objects.descendant_of(self, inclusive=False).not_child_of(self)

    def get_nuevos_nietos(self):
        return Page.objects.descendant_of(self, inclusive=False).not_child_of(self)[:2]


    @classmethod
    def can_create_at(cls, parent):
        # You can only create one of these!
        return super(DifusionCulturalCartelera, cls).can_create_at(parent) \
               and not cls.objects.exists()

    class Meta:
        verbose_name = "Cartelera"
        verbose_name_plural = "Carteleras"


class DifusionCulturalPaginaCategoria(Page):
    subpage_types = ['DifusionCulturalPagina']
    parent_page_types = ['DifusionCulturalHomePage']

    class Meta:
        verbose_name = "Categoría de página"
        verbose_name_plural = "Categorías de página"


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

    subpage_types = ['DifusionCulturalPagina', 'DifusionCulturalNota']
    parent_page_types = ['DifusionCulturalPagina', 'DifusionCulturalPaginaCategoria', 'DifusionCulturalHomePage']


    class Meta:
        verbose_name = "Página"
        verbose_name_plural = "páginas"




class DifusionCulturalDependencia(Page):
    subpage_types = ['DifusionCulturalNoticia']
    parent_page_types = ['DifusionCulturalCartelera']


    class Meta:
        verbose_name = "Dependencia"
        verbose_name_plural = "Dependencias"



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

@register_snippet
class DifusionCulturalNoticiaEtiqueta(TaggedItemBase):
    content_object = ParentalKey('DifusionCulturalNoticia', related_name='noticia_tags')


@register_snippet
class Tag(TaggitTag):
    class Meta:
        proxy = True


class DifusionCulturalNoticia(Page):
    fecha = models.DateField("Fecha de publicación")
    introduccion = models.CharField(max_length=250)
    fecha_de_evento = models.CharField(verbose_name="Fecha_de_evento", max_length=250, null=True)
    horarios = models.CharField(verbose_name="Horarios", max_length=250, null=True)
    lugar = models.CharField(verbose_name="Lugar", max_length=250, null=True)
    consideraciones = models.CharField(verbose_name="Consideraciones", max_length=250, null=True)
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
    etiquetas = ClusterTaggableManager(through='DifusionCulturalNoticiaEtiqueta', blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('introduccion'),
        index.SearchField('cuerpo'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('fecha'),
        FieldPanel('introduccion'),
        FieldPanel('fecha_de_evento'),
        FieldPanel('horarios'),
        FieldPanel('lugar'),
        FieldPanel('consideraciones'),
        StreamFieldPanel('cuerpo'),
        ImageChooserPanel('imagen'),
        FieldPanel('galeria'),
        FieldPanel('etiquetas'),
    ]

    objects = DifusionCulturalNoticiaManager()

    subpage_types = []
    parent_page_types = ['DifusionCulturalDependencia']


    class Meta:
        verbose_name = "Noticia"
        verbose_name_plural = "Noticias"


