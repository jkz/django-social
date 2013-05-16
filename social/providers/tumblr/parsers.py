from django.dispatch import Signal

import sociallib.tumblr as tumblr

from . import models as m

data_signal = Signal(providing_args=['data'])

def update_data(obj, data):
    for key in set(data) & set(obj.__dict__):
        setattr(obj, key, data[key])

def import_blog(data):
    blog, created = m.Blog.objects.get_or_create(name=data['name'])
    update_data(blog, data)
    blog.save()
    return blog

def import_user(data):
    user, created = m.User.objects.get_or_create(name=data['name'])
    for entry in data.pop('blogs', []):
        blog = import_blog(entry)
        writer, created  = user.writes.get_or_create(blog=blog)
        #XXX This feels bad
        primary = data.pop('primary', False)
        if primary:
            user.writes.update(primary=False)
            writer.primary = True
            writer.save()
    update_data(user, data)
    user.save()
    return user

def import_tag(name):
    tag, created = m.Tag.objects.get_or_create(name=name)
    return tag

def _import_text_post(data):
    post = m.TextPost()
    update_data(post, data)
    return post

def _import_photo_post(data):
    post = m.PhotoPost()
    update_data(post, data)
    return post

def _import_post(data):
    post = m.Post()
    update_data(post, data)
    return post

def import_post(data):
    blog = import_blog({'name': data.pop('blog', data.pop('blog_name'))})
    tags = [import_tag(tag) for tag in data.pop('tags')]
    type = data.get('type')
    if type == 'text':
        post = _import_text_post(data)
    elif type == 'photo':
        post = _import_photo_post(data)
    else:
        post = _import_post(data)
    post.blog = blog
    post.save()
    for tag in tags:
        post.tags.add(tag)
    return post

def import_data(data, with_meta=True):
    if with_meta:
        if data['meta']['status'] != 200:
            raise tumblr.Error(data['meta']['msg'])
        data = data['response']

    if isinstance(data, list):
        for d in data:
            import_data(d, False)
        return
    if 'blog' in data:
        import_blog(data['blog'])
    if 'user' in data:
        import_user(data['user'])
    if 'blog_name' in data or 'id' in data:
        import_post(data)
    for user in data.get('users', []):
        import_user(user)
    for post in data.get('posts', []):
        import_post(post)


