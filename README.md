# VK Post Checker

## About the program

I spent an evening and the following morning writing this program. I was experimenting with VK API - there was a need for getting posts from private groups using a token of a person which is a member of that group - me in this particular case.

## How to set up

it's relatively easy. First, you need to go to vkposts.py and insert the id of the group you want to get posts from, then your token.
They explain how to get the token at [VK Developers](https://vk.com/dev/first_guide).

After that you can already launch it, but it's easier to put some arguments, for example:
```
python vkposts.py 3 -1 False
```
Where ```3``` means that it will be checking for new posts every 3 seconds; ```-1``` means that it will be doing it until you manually shut it down; and ```False``` means that it won't be showing you 'there are no new posts' message if so.
