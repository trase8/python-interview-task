import abc
import json
import string
from collections import defaultdict
from datetime import datetime
from random import choice
from typing import List


class PostsStorage:
    # Singleton pattern is better
    data = {}


storage = PostsStorage()


# Interfaces below
class IPost:
    def format(self):
        ...


class ISocialNetworkProvider:
    @abc.abstractmethod
    def post(self, post: IPost):
        ...

    @abc.abstractmethod
    def get_posts(self) -> List[IPost]:
        ...


# Abstract classes below
class Post(abc.ABC, IPost):
    title: str
    message: str

    def __init__(self, title, message, **kwargs) -> None:
        super().__init__()
        self.title = title
        self.message = message

    @abc.abstractmethod
    def format(self):
        raise NotImplementedError


class SocialNetworkProvider(abc.ABC, ISocialNetworkProvider):
    name: str
    post_model: IPost

    @abc.abstractmethod
    def post(self, post: IPost):
        if self.name not in storage.data:
            storage.data.update(
                {
                    self.name: list(),
                }
            )
        return storage.data[self.name].append(post.format())

    @abc.abstractmethod
    def get_posts(self):
        return storage.data[self.name]


# Concrete classes below
class TwitterPost(Post):
    reply_to_post_id = 0

    def format(self):
        # maybe validate data before sending?
        # maybe wait fot some exceptions?
        return json.dumps(
            {
                'title': self.title,
                'message': self.message,
                'reply_to': self.reply_to_post_id,
                'time': str(datetime.now().timestamp()),
            }
        )


class InstagramPost(Post):
    image: str

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.image = ''.join(
            choice(
                string.ascii_uppercase + string.digits
            ) for _ in range(64)
        )

    def format(self):
        return json.dumps(
            {
                'data': {
                    'title': self.title,
                    'message': self.message,
                    'img': self.image,
                    'time': str(datetime.now().timestamp()),
                }
            }
        )


class InstagramProvider(SocialNetworkProvider):
    # use classname or name attribute to identify provider?
    name = 'instagram'
    post_model = InstagramPost

    def post(self, post: IPost):
        return super(InstagramProvider, self).post(post)

    def get_posts(self):
        return super(InstagramProvider, self).get_posts()


class TwitterProvider(SocialNetworkProvider):
    name = 'twitter'
    post_model = TwitterPost

    # @auth_decorator is an idea
    def post(self, post: IPost):
        return super(TwitterProvider, self).post(post)

    def get_posts(self):
        return super(TwitterProvider, self).get_posts()


# Facet pattern
class CommunicationWrapper:
    """
    Description of how to use this class
    """

    def __init__(self, providers) -> None:
        super().__init__()
        self.providers = providers

    @staticmethod
    def _merge_posts(a, b):
        # Need to merge 2 sorted arrays into one sorted array
        # Input: 2 sorted (ascending) arrays A and B of length M and N
        # Output: A sorted (ascending) array consisting of the elements of the first two
        # Input [1, 2, 5], [1, 2, 3, 4, 6]
        # Output [1, 1, 2, 2, 3, 4, 5, 6]

        # Time: O(n)
        # Memory: O(n)
        # n - max(N, M)

        numbers_map = defaultdict(int)

        if len(a) > len(b):
            first_list = a
            second_list = b
        else:
            first_list = b
            second_list = a

        for i in range(len(first_list)):
            numbers_map[first_list[i]] += 1
            if i < len(second_list):
                numbers_map[second_list[i]] += 1

        return list(numbers_map)

    def add_post(self, provider_name, title, message, **kwargs):
        try:
            provider_class = next(
                provider for provider in self.providers
                if provider_name == provider.name
            )
        except StopIteration:
            # Better exception class needed
            raise TypeError(f'provider_name not found')

        provider = provider_class()
        new_post_model = provider.post_model(
            title=title,
            message=message,
            **kwargs,
        )
        provider.post(post=new_post_model)

    def get_all_posts(self) -> List[IPost]:
        # get all posts
        all_posts = {}
        for provider_class in self.providers:
            provider = provider_class()
            provider_posts = provider.get_posts()
            all_posts.update(
                {
                    provider.name: provider_posts
                }
            )

        # sort this 2 providers. How to sort if there are 3+ providers?
        all_posts_flat = self._merge_posts(
            all_posts[TwitterProvider.name],
            all_posts[InstagramProvider.name],
        )

        return all_posts_flat
