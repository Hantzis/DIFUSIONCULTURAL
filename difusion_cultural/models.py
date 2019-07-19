from django.db import models


from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from rest_framework.serializers import models

# Create your models here.


from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Collection, Page
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet


# from .blocks import BaseStreamBlock, ExtraStreamBlock, HeroSlideBlock, FormStreamBlock

from base.models import HomePage

class DifusionHomePage(HomePage):
    pass