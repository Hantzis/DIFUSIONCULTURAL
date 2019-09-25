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
from base.models import HomePage, StandardPage
from django.db.models import Q
from datetime import datetime, timedelta


today = datetime.today().date()




class DifusionCulturalHomePage(HomePage):
    def get_nuevos_bisnietos(self):
        return Page.objects.live().filter(Q(depth__gte=5))[:6]

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

    subpage_types = ['DifusionCulturalNota']
    parent_page_types = ['DifusionCulturalHomePage','DifusionCulturalPagina','DifusionCulturalNota']

    class Meta:
        verbose_name = "Nota"
        verbose_name_plural = "Notas"



@register_snippet
class DifusionCulturalCarteleraCategoria(ClusterableModel):
    categoria = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=80)

    panels = [
        FieldPanel('categoria'),
        FieldPanel('slug'),
    ]

    def __str__(self):
        return self.categoria

    class Meta:
        verbose_name = "Categoría (cartelera)"
        verbose_name_plural = "Categorías (cartelera)"


class DifusionCulturalCartelera(RoutablePageMixin, Page):
    subpage_types = ['DifusionCulturalDependencia']
    parent_page_types = ['DifusionCulturalHomePage']

    def get_nietos(self):
        return Page.objects.live().descendant_of(self, inclusive=False).not_child_of(self)

    def get_nuevos_nietos(self):
        return Page.objects.live().descendant_of(self, inclusive=False).not_child_of(self)[:2]

    @classmethod
    def can_create_at(cls, parent):
        # You can only create one of these!
        return super(DifusionCulturalCartelera, cls).can_create_at(parent) \
               and not cls.objects.exists()


    def get_context(self, request, *args, **kwargs):
        context = super(DifusionCulturalCartelera, self).get_context(request, *args, **kwargs)
        context['posts'] = self.posts
        context['difusion_cultural_cartelera'] = self
        return context

    def get_next_posts(self):
        return DifusionCulturalNoticia.objects.filter(fecha_fin__gte=today).live().order_by('-fecha_fin')

    def get_prev_posts(self):
        return DifusionCulturalNoticia.objects.filter(fecha_fin__lt=today).live().order_by('-fecha_fin')

    @route(r'^etiqueta/(?P<etiqueta>[-\w]+)/$')
    def posts_proximos_etiqueta(self, request, etiqueta, *args, **kwargs):
        self.search_type = 'etiqueta'
        self.search_term = etiqueta
        self.posts = self.get_next_posts().filter(etiquetas__slug=etiqueta).order_by('-fecha_fin')
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^archivado/etiqueta/(?P<etiqueta>[-\w]+)/$')
    def posts_previos_etiqueta(self, request, etiqueta, *args, **kwargs):
        self.search_type = 'etiqueta'
        self.search_term = etiqueta
        self.posts = self.get_prev_posts().filter(etiquetas__slug=etiqueta).order_by('-fecha_fin')
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^categoria/(?P<categoria>[-\w]+)/$')
    def posts_proximos_categoria(self, request, categoria, *args, **kwargs):
        self.search_type = 'categoria'
        self.search_term = categoria
        self.posts = self.get_next_posts().filter(categoria__slug=categoria).order_by('-fecha_fin')
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^archivado/categoria/(?P<categoria>[-\w]+)/$')
    def posts_previos_categoria(self, request, categoria, *args, **kwargs):
        self.search_type = 'categoria'
        self.search_term = categoria
        self.posts = self.get_prev_posts().filter(categoria__slug=categoria).order_by('-fecha_fin')
        return Page.serve(self, request, *args, **kwargs)


    @route(r'^archivado/$')
    def prev_post_list(self, request, *args, **kwargs):
        self.posts = self.get_prev_posts().order_by('-fecha_fin')
        return Page.serve(self, request, *args, **kwargs)


    @route(r'^$')
    def next_post_list(self, request, *args, **kwargs):
        self.posts = self.get_next_posts().order_by('-fecha_fin')
        return Page.serve(self, request, *args, **kwargs)

    class Meta:
        verbose_name = "Cartelera"
        verbose_name_plural = "Carteleras"




class DifusionCulturalDependencia(Page):
    subpage_types = ['DifusionCulturalNoticia']
    parent_page_types = ['DifusionCulturalCartelera']


    class Meta:
        verbose_name = "Dependencia"
        verbose_name_plural = "Dependencias"


"""
class DifusionCulturalNoticiaQuerySet(PageQuerySet):
    def ultimos(self):
        return self.order_by('-fecha')
"""

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
    fecha_inicio = models.DateField("Fecha inicio")
    fecha_fin = models.DateField("Fecha fin")
    hora_inicio = models.TimeField("Hora fin")
    hora_fin = models.TimeField("Hora fin")

    introduccion = models.CharField(max_length=250)
    ubicacion = models.CharField(max_length=250, blank=True)
    consideraciones = models.CharField(max_length=250, blank=True, null=True)

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
    categoria = ParentalKey('DifusionCulturalCarteleraCategoria', on_delete=models.PROTECT, blank=True)
    etiquetas = ClusterTaggableManager(through='DifusionCulturalNoticiaEtiqueta', blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('introduccion'),
        index.SearchField('cuerpo'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('fecha_inicio'),
        FieldPanel('fecha_fin'),
        FieldPanel('hora_inicio'),
        FieldPanel('hora_fin'),
        FieldPanel('introduccion'),
        FieldPanel('ubicacion'),
        FieldPanel('consideraciones'),
        StreamFieldPanel('cuerpo'),
        ImageChooserPanel('imagen'),
        FieldPanel('galeria'),
        FieldPanel('categoria'),
        FieldPanel('etiquetas'),
    ]

    objects = DifusionCulturalNoticiaManager()

    subpage_types = []
    parent_page_types = ['DifusionCulturalDependencia']

    @property
    def esta_vigente(self):
        return self.fecha_fin > (today - timedelta(days=1))

    @property
    def difusion_cultural_cartelera(self):
        return self.get_parent().specific.get_parent().specific

    @property
    def difusion_cultural_cartelera_slug(self):
        return self.get_parent().specific.get_parent().specific.slug


    def get_context(self, request, *args, **kwargs):
        context = super(DifusionCulturalNoticia, self).get_context(request, *args, **kwargs)
        context['difusion_cultural_cartelera'] = self.difusion_cultural_cartelera
        return context

    class Meta:
        verbose_name = "Noticia"
        verbose_name_plural = "Noticias"



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

