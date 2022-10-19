# Solution and insides
Create base classes and interfaces for posts and social network providers. Create concrete classes. Make a simple storage.
Then create a facet or wrapper which will wrap user stories to methods and hide working with created classes behind the back. Double think of merging and sorting posts from different networks.

### Notes
1) Splitting files into models and "client code" (main.py) speaks of accuracy and structure.
2) Adding abstract classes and interfaces helps with extensibility and allows you to clearly separate one from the other so that posts can be developed by one team, and providers by another.
3) Using type hints is a good practice. Linters may help you find logical mistakes. Other developers may understand code easily.
4) Finding a specific provider by its name can be done with a simple generator or through a factory.
5) Since python version 3.6 the dictionary holds keys as they are inserted. The order is observed according to the insert. This is why method **_merge_posts** works good.
