from datetime import datetime
from turbogears.database import PackageHub
from sqlobject import *
from turbogears import identity

sqlhub.processConnection = connectionForURI("postgres://sweetter:sweetter@localhost/sweetter")

# class YourDataClass(SQLObject):
#     pass
 
# identity models.
class Visit(SQLObject):
    """
    A visit to your site
    """
    class sqlmeta:
        table = 'visit'

    visit_key = StringCol(length=40, alternateID=True,
                          alternateMethodName='by_visit_key')
    created = DateTimeCol(default=datetime.now)
    expiry = DateTimeCol()

    def lookup_visit(cls, visit_key):
        try:
            return cls.by_visit_key(visit_key)
        except SQLObjectNotFound:
            return None
    lookup_visit = classmethod(lookup_visit)


class VisitIdentity(SQLObject):
    """
    A Visit that is link to a User object
    """
    class sqlmeta:
        table = 'visit_identity'
    visit_key = StringCol(length=40, alternateID=True,
                          alternateMethodName='by_visit_key')
    user_id = IntCol()


class Group(SQLObject):
    """
    An ultra-simple group definition.
    """
    # names like "Group", "Order" and "User" are reserved words in SQL
    # so we set the name to something safe for SQL
    class sqlmeta:
        table = 'tg_group'

    group_name = UnicodeCol(length=16, alternateID=True,
                            alternateMethodName='by_group_name')
    display_name = UnicodeCol(length=255)
    created = DateTimeCol(default=datetime.now)

    # collection of all users belonging to this group
    users = RelatedJoin('User', intermediateTable='user_group',
                        joinColumn='group_id', otherColumn='user_id')

    # collection of all permissions for this group
    permissions = RelatedJoin('Permission', joinColumn='group_id',
                              intermediateTable='group_permission',
                              otherColumn='permission_id')


class Sweets(SQLObject):
    """
    Users comments
    """
    class sqlmeta:
        table = 'sweets'

    comment = UnicodeCol(length=160)
    created = DateTimeCol(default=datetime.now)
    votes = IntCol()

    user = ForeignKey('User',alternateMethodName='by_user_id', cascade=True)

    @classmethod
    def get_num_entries(cls, n=5):
        import datetime
        from sqlobject.sqlbuilder import *
        
        hoy = datetime.datetime.today()
        unasem = hoy + datetime.timedelta(days=-7)
        conn=cls._connection
        sel = conn.sqlrepr(Select((User.q.user_name,\
            func.COUNT(Sweets.q.id)), AND(Sweets.q.userID == User.q.id,\
            Sweets.q.created > unasem), \
            groupBy=User.q.user_name, orderBy=-func.COUNT(Sweets.q.id)))
        
        try:
            tal = list(conn.queryAll(sel)[0:n])
        except:
            tal = []
        return tal

    @classmethod
    def get_num_entries_id(cls, uid):
        from sqlobject.sqlbuilder import *
        import sqlobject
        conn=cls._connection
        sel = conn.sqlrepr(Select((User.q.user_name,\
            func.COUNT(Sweets.q.id)), \
            sqlobject.AND(Sweets.q.userID == User.q.id, Sweets.q.userID == uid),\
            groupBy=User.q.user_name, orderBy=-func.COUNT(Sweets.q.id)))
        tal = list(conn.queryAll(sel))
        if len(tal) > 0:
            return tal[0]
        else: return ['', 0]

class RSS(SQLObject):
    '''
    micro planet
    '''
    class sqlmeta:
        table = 'rss'

    user = ForeignKey('User', cascade=True)
    rss = UnicodeCol()
    tag = UnicodeCol(length=15)
    url = UnicodeCol()
    last_updated = DateTimeCol()
    unique = index.DatabaseIndex(user, rss, unique=True)

class Followers(SQLObject):
    """
    Relation between users
    """
    class sqlmeta:
        table = 'followers'

    follower = ForeignKey('User', cascade=True)
    following = ForeignKey('User', cascade=True)
    unique = index.DatabaseIndex(follower, following, unique=True)

