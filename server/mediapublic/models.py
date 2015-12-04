import six
import sys
from uuid import uuid4

import sqlalchemy.exc as sql_exc
from sqlalchemy.sql import func
from sqlalchemy_utils import UUIDType, JSONType
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    UnicodeText,
    DateTime,
)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    relationship,
    scoped_session,
    sessionmaker,
)

from zope.sqlalchemy import ZopeTransactionExtension
import transaction

DBSession = scoped_session(sessionmaker(
    extension=ZopeTransactionExtension(),
    expire_on_commit=False))
Base = declarative_base()


class TimeStampMixin(object):
    creation_datetime = Column(DateTime, server_default=func.now())
    modified_datetime = Column(DateTime, server_default=func.now())


class ExtraFieldMixin(object):
    extra = Column(JSONType, nullable=True)

    def to_dict(self):
        return dict(extra=self.extra)


class CreationMixin():
    @classmethod
    def add(cls, **kwargs):
        with transaction.manager:
            thing = cls(**kwargs)
            if thing.id is None:
                thing.id = uuid4()
            DBSession.add(thing)
            transaction.commit()
        return thing

    @classmethod
    def get_all(cls):
        with transaction.manager:
            things = DBSession.query(
                cls,
            ).all()
        return things

    @classmethod
    def get_by_id(cls, id):
        with transaction.manager:
            try:
                thing = DBSession.query(
                    cls,
                ).filter(
                    cls.id == id,
                ).first()
            except sql_exc.StatementError as e:
                if isinstance(e.orig, (ValueError,)):
                    raise e.orig
                six.reraise(*sys.exc_info())
        return thing

    @classmethod
    def delete_by_id(cls, id):
        with transaction.manager:
            thing = cls.get_by_id(id)
            if thing is not None:
                DBSession.delete(thing)
            transaction.commit()
        return thing

    @classmethod
    def update_by_id(cls, id, **kwargs):
        with transaction.manager:
            keys = set(cls.__dict__)
            thing = cls.get_by_id(id)
            if thing is not None:
                for k in kwargs:
                    if k in keys:
                        setattr(thing, k, kwargs[k])
                DBSession.add(thing)
                transaction.commit()
        return thing

    @classmethod
    def reqkeys(cls):
        keys = []
        for key in cls.__table__.columns:
            if '__required__' in type(key).__dict__:
                keys.append(six.text_type(key).split('.')[1])
        return keys

    def to_dict(self):
        return {
            'id': self.id,
            'creation_datetime': six.text_type(self.creation_datetime),
        }


class UserTypes(Base, CreationMixin, TimeStampMixin, ExtraFieldMixin):
    __tablename__ = 'user_types'

    id = Column(UUIDType(binary=False), primary_key=True)
    name = Column(UnicodeText, nullable=False)
    description = Column(UnicodeText, nullable=False)
    value = Column(Integer, nullable=False)

    def _to_dict(self):
        return dict(
            name=self.name,
            description=self.description,
            value=self.value,
        )

    def to_dict(self):
        resp = {}
        for klass in reversed(self.__class__.__mro__[1:]):
            try:
                resp.update(klass.to_dict(self))
            except AttributeError:
                pass
        resp.update(self._to_dict())
        return resp


