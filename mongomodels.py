from mongoengine import Document, StringField, ListField, DateTimeField, IntField, BooleanField, ObjectIdField, \
    DictField


class FileAction(Document):
    """ Document that inherits from :class:`mongoengine.Document`. Holds information for the fileaction collection.

    
    :property projectId: id of the project, which belongs to the file action (type: :class:`mongoengine.fields.ObjectIdField`)
    :property fileId: id of the file, which belongs to the file action (type: :class:`mongoengine.fields.ObjectIdField`)
    :property revisionHash: hash of the revision (type: :class:`mongoengine.fields.StringField`)
    :property mode: mode of the file action (type: :class:`mongoengine.fields.StringField`)
    
        .. NOTE:: It can only be ("A")dded, ("D")eleted, ("M")odified, ("C")opied or Moved, "T" for links (special in git)
        
    :property sizeAtCommit: size of the file on commit (type: :class:`mongoengine.fields.IntField`)
    :property linesAdded: number of lines added in this action (type: :class:`mongoengine.fields.IntField`)
    :property linesDeleted: number of lines deleted in this action (type: :class:`mongoengine.fields.IntField`)
    :property isBinary: indicates if the file is a binary file or not (type: :class:`mongoengine.fields.BooleanField`)
    :property oldFilePathId: object id of old file (if it was moved or copied) (type: :class:`mongoengine.fields.ObjectIdField`)
    :property hunkIds: list of ids to the different hunks of this action (type: :class:`mongoengine.fields.ListField(:class:`mongoengine.fields.ObjectIdField`)`)
        
    .. NOTE:: Unique (or primary key) are the fields: projectId, fileId, and revisionHash.
    
    .. NOTE:: oldFilePathId only exists, if the file was created due to a copy or move action
    

    """
    meta = {
        'indexes': [
            'projectId',
            ('projectId', 'revisionHash'),
        ],
        'shard_key': ('revisionHash', 'projectId', 'fileId'),
    }

    MODES = ('A', 'M', 'D', 'C', 'T')
    #pk fileId, revisionhash, projectId
    projectId = ObjectIdField(required=True)
    fileId = ObjectIdField(required=True)
    revisionHash = StringField(max_length=50, required=True,unique_with=['projectId', 'fileId'])
    mode = StringField(max_length=1, required=True, choices=MODES)
    sizeAtCommit = IntField()
    linesAdded = IntField()
    linesDeleted = IntField()
    isBinary = BooleanField()

    # oldFilePathId is only set, if we detected a copy or move operation
    oldFilePathId = ObjectIdField()
    hunkIds = ListField(ObjectIdField())
    
        
    


class Hunk(Document):
    """ Document that inherits from :class:`mongoengine.Document`. Holds information for the hunk collection.
    :property new_start: new starting of the hunk in new file
    :property new_lines: number of new lines
    :property old_start: old start of the hunk in the old file
    :property old_lines: old number of lines
    :property content: content of the hunk.

    For more information: https://en.wikipedia.org/wiki/Diff#Unified_format)
    """
    meta = {
        'indexes': [
            '#id',
        ],
        'shard_key': ('id',),
    }

    new_start = IntField(required=True)
    new_lines = IntField(required=True)
    old_start = IntField(required=True)
    old_lines = IntField(required=True)
    content = StringField(required=True)


class File(Document):
    """ Document that inherits from :class:`mongoengine.Document`. Holds information for the file collection.
    
    :property projectId: id of the project, which belongs to the file action (type: :class:`mongoengine.fields.ObjectIdField`)
    :property path: path of the file (type: :class:`mongoengine.fields.StringField`)
    :property name: name of the file (type: :class:`mongoengine.fields.StringField`)
    
    .. NOTE:: Unique (or primary key) are the fields: path, name, and projectId.
    """
    meta = {
        'indexes': [
            'projectId',
        ],
        'shard_key': ('path', 'projectId',),
    }

    #PK path, name, projectId
    projectId = ObjectIdField(required=True)
    path = StringField(max_length=300, required=True,unique_with=['projectId'] )
    name = StringField(max_length=100, required=True)

