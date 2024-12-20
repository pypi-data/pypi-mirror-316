from modeltranslation.translator import TranslationOptions, register, translator

from wagtail_modeltranslation.tests.models import (
    BaseInlineModel,
    FieldPanelPage,
    FieldPanelSnippet,
    FieldRowPanelPage,
    FieldRowPanelSnippet,
    ImageChooserPanelPage,
    ImageChooserPanelSnippet,
    InlinePanelPage,
    InlinePanelSnippet,
    MultiFieldPanelPage,
    MultiFieldPanelSnippet,
    PageInlineModel,
    PatchTestPage,
    PatchTestSnippet,
    PatchTestSnippetNoPanels,
    RoutablePageTest,
    SnippetInlineModel,
    StreamFieldPanelPage,
    StreamFieldPanelSnippet,
    TestRootPage,
    TestSlugPage1,
    TestSlugPage1Subclass,
    TestSlugPage2,
    TitleFieldPanelPageTest,
)


# Wagtail Models
@register(TestRootPage)
class TestRootPagePageTranslationOptions(TranslationOptions):
    fields = ()


@register(TestSlugPage1)
class TestSlugPage1TranslationOptions(TranslationOptions):
    fields = ()


@register(TestSlugPage2)
class TestSlugPage2TranslationOptions(TranslationOptions):
    fields = ()


@register(TestSlugPage1Subclass)
class TestSlugPage1SubclassTranslationOptions(TranslationOptions):
    pass


@register(PatchTestPage)
class PatchTestPageTranslationOptions(TranslationOptions):
    fields = ("description",)


@register(PatchTestSnippetNoPanels)
class PatchTestSnippetNoPanelsTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(PatchTestSnippet)
class PatchTestSnippetTranslationOptions(TranslationOptions):
    pass


# Panel Patching Models


class FieldPanelTranslationOptions(TranslationOptions):
    fields = ("name",)


translator.register(FieldPanelPage, FieldPanelTranslationOptions)
translator.register(FieldPanelSnippet, FieldPanelTranslationOptions)


class ImageChooserPanelTranslationOptions(TranslationOptions):
    fields = ("image",)


translator.register(ImageChooserPanelPage, ImageChooserPanelTranslationOptions)
translator.register(ImageChooserPanelSnippet, ImageChooserPanelTranslationOptions)


class FieldRowPanelTranslationOptions(TranslationOptions):
    fields = ("other_name",)


translator.register(FieldRowPanelPage, FieldRowPanelTranslationOptions)
translator.register(FieldRowPanelSnippet, FieldRowPanelTranslationOptions)


class StreamFieldPanelTranslationOptions(TranslationOptions):
    fields = ("body",)


translator.register(StreamFieldPanelPage, StreamFieldPanelTranslationOptions)
translator.register(StreamFieldPanelSnippet, StreamFieldPanelTranslationOptions)


class MultiFieldPanelTranslationOptions(TranslationOptions):
    fields = (
        "name",
        "image",
        "other_name",
    )


translator.register(MultiFieldPanelPage, MultiFieldPanelTranslationOptions)
translator.register(MultiFieldPanelSnippet, MultiFieldPanelTranslationOptions)


class InlinePanelTranslationOptions(TranslationOptions):
    fields = (
        "name",
        "image",
        "other_name",
        "field_name",
        "image_chooser",
        "fieldrow_name",
    )


translator.register(BaseInlineModel, InlinePanelTranslationOptions)


class InlinePanelTranslationOptions(TranslationOptions):
    fields = ()


translator.register(PageInlineModel, InlinePanelTranslationOptions)
translator.register(SnippetInlineModel, InlinePanelTranslationOptions)


@register(InlinePanelPage)
class InlinePanelModelTranslationOptions(TranslationOptions):
    fields = ()


translator.register(InlinePanelSnippet, InlinePanelModelTranslationOptions)


@register(RoutablePageTest)
class RoutablePageTestTranslationOptions(TranslationOptions):
    fields = ()


@register(TitleFieldPanelPageTest)
class TitleFieldPanelPageTestTranslationOptions(TranslationOptions):
    fields = ("name",)
