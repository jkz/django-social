from django.db import models as m

from .objects import User, Blog, Tag, Post

class Writer(m.Model):
    user = m.ForeignKey(User, related_name='writes')
    blog = m.ForeignKey(Blog, related_name='writers')
    primary = m.BooleanField(default=False)

    class Meta:
        app_label = 'tumblr'
        unique_together = [('user', 'blog')]

    def __str__(self):
        return '{} for {}'.format(self.user, self.blog)

class Like(m.Model):
    user = m.ForeignKey(User, related_name='likes')
    post = m.ForeignKey(Post, related_name='likes')

    class Meta:
        app_label = 'tumblr'

    def __str__(self):
        return '{} likes {}'.format(self.user, self.post)

class TagUse(m.Model):
    tag = m.ForeignKey(Tag, related_name='uses')

    class Meta:
        app_label = 'tumblr'

    def __str__(self):
        return '{} uses {}'.format(self.user, self.tag)

class Reblog(m.Model):
    user = m.ForeignKey(User, related_name='reblogs')
    post = m.ForeignKey(Post, related_name='reblogs')

    class Meta:
        app_label = 'tumblr'

    def __str__(self):
        return '{} reblogs {}'.format(self.user, self.post)