class Users(Base, CreationMixin, TimeStampMixin, ExtraFieldMixin):
    __tablename__ = 'users'

    id = Column(UUIDType(binary=False), primary_key=True)
    display_name = Column(UnicodeText, nullable=False)
    email = Column(UnicodeText, nullable=False)
    last_longin_datetime = Column(DateTime, server_default=func.now())

    signup_date = Column(DateTime, server_default=func.now())

    twitter_handle = Column(UnicodeText, unique=True)
    twitter_user_id = Column(UnicodeText, unique=True)
    twitter_auth_token = Column(UnicodeText)
    twitter_auth_secret = Column(UnicodeText)
    profile_photo_url = Column(UnicodeText)

    user_type_id = Column(ForeignKey('user_types.id'))
    organization_id = Column(ForeignKey('organizations.id'))

    @classmethod
    def update_social_login(cls, social_uname, auth_info, provider='twitter'):
        try:
            user = Users.add(
                email="%s@%s.social.auth" % (social_uname, provider),
                display_name=auth_info["profile"]["name"]["formatted"],
                twitter_handle=six.text_type(social_uname),
                profile_photo_url=auth_info["profile"]["photos"][0]["value"],
                twitter_auth_secret=auth_info[
                    "credentials"]["oauthAccessTokenSecret"],
                twitter_auth_token=auth_info[
                    "credentials"]["oauthAccessToken"],
                twitter_user_id=auth_info["profile"]["accounts"][0]['userid'],
            )
        except sql_exc.IntegrityError:
            with transaction.manager:
                DBSession.query(cls).filter(
                    cls.twitter_handle == six.text_type(social_uname),
                ).update(
                    values=dict(
                        twitter_auth_secret=auth_info[
                            "credentials"]["oauthAccessTokenSecret"],
                        twitter_auth_token=auth_info[
                            "credentials"]["oauthAccessToken"],
                        twitter_user_id=auth_info[
                            "profile"]["accounts"][0]['userid'],
                    )
                )
                user = DBSession.query(cls).filter(
                    cls.twitter_handle == six.text_type(social_uname)
                ).first()
            return True, user.id

        return False, user.id

    def _to_dict(self):
        return dict(
            display_name=self.display_name,
            twitter_handle=self.twitter_handle,
            email=self.email,
            user_type=self.user_type_id,
            organization_id=self.organization_id,
        )

    def to_dict(self):
        resp = {}
        for klass in reversed(self.__class__.__mro__[1:]):
            try:
                resp.update(klass.to_dict(self))
            except AttributeError:
                pass
        resp.update(self._to_dict())
        return resp


class Comments(Base, CreationMixin, TimeStampMixin):
    __tablename__ = 'comments'

    id = Column(UUIDType(binary=False), primary_key=True)
    subject = Column(UnicodeText)
    contents = Column(UnicodeText, nullable=False)

    parent_comment_id = Column(ForeignKey('comments.id'))

    author_id = Column(ForeignKey('users.id'), nullable=False)

    organization_id = Column(ForeignKey('organizations.id'))
    people_id = Column(ForeignKey('people.id'))
    recording_id = Column(ForeignKey('recordings.id'))
    howto_id = Column(ForeignKey('howtos.id'))
    blog_id = Column(ForeignKey('blogs.id'))

    def _to_dict(self):
        return dict(
            subject=self.subject,
            contents=self.contents,
            parent_comment_id=self.parent_comment_id,
            author_id=self.author_id,
        )

    def to_dict(self):
        resp = {}
        for klass in reversed(self.__class__.__mro__[1:]):
            try:
                resp.update(klass.to_dict(self))
            except AttributeError:
                pass
        resp.update(self._to_dict())
        return resp

    @classmethod
    def get_by_organization_id(cls, id):
        with transaction.manager:
            comments = DBSession.query(
                Comments,
            ).filter(
                Comments.organization_id == id,
            ).all()
        return comments

    @classmethod
    def get_by_people_id(cls, id):
        with transaction.manager:
            comments = DBSession.query(
                Comments,
            ).filter(
                Comments.people_id == id,
            ).all()
        return comments

    @classmethod
    def get_by_recording_id(cls, id):
        with transaction.manager:
            comments = DBSession.query(
                Comments,
            ).filter(
                Comments.recording_id == id,
            ).all()
        return comments

    @classmethod
    def get_by_howto_id(cls, id):
        with transaction.manager:
            comments = DBSession.query(
                Comments,
            ).filter(
                Comments.howto_id == id,
            ).all()
        return comments

    @classmethod
    def get_by_blog_id(cls, id):
        with transaction.manager:
            comments = DBSession.query(
                Comments,
            ).filter(
                Comments.blog_id == id,
            ).all()
        return comments


