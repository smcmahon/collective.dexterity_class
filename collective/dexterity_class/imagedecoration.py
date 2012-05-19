from zope.interface import alsoProvides, implements
from zope.component import adapts
from zope import schema
from plone.directives import form
from plone.dexterity.interfaces import IDexterityContent
from plone.autoform.interfaces import IFormFieldProvider

from plone.namedfile import field as namedfile
from z3c.relationfield.schema import RelationChoice, RelationList
from plone.formwidget.contenttree import ObjPathSourceBinder

from collective.dexterity_class import MessageFactory as _


class IImageDecoration(form.Schema):
    """
       Marker/Form interface for Image Decoration
    """

    form.fieldset('decoration',
                label=u"Decoration",
                fields=['image_one', 'image_two']
            )

    image_one = namedfile.NamedBlobImage(title=_(u"Image One"), required=False)

    image_two = namedfile.NamedBlobImage(title=_(u"Image Two"), required=False)


alsoProvides(IImageDecoration,IFormFieldProvider)

# def context_property(name):
#     def getter(self):
#         return getattr(self.context, name)
#     def setter(self, value):
#         setattr(self.context, name, value)
#     def deleter(self):
#         delattr(self.context, name)
#     return property(getter, setter, deleter)

# class ImageDecoration(object):
#     """
#        Adapter for Image Decoration
#     """
#     implements(IImageDecoration)
#     adapts(IDexterityContent)

#     def __init__(self,context):
#         self.context = context

#     # -*- Your behavior property setters & getters here ... -*-
