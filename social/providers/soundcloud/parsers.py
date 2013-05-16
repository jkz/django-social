from . import models as m

def import_user(json):
    return m.User.importer.put(**json)

def import_playbacks(track, user, new):
    if new:
        old = track.playbacks.filter(user=user).sum()
        difference = int(new) - old
        if difference:
            track.playbacks.create(user=user, count=difference)

def import_favorite(track, user, is_favorite=True):
    if is_favorite:
        track.favorites.get_or_create(user=user)
    else:
        track.favorites.filter(user=user).delete()

def import_track(json, user=None):
    if 'user' in json:
        json['user'] = import_user(json.pop('user'))
    track = m.Track.importer.put(**json)
    if user:
        if 'user_playback_count' in json:
            import_playbacks(track, user, json.pop('user_playback_count'))
        if 'user_favorite' in json:
            import_favorite(track, user, json.pop('user_favorite'))
    return track


def import_tracks(json, user=None):
    for track in json:
        import_track(track, user)

def import_comment(json, user=None):
    track = import_track(json.pop('track'))
    user = import_user(json.pop('user'))
    return m.Comment.importer.put(**json)

def import_activity(json, user=None):
    typ = json['type']
    origin = json['origin']
    if typ == 'favoriting':
        user = import_user(origin.pop('user'))
        track = import_track(origin.pop('track'))
        return import_favorite(track, user)
    elif typ == 'comment':
        return import_comment(origin, user)
    elif typ == 'track':
        return import_track(origin)
    elif typ == 'track-sharing':
        print 'TRACK-SHARING', origin
        return

def import_activities(json, user=None):
    return [import_activity(activity) for activity in json['collection']]
    return [{'comment': import_comment,
             'track': import_track,
             'favoriting': import_favorite,
             'track-sharing': import_share}.get(
                 activity['type'], lambda *a: None)(activity['origin'])
             for activity in json]