class Tag(Document):
    """ Document that inherits from :class:`mongoengine.Document`. Holds information for the tag collection.
    
    :property projectId: id of the project, which belongs to the file action (type: :class:`mongoengine.fields.ObjectIdField`)
    :property name: name of the tag (type: :class:`mongoengine.fields.StringField`)
    :property message: message of the tag (type: :class:`mongoengine.fields.StringField`)
    :property taggerId: id of the person who created the tag (type: :class:`mongoengine.fields.ObjectIdField`)
    :property date: date of the creation of the tag (type: :class:`mongoengine.fields.DateTimeField`)
    :property offset: offset of the tag creation date for timezones (type: :class:`mongoengine.fields.IntField`)
    
    .. NOTE:: Unique (or primary key) are the fields: name and projectId.
    """
    meta = {
        'indexes': [
            'projectId',
        ],
        'shard_key': ('projectId', 'name'),
    }
    
     #PK: project, name
    projectId = ObjectIdField(required=True,unique_with=['name'])
    name = StringField(max_length=150, required=True)
    message = StringField()
    taggerId = ObjectIdField()
    date = DateTimeField()
    offset = IntField()
    
class People(Document):
    """ Document that inherits from :class:`mongoengine.Document`. Holds information for the people collection.
    
    :property name: name of the person (type: :class:`mongoengine.fields.StringField`)
    :property email: email of the person (type: :class:`mongoengine.fields.StringField`)
    
    .. NOTE:: Unique (or primary key) are the fields: name and email.
    """
    meta = {
        'shard_key': ('email', 'name',)
    }
    
     #PK: email, name
    email = StringField(max_length=150, required=True, unique_with=['name'])
    name = StringField(max_length=150, required=True)
    username = StringField(max_length=300)

    def __hash__(self):
        return hash(self.name+self.email)
    
    
class Project(Document):
    """ Document that inherits from :class:`mongoengine.Document`. Holds information for the project collection.
    
    :property url: url to the project repository (type: :class:`mongoengine.fields.StringField`)
    :property name: name of the project (type: :class:`mongoengine.fields.StringField`)
    :property repositoryType: type of the repository (type: :class:`mongoengine.fields.StringField`)
    
    .. NOTE:: Unique (or primary key) is the field url.
    """
    meta = {
        'indexes': [
            '#url'
        ],
        'shard_key': ('url', ),
    }

    # PK uri
    url = StringField(max_length=400, required=True, unique=True)
    name = StringField(max_length=100, required=True)
    repositoryType = StringField(max_length=15)
    issue_urls = ListField(StringField())
    mailing_urls = ListField(StringField())
    
        

class Commit(Document):
    """ Document that inherits from :class:`mongoengine.Document`. Holds information for the commit collection.
    
    :property projectId: id of the project, which belongs to the file action (type: :class:`mongoengine.fields.ObjectIdField`)
    :property revisionHash: revision hash of the commit (type: :class:`mongoengine.fields.StringField`)
    :property branches: list of branches to which the commit belongs to (type: :class:`mongoengine.fields.ListField(:class:`mongoengine.fields.StringField`)`)
    :property tagIds: list of tag ids, which belong to the commit (type: :class:`mongoengine.fields.ListField(:class:`mongoengine.fields.ObjectIdField`)`)
    :property parents: list of parents of the commit (type: :class:`mongoengine.fields.ListField(:class:`mongoengine.fields.StringField`)`)
    :property authorId: id of the author of the commit (type: :class:`mongoengine.fields.ObjectIdField`)
    :property authorDate: date when the commit was created (type: :class:`mongoengine.fields.DateTimeField`)
    :property authorOffset: offset of the authorDate (type: :class:`mongoengine.fields.IntField`)
    :property committerId: id of the committer of the commit (type: :class:`mongoengine.fields.ObjectIdField`)
    :property committerDate: date when the commit was committed (type: :class:`mongoengine.fields.DateTimeField`)
    :property committerOffset: offset of the committerDate (type: :class:`mongoengine.fields.IntField`)
    :property message: commit message (type: :class:`mongoengine.fields.StringField`)
    :property fileActionIds: list of file action ids, which belong to the commit (type: :class:`mongoengine.fields.ListField(:class:`mongoengine.fields.ObjectIdField`)`)
    
    .. NOTE:: Unique (or primary key) are the fields projectId and revisionHash.
    """

    meta = {
        'indexes': [
            'projectId',
        ],
        'shard_key': ('projectId', 'revisionHash'),
    }

    #PK: projectId and revisionhash
    projectId = ObjectIdField(required=True, unique_with=['revisionHash'] )
    revisionHash = StringField(max_length=50, required=True)
    branches = ListField(StringField(max_length=500))
    tagIds = ListField(ObjectIdField())
    parents = ListField(StringField(max_length=50))
    authorId = ObjectIdField()
    authorDate = DateTimeField()
    authorOffset = IntField()
    committerId = ObjectIdField()
    committerDate = DateTimeField()
    committerOffset = IntField()
    message = StringField()
    fileActionIds = ListField(ObjectIdField())

    
    def __str__(self):
        return ""


