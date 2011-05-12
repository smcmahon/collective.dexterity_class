from five import grok
from plone.directives import dexterity, form

from zope import schema

from z3c.form import group, field
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget

from collective.dexterity_class import MessageFactory as _


# Interface class; used to define content-type schema.

class ITypefromschema(form.Schema):
    """
    A simple type built by schema
    """
    text_line = schema.TextLine(title=_(u"A Text Line"), required=False)


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class Typefromschema(dexterity.Item):
    grok.implements(ITypefromschema)
    
    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# type_from_schema_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class SampleView(grok.View):
    grok.context(ITypefromschema)
    grok.require('zope2.View')
    
    # grok.name('view)