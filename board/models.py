# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TashkentBoard(models.Model):
    id_board = models.AutoField(db_column='ID_BOARD', primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        db_table = 'tashkent_boards'

    def __str__(self):
        return self.name


class TashkentMember(models.Model):
    id_member = models.AutoField(db_column='ID_MEMBER', primary_key=True)
    membername = models.CharField(db_column='memberName', max_length=80)
    dateregistered = models.PositiveIntegerField(db_column='dateRegistered')
    posts = models.PositiveIntegerField()
    realname = models.CharField(db_column='realName', max_length=255)
    emailaddress = models.CharField(db_column='emailAddress', max_length=64)

    class Meta:
        db_table = 'tashkent_members'

    def __str__(self):
        return self.realname


class TashkentMessage(models.Model):
    id_msg = models.AutoField(db_column='ID_MSG', primary_key=True)
    id_topic = models.ForeignKey('TashkentTopic', models.DO_NOTHING, db_column='ID_TOPIC')
    id_board = models.ForeignKey(TashkentBoard, models.DO_NOTHING, db_column='ID_BOARD')
    postertime = models.PositiveIntegerField(db_column='posterTime')
    id_member = models.ForeignKey(TashkentMember, models.DO_NOTHING, db_column='ID_MEMBER')
    id_msg_modified = models.PositiveIntegerField(db_column='ID_MSG_MODIFIED')
    subject = models.TextField()
    postername = models.TextField(db_column='posterName')
    posteremail = models.TextField(db_column='posterEmail')
    modifiedtime = models.PositiveIntegerField(db_column='modifiedTime')
    modifiedname = models.TextField(db_column='modifiedName')
    body = models.TextField()

    class Meta:
        db_table = 'tashkent_messages'

    def __str__(self):
        return "%s:    %s" % (self.id_member, self.subject)


class TashkentTopic(models.Model):
    id_topic = models.AutoField(db_column='ID_TOPIC', primary_key=True)
    id_board = models.ForeignKey(TashkentBoard, models.DO_NOTHING, db_column='ID_BOARD')
    id_first_msg = models.ForeignKey(TashkentMessage, models.DO_NOTHING, db_column='ID_FIRST_MSG', related_name='topics_first')
    id_last_msg = models.ForeignKey(TashkentMessage, models.DO_NOTHING, db_column='ID_LAST_MSG', related_name='topics_last')
    id_member_started = models.ForeignKey(TashkentMember, models.DO_NOTHING, db_column='ID_MEMBER_STARTED', related_name='started_topics')

    class Meta:
        db_table = 'tashkent_topics'

    def __str__(self):
        return self.id_first_msg.subject


class Identifier(models.Model):
    object_type = models.PositiveIntegerField(db_column='type')
    object_id_in_contest = models.PositiveIntegerField(db_column='id_in_contest')
    object_name = models.TextField(db_column='name')

    class Meta:
        db_table = '_identifiers'

    def __str__(self):
        return self.object_name


class User(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    username = models.CharField(max_length=80)
    full_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=80, null=True, blank=True)
    last_name = models.CharField(max_length=80, null=True, blank=True)
    email = models.CharField(max_length=64)
    admission_year = models.PositiveIntegerField()

    class Meta:
        db_table = '_users'

    def __str__(self):
        return self.full_name


class Message(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    parent_msg_id = models.PositiveIntegerField()
    author = models.ForeignKey(User, models.DO_NOTHING, db_column='author')
    text = models.TextField()
    date_created = models.PositiveIntegerField()
    subject = models.TextField()
    topic = models.ForeignKey(TashkentTopic, models.DO_NOTHING, db_column='topic')
    board = models.ForeignKey(TashkentBoard, models.DO_NOTHING, db_column='board')
    identifier = models.ForeignKey(Identifier, models.DO_NOTHING, db_column='identifier', null=True)

    class Meta:
        db_table = '_messages'

    def __str__(self):
        return '%s:    %s' % (self.author, self.subject)