class TestState(Document):
    """ Document that inherits from :class:`mongoengine.Document`. Holds information for the test_state collection.

    :property file_id: id of the test, that we analyzed (type: :class:`mongoengine.fields.ObjectIdField`)
    :property commit_id: id of the commit, we analyzed (type: :class:`mongoengine.fields.ObjectIdField`)
    :property long_name: name of the file (type: :class:`mongoengine.fields.StringField`)
    :property file_type: type of the file (type: :class:`mongoengine.fields.StringField`)
    :property depends_on: file ids of dependencies of the test (recursive) (type: :class:`mongoengine.fields.ListField(:class:`mongoengine.fields.ObjectIdField`))
    :property direct_imp: file ids of direct dependencies of the test (type: :class:`mongoengine.fields.ListField(:class:`mongoengine.fields.ObjectIdField`))
    :property mock_cut_dep: file ids of the mock_cutoff_dependencies (type: :class:`mongoengine.fields.ListField(:class:`mongoengine.fields.ObjectIdField`))
    :property mocked_modules: file ids of the mocked modules (type: :class:`mongoengine.fields.ListField(:class:`mongoengine.fields.ObjectIdField`))
    :property uses_mock: is true, if the file at this commit uses mocks (type: :class:`mongoengine.fields.BooleanField`)
    :property error: is true if there was an error with mining this file at this commit (type: :class:`mongoengine.fields.BooleanField`)

    .. NOTE:: Unique (or primary key) are the fields: file_id, commit_id, and long_name.
    """
    meta = {
        'indexes': [
            'commit_id',
        ],
        'shard_key': ('file_id', 'commit_id', 'long_name'),
    }

    file_id = ObjectIdField(required=True,unique_with=['commit_id', 'long_name'])
    commit_id = ObjectIdField(required=True)
    long_name = StringField(required=True)
    file_type = StringField()
    depends_on = ListField(ObjectIdField())
    direct_imp = ListField(ObjectIdField())
    mock_cut_dep = ListField(ObjectIdField())
    mocked_modules = ListField(ObjectIdField())
    uses_mock = BooleanField()
    error = BooleanField()


class Issue(Document):
    meta = {
        'indexes': [
            'system_id',
            'project_id'
        ],
        'shard_key': ('system_id', 'project_id'),
    }

    system_id = StringField(unique_with=['project_id'])
    project_id = ObjectIdField()
    title = StringField()
    desc = StringField()
    created_at = DateTimeField()
    updated_at = DateTimeField()
    creator_id = ObjectIdField()
    reporter_id = ObjectIdField()

    issue_type = StringField()
    priority = StringField()
    status = StringField()
    affects_versions = ListField(StringField())
    components = ListField(StringField())
    labels = ListField(StringField())
    resolution = StringField()
    fix_versions = ListField(StringField())
    assignee = ObjectIdField()
    issue_links = ListField(DictField())
    original_time_estimate=IntField()
    environment=StringField()

    def __str__(self):
        return "System_id: %s, project_id: %s, title: %s, desc: %s, created_at: %s, updated_at: %s, issue_type: %s," \
               " priority: %s, affects_versions: %s, components: %s, labels: %s, resolution: %s, fix_versions: %s," \
               "assignee: %s, issue_links: %s, status: %s, time_estimate: %s, environment: %s, creator: %s, " \
               "reporter: %s" % (
            self.system_id, self.project_id, self.title, self.desc, self.created_at, self.updated_at, self.issue_type,
            self.priority, ','.join(self.affects_versions), ','.join(self.components), ','.join(self.labels),
            self.resolution, ','.join(self.fix_versions), self.assignee, str(self.issue_links), self.status,
            str(self.original_time_estimate), self.environment, self.creator_id, self.reporter_id
        )