class Organizations(Base, CreationMixin, TimeStampMixin):
    __tablename__ = 'organizations'

    id = Column(UUIDType(binary=False), primary_key=True)
    short_name = Column(UnicodeText, nullable=False)
    long_name = Column(UnicodeText)
    long_description = Column(UnicodeText)

    address_0 = Column(UnicodeText)
    address_1 = Column(UnicodeText)
    city = Column(UnicodeText)
    state = Column(UnicodeText)
    zipcode = Column(UnicodeText)

    phone = Column(UnicodeText)
    fax = Column(UnicodeText)
    primary_website = Column(UnicodeText)
    secondary_website = Column(UnicodeText)
    image_url = Column(UnicodeText)

    def _to_dict(self):
        return dict(
            short_name=self.short_name,
            long_name=self.long_name,
            long_description=self.long_description,
            address_0=self.address_0,
            address_1=self.address_1,
            city=self.city,
            state=self.state,
            zipcode=self.zipcode,
            phone=self.phone,
            fax=self.fax,
            primary_website=self.primary_website,
            secondary_website=self.secondary_website,
            image_url=self.image_url,
        )

    def to_dict(self):
        resp = {}
        for klass in reversed(self.__class__.__mro__[1:]):
            try:
                resp.update(klass.to_dict(self))
            except AttributeError:
                pass
        resp.update(self._to_dict())
        return resp


class PlaylistAssignments(Base, CreationMixin, TimeStampMixin):
    __tablename__ = 'playlist_assignments'

    id = Column(UUIDType(binary=False), primary_key=True)
    playlist_id = Column(ForeignKey('playlists.id'), nullable=False)
    recording_id = Column(ForeignKey('recordings.id'), nullable=False)

    @classmethod
    def delete_by_playlist_id_and_recording_id(cls, pid, rid):
        success = False
        with transaction.manager:
            playlist = DBSession.query(
                PlaylistAssignments,
            ).filter(
                PlaylistAssignments.playlist_id == pid,
                PlaylistAssignments.recording_id == rid,
            ).first()
            if playlist is not None:
                DBSession.remove(playlist)
                transaction.commit()
                success = True
        return success

    def to_dict(self):
        resp = {}
        for klass in reversed(self.__class__.__mro__[1:]):
            try:
                resp.update(klass.to_dict(self))
            except AttributeError:
                pass
        resp.update(
            playlist_id=self.playlist_id,
            recording_id=self.recording_id,
        )
        return resp


class Playlists(Base, CreationMixin, TimeStampMixin):
    __tablename__ = 'playlists'

    id = Column(UUIDType(binary=False), primary_key=True)
    author_id = Column(ForeignKey('people.id'))
    title = Column(UnicodeText, nullable=False)
    description = Column(UnicodeText)

    recordings = relationship(
        "Recordings",
        secondary=PlaylistAssignments.__table__,
        backref="playlists",
    )

    @classmethod
    def get_by_owner_id(cls, id):
        with transaction.manager:
            playlists = DBSession.query(
                Playlists,
            ).filter(
                Playlists.author_id == id,
            ).all()
        return playlists

    @classmethod
    def remove_recording_ny_id(cls, pid, rid):
        with transaction.manager:
            assignment = DBSession.query(
                PlaylistAssignments,
            ).filter(
                PlaylistAssignments.playlist_id == pid,
                PlaylistAssignments.recording_id == rid,
            ).first()
            DBSession.delete(assignment)

    @classmethod
    def get_recordings_by_playlist_id(self, id):
        with transaction.manager:
            recordings = DBSession.query(
                Recordings,
            ).join(
                PlaylistAssignments,
            ).filter(
                PlaylistAssignments.playlist_id == id,
            ).all()
            if recordings is None:
                recordings = []
            if not isinstance(recordings, list):
                recordings = [recordings]
        return recordings

    def to_dict(self):
        resp = {}
        for klass in reversed(self.__class__.__mro__[1:]):
            try:
                resp.update(klass.to_dict(self))
            except AttributeError:
                pass
        resp.update(
            author_id=self.author_id,
            title=self.title,
            # This should cause a LEFT JOIN against the many-to-many
            # recording_assignments table, and get the recordings
            # that are associated with the playlist
            # recordings = [r.to_dict() for r in self.recordings]
            recordings=[r.to_dict() for r in
                        Playlists.get_recordings_by_playlist_id(self.id)],
        )
        return resp


