from facepy import GraphAPI


class User(object):
    """Instances of the User class represent Facebook test users."""

    def __init__(self, id, access_token, login_url, email, password):
        """
        Initialize a Facebook test user.

        :param id: A string describing the user's Facebook ID.
        :param access_token: A string describing the user's access token.
        :param login_url: A string describing the user's login URL.
        :param email: A string describing the user's email.
        :param password: A string describing the user's password.
        """
        self.id = id
        self.access_token = access_token
        self.login_url = login_url
        self.email = email
        self.password = password

        self.graph = GraphAPI(access_token)

    @classmethod
    def create(self, application_id, access_token, **parameters):
        """
        Create a new Facebook test user.

        :param application_id: A string describing the Facebook application ID.
        :param access_token: A string describing the application's access token.
        :param name: An optional string describing the user's name (defaults to a generated name).
        :param permissions: An optional list describing permissions.
        :param locale: An optional string describing the user's locale (defaults to ``en_US``).
        :param installed: A boolean describing whether the user has installed your application (defaults to ``True``).
        """
        return User(**GraphAPI(access_token).post('%s/accounts/test-users' % application_id, **parameters))

    def delete(self):
        """
        Delete the test user.
        """
        self.graph.delete(self.id)

    def befriend(self, other):
        """
        Befriend other user.

        :param other: Another test User
        """
        r = self.graph.get('me/friends/%s' % other.id)
        if 'data' in r and r['data'] and r['data'][0]['id'] == other.id:
            # already friends
            return

        self.graph.post('%s/friends/%s' % (self.id, other.id))
        other.graph.post('%s/friends/%s' % (other.id, self.id))

    @classmethod
    def users(self, application_id, access_token, **parameters):
        """
        Get existing test users.
        """
        r = GraphAPI(access_token).get('%s/accounts/test-users' % application_id, **parameters)
        for u in r['data']:
            yield User(u['id'], u['access_token'], u['login_url'], None, None)

    @property
    def me(self):
        """
        Get user information.
        """
        return self.graph.get('me')

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.delete()
