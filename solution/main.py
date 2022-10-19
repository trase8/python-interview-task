from models import CommunicationWrapper
from models import InstagramProvider
from models import TwitterProvider


wrapper = CommunicationWrapper(
    providers=[InstagramProvider, TwitterProvider],
)
wrapper.add_post(
    provider_name=TwitterProvider.name,
    title='1 First tweet',
    message='Hello world!',
)

wrapper.add_post(
    provider_name=InstagramProvider.name,
    title='1 First post in Instagram',
    message='Hello moto!',
)

wrapper.add_post(
    provider_name=TwitterProvider.name,
    title='2 Second tweet! I am Mask',
    message='Ban Joseph Robinette Biden!',
)

wrapper.add_post(
    provider_name=InstagramProvider.name,
    title='2 Second i-post. Ivan Ivanov',
    message='My favourite photographer',
)

wrapper.add_post(
    provider_name=InstagramProvider.name,
    title='3 Third i-post. My cat',
    message='I LOVE my kitty',
)

all_posts = wrapper.get_all_posts()
for post in all_posts:
    print(post)

exit(0)
