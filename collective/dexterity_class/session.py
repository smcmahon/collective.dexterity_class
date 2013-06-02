import datetime
from five import grok

from z3c.form import group, field
from zope import schema
from zope.interface import provider
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.interfaces import IContextAwareDefaultFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Container
from plone.directives import dexterity, form
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable
from plone.supermodel import model

from plone.app.textfield import RichText


from collective.dexterity_class import MessageFactory as _


@provider(IContextAwareDefaultFactory)
def default_start(context):
    return datetime.datetime.now() + datetime.timedelta(7)

@provider(IContextAwareDefaultFactory)
def default_end(context):
    return datetime.datetime.now() + datetime.timedelta(10)


# Interface class; used to define content-type schema.

class ISession(form.Schema, IImageScaleTraversable):
    """
    Conference Session
    """

    title = schema.TextLine(title=_(u'Session Name'))

    description = schema.Text(
        title=_(u'Session summary'),
        description=_(u'Short description of session topics')
        )

    start = schema.Datetime(
        title=_(u'Session starts'),
        defaultFactory=default_start,
        )

    end = schema.Datetime(
        title=_(u'Session ends'),
        defaultFactory=default_end
        )

    accessible = schema.Choice(
        title=_(u'Accessible?'),
        values=(_(u'Yes'), _(u'No')),
        default='Yes',
        )
    form.widget(accessible="z3c.form.browser.radio.RadioFieldWidget")

    details = RichText(title=_(u'Details'))


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class Session(Container):
    grok.implements(ISession)

    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# session_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class SampleView(grok.View):
    """ sample view class """

    grok.context(ISession)
    grok.require('zope2.View')

    # grok.name('view')

    # Add view methods here