class Event(Document):
    STATI = (
        ('created', 'The issue was created by the actor.'),
        ('closed','The issue was closed by the actor. When the commit_id is present, it identifies the commit '
                  'that closed the issue using "closes / fixes #NN" syntax.'),
        ('reopened', 'The issue was reopened by the actor.'),
        ('subscribed', 'The actor subscribed to receive notifications for an issue.'),
        ('merged','The issue was merged by the actor. The `commit_id` attribute is the SHA1 of the HEAD '
                  'commit that was merged.'),
        ('referenced', 'The issue was referenced from a commit message. The `commit_id` attribute is the '
                       'commit SHA1 of where that happened.'),
        ('mentioned', 'The actor was @mentioned in an issue body.'),
        ('assigned', 'The issue was assigned to the actor.'),
        ('unassigned', 'The actor was unassigned from the issue.'),
        ('labeled', 'A label was added to the issue.'),
        ('unlabeled', 'A label was removed from the issue.'),
        ('milestoned', 'The issue was added to a milestone.'),
        ('demilestoned', 'The issue was removed from a milestone.'),
        ('renamed', 'The issue title was changed.'),
        ('locked', 'The issue was locked by the actor.'),
        ('unlocked','The issue was unlocked by the actor.'),
        ('head_ref_deleted', 'The pull requests branch was deleted.'),
        ('head_ref_restored', 'The pull requests branch was restored.'),
        ('description', 'The description was changed.'),
        ('priority', 'The issue was added to a milestone.'),
        ('status', 'The status was changed.'),
        ('resolution', 'The resolution was changed.'),
        ('issuetype','The issuetype was changed.'),
        ('environment', 'The environment was changed.'),
        ('timeoriginalestimate', 'The original time estimation for fixing the issue was changed.'),
        ('version', 'The affected versions was changed.'),
        ('component', 'The component list was changed.'),
        ('labels', 'The labels of the issue were changed.'),
        ('fix version', 'The fix versions of the issue were changed.'),
        ('link', 'Issuelinks were added or deleted.'),
        ('attachment','The attachments of the issue were changed.'),
        ('release note', 'A release note was changed.'),
        ('remoteissuelink', 'A remote link was added to the issue.'),
        ('comment', 'A comment was deleted or added to the issue.'),
        ('hadoop flags', 'Hadoop flags were change to the issue.'),
        ('timeestimate', 'Time estimation was changed in the issue.'),
        ('tags', 'Tags of the issue were changed.')
    )

    meta = {
        'indexes': [
            'issue_id',
            '#system_id',
            ('issue_id', '-created_at')
        ],
        'shard_key': ('system_id',),
    }

    system_id = StringField(unique=True)
    issue_id = ObjectIdField()
    created_at = DateTimeField()
    status = StringField(max_length=50, choices=STATI)
    author_id = ObjectIdField()

    old_value = StringField()
    new_value = StringField()

    def __str__(self):
        return "system_id: %s, issue_id: %s, created_at: %s, status: %s, author_id: %s, " \
               "old_value: %s, new_value: %s" % (
                    self.system_id,
                    self.issue_id,
                    self.created_at,
                    self.status,
                    self.author_id,
                    self.old_value,
                    self.new_value
               )


class IssueComment(Document):
    meta = {
        'indexes': [
            'issue_id',
            '#system_id',
            ('issue_id', '-created_at')
        ],
        'shard_key': ('system_id',),
    }

    system_id = IntField(unique=True)
    issue_id = ObjectIdField()
    created_at = DateTimeField()
    author_id = ObjectIdField()
    comment = StringField()

    def __str__(self):
        return "system_id: %s, issue_id: %s, created_at: %s, author_id: %s, comment: %s" % (
            self.system_id, self.issue_id, self.created_at, self.author_id, self.comment
        )

class Import(Document):
    """Document that inherits from :class:`mongoengine.Document`.
    Holds information for the imports of a specific file.
    :property commitId: id of the project, which belongs to the file action (type: :class:`mongoengine.fields.ObjectIdField`)
    :property fileId: id of the file, which belongs to the file action (type: :class:`mongoengine.fields.ObjectIdField`)
    :property name: name of the import (type: :class:`mongoengine.fields.ListField(:class:`mongoengine.fields.StringField`)`)
    """

    meta = {
        'indexes': [
            'commitId',
            'fileId'
        ],
        'shard_key': ('commitId', 'fileId'),
    }

    # PK: commitId and fileId
    commitId = ObjectIdField(required=True, unique_with=['fileId'])
    fileId = ObjectIdField(required=True, unique_with=['commitId'])
    imports = ListField(StringField(max_length=300))


class NodeTypeCount(Document):
    """Document that inherits from :class:`mongoengine.Document`.
    Contains AST Node Types for Python.
    :property commitId: id of the commit, which belongs to the file action (type: :class:`mongoengine.fields.ObjectIdField`)
    :property fileId: id of the file, which belongs to the file action (type: :class:`mongoengine.fields.ObjectIdField`)
    :property nodeCount: number of AST nodes (type: :class:`mongoengine.fields.IntField`)
    :property nodeTypeCounts: AST nodes and their respective counts for this file (type: :class:`mongoengine.fields.DictField`)
    """

    meta = {
        'indexes': [
            'commitId',
            'fileId'
        ],
        'shard_key': ('commitId', 'fileId'),
    }

    # PK: commitId and fileId
    commitId = ObjectIdField(required=True, unique_with=['fileId'])
    fileId = ObjectIdField(required=True, unique_with=['commitId'])
    nodeCount = IntField()  # full number of nodes
    nodeTypeCounts = DictField() # every node with its number for this file