class Todo(SQLObject):
    class sqlmeta:
        table = 'todo'

    sweetid = ForeignKey('Sweets', cascade=True)
    asigned = ForeignKey('User', cascade=True)
    doit = BoolCol()

class UnvalidatedUsers (SQLObject):
    class sqlmeta:
        table = 'unvalidated_users'
    
    user = ForeignKey('User', cascade=True)
    key = UnicodeCol(length=20, alternateMethodName='by_key') 

class Recover(SQLObject):
    class sqlmeta:
        table = 'recover'

    user = ForeignKey('User', cascade=True)
    created = DateTimeCol(default=datetime.now)
    key = UnicodeCol(length=20, alternateMethodName='by_key') 

class Favorites (SQLObject):
    class sqlmeta:
        table = 'favorites'
    
    user = ForeignKey('User', cascade = True)
    sweet = ForeignKey('Sweets', cascade = True)
    unique = index.DatabaseIndex(user, sweet, unique = True)

class Votes(SQLObject):
    class sqlmeta:
        table = 'votes'

    user = ForeignKey('User', cascade=True)
    sweet = ForeignKey('Sweets', cascade=True)
    unique = index.DatabaseIndex(user, sweet, unique=True)

class Replies(SQLObject):
    class sqlmeta:
        table = "replies"

    sweet = ForeignKey('Sweets', cascade=True)
    to = ForeignKey('User', cascade=True)

    unique = index.DatabaseIndex(sweet, to, unique=True)

class User(SQLObject):
    """
    Reasonably basic User definition.
    Probably would want additional attributes.
    """
    # names like "Group", "Order" and "User" are reserved words in SQL
    # so we set the name to something safe for SQL
    class sqlmeta:
        table = 'tg_user'

    user_name = UnicodeCol(length=20, alternateID=True, alternateMethodName='by_user_name')
    email_address = UnicodeCol(length=255, alternateID=True, alternateMethodName='by_email_address')
    url = UnicodeCol(length=255)
    api_key = UnicodeCol(length=32, alternateID=True)
    avatar = UnicodeCol(length=255)
    location = UnicodeCol(length=50, alternateMethodName='by_location')
    display_name = UnicodeCol(length=255)
    password = UnicodeCol(length=40)
    created = DateTimeCol(default=datetime.now)
    karma = FloatCol()
    nvotos = IntCol(default=0)
    nvotos_dia = IntCol(default=0)
    validated = BoolCol(default=0)

    # groups this user belongs to
    groups = RelatedJoin('Group', intermediateTable='user_group',
                         joinColumn='user_id', otherColumn='group_id')

    def _get_permissions(self):
        perms = set()
        for g in self.groups:
            perms = perms | set(g.permissions)
        return perms

    def _set_password(self, cleartext_password):
        "Runs cleartext_password through the hash algorithm before saving."
        password_hash = identity.encrypt_password(cleartext_password)
        self._SO_set_password(password_hash)

    def set_password_raw(self, password):
        "Saves the password as-is to the database."
        self._SO_set_password(password)


class Permission(SQLObject):
    """
    A relationship that determines what each Group can do
    """
    permission_name = UnicodeCol(length=16, alternateID=True,
                                 alternateMethodName='by_permission_name')
    description = UnicodeCol(length=255)

    groups = RelatedJoin('Group',
                         intermediateTable='group_permission',
                         joinColumn='permission_id',
                         otherColumn='group_id')

class Jabber(SQLObject):
    '''
    Lista de usuarios con el jabberbot activo y sus correspondientes
    cuentas
    '''
    class sqlmeta:
        table = 'jabber'

    user = ForeignKey('User', cascade=True)
    jabber = UnicodeCol(length=255, alternateID=True,\
                                 alternateMethodName='by_jabber')
    created = DateTimeCol(default=datetime.now)
    validated = BoolCol(default=0)
    active = BoolCol(default=1)
    unique = index.DatabaseIndex(user, jabber, unique=True)