class People(Base, CreationMixin, TimeStampMixin):
    __tablename__ = 'people'

    id = Column(UUIDType(binary=False), primary_key=True)
    first = Column(UnicodeText, nullable=False)
    last = Column(UnicodeText, nullable=False)
    address_0 = Column(UnicodeText)
    address_1 = Column(UnicodeText)
    city = Column(UnicodeText)
    state = Column(UnicodeText)
    zipcode = Column(UnicodeText)
    phone = Column(UnicodeText)
    fax = Column(UnicodeText)
    primary_website = Column(UnicodeText)
    secondary_website = Column(UnicodeText)

    # these should probably be brough out into a seperate table as
    # many to one so we don't have to keep adding columns ...
    twitter = Column(UnicodeText)
    facebook = Column(UnicodeText)
    instagram = Column(UnicodeText)
    periscope = Column(UnicodeText)

    user_id = Column(ForeignKey('users.id'))

    organization_id = Column(ForeignKey('organizations.id'))

    def _to_dict(self):
        return dict(
            first=self.first,
            last=self.last,
            address_0=self.address_0,
            address_1=self.address_1,
            city=self.city,
            state=self.state,
            zipcode=self.zipcode,
            phone=self.phone,
            fax=self.fax,
            primary_website=self.primary_website,
            secondary_website=self.secondary_website,

            # see note on definitions
            twitter=self.twitter,
            facebook=self.facebook,
            instagram=self.instagram,
            periscope=self.periscope,
            user_id=self.user_id,
            organization_id=self.organization_id,
        )

    def to_dict(self):
        resp = {}
        for klass in reversed(self.__class__.__mro__[1:]):
            try:
                resp.update(klass.to_dict(self))
            except AttributeError:
                pass
        resp.update(self._to_dict())
        return resp

    @classmethod
    def get_by_organization_id(cls, id):
        with transaction.manager:
            people = DBSession.query(
                People,
            ).filter(
                People.organization_id == id,
            ).all()
        return people


class Recordings(Base, CreationMixin, TimeStampMixin):
    __tablename__ = 'recordings'

    id = Column(UUIDType(binary=False), primary_key=True)
    title = Column(UnicodeText, nullable=False)
    url = Column(UnicodeText, nullable=False)
    recorded_datetime = Column(DateTime)

    organization_id = Column(ForeignKey('organizations.id'))

    def to_dict(self):
        resp = {}
        for klass in reversed(self.__class__.__mro__[1:]):
            try:
                resp.update(klass.to_dict(self))
            except AttributeError:
                pass
        resp.update(
            title=self.title,
            url=self.url,
            recorded_datetime=self.recorded_datetime,
            organization_id=self.organization_id,
        )
        return resp

    @classmethod
    def get_by_organization_id(cls, id):
        with transaction.manager:
            recordings = DBSession.query(
                Recordings,
            ).filter(
                Recordings.organization_id == id,
            ).all()
        return recordings


