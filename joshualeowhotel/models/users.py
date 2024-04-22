from __init__ import db
from flask_login import UserMixin
from models.guest import Guest


class User(UserMixin, db.Document):
    meta = {'collection': 'users'}
    email = db.StringField(max_length=30)
    password = db.StringField()
    name = db.StringField()
    guest = db.EmbeddedDocumentField(Guest)

    @staticmethod
    def getUser(email):
        return User.objects(email=email).first()

    @staticmethod
    def getUserFromGuest(guestObj):
        return User.objects(guest=guestObj).first()

    # guest is None during registration
    @staticmethod
    def createUser(email, name, password):
        user = User.getUser(email)
        if not user:
            user = User(email=email, name=name, password=password, guest=None).save()
        return user

    @staticmethod
    def updatePassword(email, newPassword):
        user = User.getUser(email)
        if user:
            user.password = newPassword
            user.save()
        return user

    # only update guest when make booking
    @staticmethod
    def updateGuest(email, guestObj):
        user = User.getUser(email)
        if user:
            user.guest = guestObj
            user.save()
        return user

    @staticmethod
    def getAllUsers():
        users = list(User.objects())
        return sorted(users, key=lambda user: user.name)

    @staticmethod
    def getAllUsersWithGuest():
        users = User.getAllUsers()
        usersWithGuest = [user for user in users if user.guest and user.guest.passport]
        return sorted(usersWithGuest, key=lambda user: user.guest.passport)
