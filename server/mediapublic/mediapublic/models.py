from sqlalchemy import (
    Column,
    Index,
    ForeignKey,
    Integer,
    Text,
    UnicodeText,
    DateTime,
    
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

import transaction

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension(), expire_on_commit=False))
Base = declarative_base()

class CreationMixin():

    @classmethod
    def add(cls, **kwargs):
        with transaction.manager:
            thing = cls(**kwargs)
            DBSession.add(thing)
            transaction.commit()
        return thing

    @classmethod
    def get_all(cls):
        with transaction.manager:
            things = DBSession.query(
                cls,
            ).all()
            #retThings = []
            #for t in things:
            #    retThings.append(t.to_dict())
        #return retThings
        return things

    @classmethod
    def get_by_id(cls, id):
        with transaction.manager:
            thing = DBSession.query(
                cls,
            ).filter(
                cls.id == id,
            ).first()
        return thing

    @classmethod
    def delete_by_id(cls, id):
        with transaction.manager:
            thing = cls.get_by_id(id)
            if not thing is None:
                DBSession.delete(thing)
            transaction.commit()
        return thing

    @classmethod
    def update_by_id(cls, id, **kwargs):
        print '\nupdate_by_id(), args:'
        #print args
        with transaction.manager:
            keys = set(cls.__dict__)
            thing = cls.get_by_id(id)
            if not thing is None:
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
                keys.append(str(key).split('.')[1])
        return keys

class ReqColumn(Column):

    __required__ = True

class UserTypes(Base, CreationMixin):

    __tablename__ = 'user_types'

    id = Column(Integer, primary_key=True)
    name = ReqColumn(UnicodeText)
    description = ReqColumn(UnicodeText)
    value = ReqColumn(Integer)
    creation_datetime = Column(DateTime)
    
    def to_dict(self):
        resp = dict(
            id = self.id,
            name = self.name,
            description = self.description,
            value = self.value,
        )
        return resp

class Users(Base, CreationMixin):

    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    unique = Column(Text)
    first = ReqColumn(UnicodeText)
    last = ReqColumn(UnicodeText)
    email = ReqColumn(UnicodeText)
    twitter = ReqColumn(UnicodeText)
    creation_datetime = Column(UnicodeText)
    last_longin_datetime = Column(UnicodeText)
    
    user_type_id = ReqColumn(ForeignKey('user_types.id'))
    
    organization_id = Column(ForeignKey('organizations.id'), nullable=True)
    
    def to_dict(self):
        resp = dict(
            id = self.id,
            first = self.first,
            last = self.last,
            email = self.email,
            user_type = self.user_type_id,
            organization_id = self.organization_id,
        )
        return resp
        
class Comments(Base, CreationMixin):

    __tablename__ = 'comments'
    
    id = Column(Integer, primary_key=True)
    subject = ReqColumn(UnicodeText)
    contents = ReqColumn(UnicodeText)
    creation_datetime = Column(DateTime)
    
    parent_comment_id = ReqColumn(Integer, ForeignKey('comments.id'))
    
    author_id = ReqColumn(Integer, ForeignKey('users.id'))
    
    organization_id = Column(ForeignKey('organizations.id'), nullable=True)
    people_id = Column(ForeignKey('people.id'), nullable=True)
    recording_id = Column(ForeignKey('recordings.id'), nullable=True)
    howto_id = Column(ForeignKey('howtos.id'), nullable=True)
    blog_id = Column(ForeignKey('blogs.id'), nullable=True)
    
    def to_dict(self):
        resp = dict(
            id = self.id,
            subject = self.subject,
            contents = self.contents,
            creation_datetime = str(self.creation_datetime),
            parent_comment_id = self.parent_comment_id,
            author_id = self.author_id,
        )
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
        
class Organizations(Base, CreationMixin):

    __tablename__ = 'organizations'
    
    id = Column(Integer, primary_key=True)
    short_name = ReqColumn(UnicodeText)
    long_name = ReqColumn(UnicodeText)
    short_description = ReqColumn(UnicodeText)
    long_description = ReqColumn(UnicodeText)
    
    address_0 = ReqColumn(UnicodeText)
    address_1 = ReqColumn(UnicodeText)
    city = ReqColumn(UnicodeText)
    state = ReqColumn(UnicodeText)
    zipcode = ReqColumn(UnicodeText)
    
    phone = ReqColumn(UnicodeText)
    fax = ReqColumn(UnicodeText)
    primary_website = ReqColumn(UnicodeText)
    secondary_website = ReqColumn(UnicodeText)
    
    creation_datetime = Column(DateTime)
  
    def to_dict(self):
        resp = dict(
            id = self.id,
            short_name = self.short_name,
            long_name = self.long_name,
            short_description = self.short_description,
            long_description = self.long_description,
            address_0 = self.address_0,
            address_1 = self.address_1,
            city = self.city,
            state = self.state,
            zipcode = self.zipcode,
            phone = self.phone,
            fax = self.fax,
            primary_website = self.primary_website,
            secondary_website = self.secondary_website,
            creation_datetime = str(self.creation_datetime),
        )
        return resp    
    
