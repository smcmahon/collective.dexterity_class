from five import grok

from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Container
from plone.directives import dexterity, form
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable
from plone.supermodel import model

from plone.app.textfield import RichText


from collective.dexterity_class import MessageFactory as _


# Interface class; used to define content-type schema.

class IProgram(form.Schema, IImageScaleTraversable):
    """
    Conference Program
    """

    # If you want a schema-defined interface, delete the model.load
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/program.xml to define the content type.

    model.load("models/program.xml")


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class Program(Container):
    grok.implements(IProgram)

    def trackVocabulary(self):
        tracks = [s.strip() for s in self.tracks.split('\n')]
        return SimpleVocabulary.fromValues(tracks)



# View class
# The view will automatically use a similarly named template in
# program_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class SampleView(grok.View):
    """ sample view class """

    grok.context(IProgram)
    grok.require('zope2.View')

    # grok.name('view')

    # Add view methods here
