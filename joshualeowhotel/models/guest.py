from mongoengine import EmbeddedDocument, StringField


class Guest(EmbeddedDocument):
    passport = StringField()
    country = StringField()
