# Task description
Imagine you are developing a social networks wrapper to post some media in different social networks in a **single** window and post format.
Each social network expects posts in its own unique format. There are 2 integrations In our MVP: Twitter and Instagram. In future releases we are planning to add 5 more networks. 

### Twitter
Twitter expects post in JSON format with required fields: 
- title
- message
- current time
- other tweet ID to reply to (optional)

### Instagram
Instagram expects post in JSON format with required tags:
- title
- message
- current time in a timestamp format
- image (optional)

You can store posts in-memory to emulate social networks backends. Each social network must store data in a place isolated from others.

# User stories

#### Creating new posts. Example:
```python
wrapper.add_post(
    provider_name='twitter',
    title='I am Mask',
    message='Ban Joseph Robinette Biden!',
)
```

#### Retrieve all messages from all networks, merged and sorted by the order in which they were added. Example:
```python
wrapper.get_all_posts()

> First Instagram post
> First tweet
> Second tweet
> ...
```