class RecordingCategories(Base, CreationMixin, TimeStampMixin):

    __tablename__ = 'recording_categories'

    id = Column(UUIDType(binary=False), primary_key=True)
    name = Column(UnicodeText, nullable=False)
    short_description = Column(UnicodeText)
    long_description = Column(UnicodeText)

    def to_dict(self):
        resp = {}
        for klass in reversed(self.__class__.__mro__[1:]):
            try:
                resp.update(klass.to_dict(self))
            except AttributeError:
                pass
        resp.update(
            name=self.name,
            short_description=self.short_description,
            long_description=self.long_description,
        )
        return resp


class RecordingCategoryAssignments(Base, CreationMixin, TimeStampMixin):
    __tablename__ = 'recording_category_assignments'

    id = Column(UUIDType(binary=False), primary_key=True)
    recording_category_id = Column(ForeignKey('recording_categories.id'),
                                   nullable=False)
    recording_id = Column(ForeignKey('recordings.id'), nullable=False)

    def to_dict(self):
        resp = {}
        for klass in reversed(self.__class__.__mro__[1:]):
            try:
                resp.update(klass.to_dict(self))
            except AttributeError:
                pass
        resp.update(
            recording_category_id=self.recording_category_id,
            recording_id=self.recording_id,
        )
        return resp


class Howtos(Base, CreationMixin, TimeStampMixin):
    __tablename__ = 'howtos'

    id = Column(UUIDType(binary=False), primary_key=True)
    title = Column(UnicodeText, nullable=False)
    contents = Column(UnicodeText, nullable=False)
    edit_datetime = Column(DateTime)
    tags = Column(UnicodeText)

    def to_dict(self):
        resp = {}
        for klass in reversed(self.__class__.__mro__[1:]):
            try:
                resp.update(klass.to_dict(self))
            except AttributeError:
                pass
        resp.update(
            title=self.title,
            contents=self.contents,
            edit_datetime=self.edit_datetime,
            tags=self.tags,
        )
        return resp


class HowtoCategories(Base, CreationMixin, TimeStampMixin):
    __tablename__ = 'howto_categories'

    id = Column(UUIDType(binary=False), primary_key=True)
    name = Column(UnicodeText, nullable=False)
    short_description = Column(UnicodeText)
    long_description = Column(UnicodeText)

    def to_dict(self):
        resp = {}
        for klass in reversed(self.__class__.__mro__[1:]):
            try:
                resp.update(klass.to_dict(self))
            except AttributeError:
                pass
        resp.update(
            name=self.name,
            short_description=self.short_description,
            long_description=self.long_description,
        )
        return resp


class HowtoCategoryAssignments(Base, CreationMixin, TimeStampMixin):
    __tablename__ = 'howto_category_assignments'

    id = Column(UUIDType(binary=False), primary_key=True)
    howto_category_id = Column(ForeignKey('howto_categories.id'),
                               nullable=False)
    howto_id = Column(ForeignKey('howtos.id'), nullable=False)

    def to_dict(self):
        resp = {}
        for klass in reversed(self.__class__.__mro__[1:]):
            try:
                resp.update(klass.to_dict(self))
            except AttributeError:
                pass
        resp.update(
            howto_category_id=self.howto_category_id,
            howto_id=self.howto_id,
        )
        return resp


class Blogs(Base, CreationMixin, TimeStampMixin):
    __tablename__ = 'blogs'

    id = Column(UUIDType(binary=False), primary_key=True)
    title = Column(UnicodeText, nullable=False)
    contents = Column(UnicodeText, nullable=False)
    edit_datetime = Column(DateTime)
    tags = Column(UnicodeText)

    author_id = Column(ForeignKey('users.id'))

    def to_dict(self):
        resp = {}
        for klass in reversed(self.__class__.__mro__[1:]):
            try:
                resp.update(klass.to_dict(self))
            except AttributeError:
                pass
        resp.update(
            title=self.title,
            contents=self.contents,
            edit_datetime=self.edit_datetime,
            tags=self.tags,
            author_id=self.author_id,
        )
        return resp
