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
from plone.indexer import indexer
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable
from plone.supermodel import model

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from plone.app.textfield import RichText

from collective.dexteritytextindexer import searchable

from collective.dexterity_class import MessageFactory as _

from program import IProgram


@provider(IContextSourceBinder)
def trackVocabulary(context):
    while context is not None and not IProgram.providedBy(context):
        context = context.aq_parent

    return context.trackVocabulary()


@provider(IContextAwareDefaultFactory)
def default_start(context):
    return datetime.datetime.now() + datetime.timedelta(7)

@provider(IContextAwareDefaultFactory)
def default_end(context):
    return datetime.datetime.now() + datetime.timedelta(10)


class StartBeforeEnd(Invalid):
    __doc__ = _(u"The start or end date is invalid")


# Interface class; used to define content-type schema.

class ISession(form.Schema, IImageScaleTraversable):
    """
    Conference Session
    """

    title = schema.TextLine(title=_(u'Session Name'))

    description = schema.Text(
        title=_(u'Session summary'),
        description=_(u'Short description of session topics'),
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

    tracks = schema.List(
        title=_(u'Tracks for this session'),
        value_type=schema.Choice(title=u'dummy', source=trackVocabulary),
        )

    searchable('details')
    details = RichText(title=_(u'Details'))

    presenters = RelationList(
        title=u"Presenters",
        default=[],
        value_type=RelationChoice(
            title=_(u"Presenter"),
            source=ObjPathSourceBinder(
                object_provides='collective.dexterity_class.presenter.IPresenter'
                )
            ),
        required=False,
)

    @invariant
    def checkDates(data):
        if data.start is not None and data.end is not None:
            if data.start > data.end:
                raise StartBeforeEnd(_(u"The start date must be before the end date."))


@form.validator(field=ISession['description'])
def validateDescription(value):
    if 'php' in value.lower():
        raise schema.ValidationError(
          u"PHP is not for mature audiences.")

@form.error_message(error=schema.ValidationError, field=ISession['description'])
def yuck(value):
    return u"Yuck"


@indexer(ISession)
def tracksIndexer(obj):
    return obj.tracks
grok.global_adapter(tracksIndexer, name="Subject")

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

class SampleView(dexterity.DisplayForm):
    """ sample view class """

    grok.context(ISession)
    grok.require('zope2.View')

    # grok.name('view')

    # Add view methods here