class People(Base, CreationMixin):

    __tablename__= 'people'

    id = Column(Integer, primary_key=True)
    first = ReqColumn(UnicodeText)
    last = ReqColumn(UnicodeText)
    address_0 = ReqColumn(UnicodeText)
    address_1 = ReqColumn(UnicodeText)
    city = ReqColumn(UnicodeText)
    state = ReqColumn(UnicodeText)
    zipcode = ReqColumn(UnicodeText)
    phone = ReqColumn(UnicodeText)
    fax = ReqColumn(UnicodeText)
    primary_website = ReqColumn(UnicodeText)
    secondary_website = ReqColumn(UnicodeText)
    creation_datetime = Column(DateTime)
    
    # these should probably be brough out into a seperate table as
    # many to one so we don't have to keep adding colyumns ...
    twitter = ReqColumn(UnicodeText)
    facebook = ReqColumn(UnicodeText)
    instagram = ReqColumn(UnicodeText)
    parascope = ReqColumn(UnicodeText)
    
    user_id = ReqColumn(ForeignKey('users.id'), nullable=True)
    
    organization_id = Column(ForeignKey('organizations.id'), nullable=True)
    
    def to_dict(self):
        resp = dict(
            id = self.id,
            first = self.first,
            address_0 = self.address_0,
            address_1 = self.address_1,
            city = self.city,
            state = self.state,
            zipcode = self.zipcode,
            phone = self.phone,
            fax = self.fax,
            primary_website = self.primary_website,
            secondary_website = self.secondary_website,
            creation_datetime = str(self.creation_datetime),
            
            # see note on definitions
            twitter = self.twitter,
            facebook = self.facebook,
            instagram = self.instagram,
            parascope = self.parascope,
            
            user_id = self.user_id,
            organization_id = self.organization_id,
        )
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

class Recordings(Base, CreationMixin):

    __tablename__= 'recordings'

    id = Column(Integer, primary_key=True)
    title = ReqColumn(UnicodeText)
    url = ReqColumn(UnicodeText)
    recorded_datetime = ReqColumn(DateTime)
    creation_datetime = Column(DateTime)
    
    organization_id = Column(Integer, ForeignKey('organizations.id'))

    def to_dict(self):
        resp = dict(
            id = self.id,
            title = self.title,
            url = self.url,
            recorded_datetime = str(self.recorded_datetime),
            creation_datetime = str(self.creation_datetime),
            organization_id = self.organization_id,
        )
        return resp

    @classmethod
    def get_by_organization_id(cls, id):
        with transaction.manager:
            recordings = DBSession.query(
                Recordings,
            #    RecordingCategories,
            ).filter(
                Recordings.organization_id == id,
            #).join(
            #    RecordingCategoryAssignments,
            ).all()
        return recordings

class RecordingCategories(Base, CreationMixin):

    __tablename__ = 'recording_categories'

    id = Column(Integer, primary_key=True)
    name = ReqColumn(UnicodeText)
    short_description = ReqColumn(UnicodeText)
    long_description = ReqColumn(UnicodeText)
    creation_datetime = Column(DateTime)
    
    def to_dict(self):
        resp = dict(
            id = self.id,
            name = self.name,
            short_description = self.short_description,
            long_description = self.long_description,
            creation_datetime = str(self.creation_datetime),
        )
        return resp

class RecordingCategoryAssignments(Base, CreationMixin):

    __tablename__ = 'recording_category_assignments'

    id = Column(Integer, primary_key=True)
    recording_category_id = ReqColumn(Integer, ForeignKey('recording_categories.id'))
    recording_id = ReqColumn(Integer, ForeignKey('recordings.id'))
    creation_datetime = Column(DateTime)

    def to_dict(self):
        resp = dict(
            id = self.id,
            recording_category_id = self.recording_category_id,
            recording_id = self.recording_id,
            creation_datetime = str(self.creation_datetime),
        )
        return resp

class Howtos(Base, CreationMixin):

    __tablename__ = 'howtos'

    id = Column(Integer, primary_key=True)
    title = ReqColumn(UnicodeText)
    contents = ReqColumn(UnicodeText)
    creation_datetime = Column(DateTime)
    edit_datetime = Column(DateTime)
    tags = ReqColumn(UnicodeText)
    
    def to_dict(self):
        resp = dict(
            id = self.id,
            title = self.title,
            contents = self.contents,
            creation_datetime = str(self.creation_datetime),
            edit_datetime = self.edit_datetime,
            tags = self.tags,
        )
        return resp
    
class HowtoCategories(Base, CreationMixin):

    __tablename__ = 'howto_categories'
    
    id = Column(Integer, primary_key=True)
    name = ReqColumn(UnicodeText)
    short_description = ReqColumn(UnicodeText)
    long_description = ReqColumn(UnicodeText)
    creation_datetime = Column(DateTime)
    
    def to_dict(self):
        resp = dict(
            id = self.id,
            name = self.name,
            short_description = self.short_description,
            long_description = self.long_description,
            creation_datetime = str(self.creation_datetime),
        )
        return resp

class HowtoCategoryAssignments(Base, CreationMixin):

    __tablename__ = 'howto_category_assignments'
    
    id = Column(Integer, primary_key=True)
    howto_category_id = ReqColumn(Integer, ForeignKey('howto_categories.id'))
    howto_id = ReqColumn(Integer, ForeignKey('howtos.id'))
    creation_datetime = Column(DateTime)
    
    def to_dict(self):
        resp = dict(
            id = self.id,
            howto_category_id = self.howto_category_id,
            howto_id = self.howto_id,
            creation_datetime = str(self.creation_datetime),
        )
        return resp
        
class Blogs(Base, CreationMixin):

    __tablename__ = 'blogs'
    
    id = Column(Integer, primary_key=True)
    title = ReqColumn(UnicodeText)
    contents = ReqColumn(UnicodeText)
    creation_datetime = Column(DateTime)
    edit_datetime = Column(DateTime)
    tags = ReqColumn(UnicodeText)
    
    author_id = Column(ForeignKey('users.id'))

    def to_dict(self):
        resp = dict(
            id = self.id,
            title = self.title,
            contents = self.contents,
            creation_datetime = str(self.creation_datetime),
            edit_datetime = self.edit_datetime,
            tags = self.tags,
            author_id = self.author_id,
        )
        return resp
