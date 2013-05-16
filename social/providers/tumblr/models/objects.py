from django.db import models as m

from utils.fields import DefaultTextField


class User(m.Model):
    name = m.TextField(primary_key=True)

    def __unicode__(self):
        return self.name or unicode(self.id)

    class Meta:
        app_label = 'tumblr'

    def avatar(self, size=64):
        try:
            blog = self.blogs.all()[0].name
        except Blog.DoesNotExist:
            return 'http://assets.tumblr.com/images/default_avatar_%s.gif' % size
        return 'http://api.tumblr.com/v2/blog/%s.tumblr.com/avatar/%s' % (blog,
                size)


class Blog(m.Model):
    title = DefaultTextField()
    name = m.TextField(primary_key=True)
    url = DefaultTextField()
    description = DefaultTextField()
    ask = m.BooleanField(default=False)
    ask_anon = m.BooleanField(default=False)

    users = m.ManyToManyField(User, through='Writer', related_name='blogs')

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'tumblr'


class Tag(m.Model):
    name = m.TextField(primary_key=True)

    def __unicode__(self):
        return self.text

    class Meta:
        app_label = 'tumblr'


class Post(m.Model):
    id = m.BigIntegerField(primary_key=True)
    blog = m.ForeignKey(Blog, related_name='posts')
    post_url = DefaultTextField()
    type = DefaultTextField()
    #TODO: convert this
    timestamp = m.IntegerField()
    date = DefaultTextField()
    format = DefaultTextField()
    reblog_key = DefaultTextField()
    source_url = DefaultTextField()
    source_title = DefaultTextField()
    state = DefaultTextField()

    tags = m.ManyToManyField(Tag, related_name='posts')

    def __unicode__(self):
        return '%s %s on %s' % (self.type, self.id, self.blog)

    class Meta:
        app_label = 'tumblr'


class TextPost(Post):
    title = DefaultTextField(null=True)
    body = DefaultTextField()

    def __unicode__(self):
        return '%s on %s' % (self.title or self.id, self.blog)

    class Meta:
        app_label = 'tumblr'


class PhotoPost(Post):
    title = DefaultTextField(null=True)
    body = DefaultTextField()

    def __unicode__(self):
        return '%s on %s' % (self.title or self.id, self.blog)

    class Meta:
        app_label = 'tumblr'


class Photo(m.Model):
    post = m.ForeignKey(PhotoPost, related_name='photos')
    caption = DefaultTextField()

    def __unicode__(self):
        return '%s on %s' % (self.caption or 'photo', self.blog)

    class Meta:
        app_label = 'tumblr'


class PhotoSize(m.Model):
    photo = m.ForeignKey(Photo, related_name='sizes')
    url = m.TextField(primary_key=True)
    width = m.IntegerField()
    height = m.IntegerField()

    def __unicode__(self):
        return '%s %sx%s' % (unicode(self.photo), self.width, self.height)

    class Meta:
        app_label = 'tumblr'

