from django.db import models as m

from .objects import User, Blog, Tag, Post

class Writer(m.Model):
    user = m.ForeignKey(User, related_name='writes')
    blog = m.ForeignKey(Blog, related_name='writers')
    primary = m.BooleanField(default=False)

    class Meta:
        app_label = 'tumblr'
        unique_together = [('user', 'blog')]

    def __unicode__(self):
        return '%s for %s' (unicode(self.user), unicode(self.blog))

class Like(m.Model):
    user = m.ForeignKey(User, related_name='likes')
    post = m.ForeignKey(Post, related_name='likes')

    class Meta:
        app_label = 'tumblr'

    def __unicode__(self):
        return '%s likes %s' % (unicode(self.user), unicode(self.post))

class TagUse(m.Model):
    tag = m.ForeignKey(Tag, related_name='uses')

    class Meta:
        app_label = 'tumblr'

    def __unicode__(self):
        return '%s uses %s' % (unicode(self.user), unicode(self.tag))

class Reblog(m.Model):
    user = m.ForeignKey(User, related_name='reblogs')
    post = m.ForeignKey(Post, related_name='reblogs')

    class Meta:
        app_label = 'tumblr'

    def __unicode__(self):
        return '%s reblogs %s' % (unicode(self.user), unicode(self.post))

