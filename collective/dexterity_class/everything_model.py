from five import grok
from plone.directives import dexterity, form

from zope import schema

from z3c.form import group, field
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget

from collective.dexterity_class import MessageFactory as _


# Interface class; used to define content-type schema.

class IEverythingModel(form.Schema):
    """
    Everything type built via model.
    """
    
    # If you want a schema-defined interface, delete the form.model
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/everything_model.xml to define the content type
    # and add directives here as necessary.
    
    form.model("models/everything_model.xml")
    
    form.fieldset(
        "attachments", 
        label=_("Attachments"),
        fields=['file_upload', 'image_field'],
        )


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class EverythingModel(dexterity.Item):
    grok.implements(IEverythingModel)
    
    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# everything_model_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class SampleView(grok.View):
    grok.context(IEverythingModel)
    grok.require('zope2.View')
    
    # grok.name('view)