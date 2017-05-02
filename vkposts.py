# PASSED ARGUMENTS:
# 1: INTERVAL BETWEEN CHECKS (5.0 BY DEFAULT)
# 2: REPEAT X TIMES (-1 BY DEFAULT)
# 3: WHETHER PRINT NO OR JUST SKIP WHEN THERE'S NO NEW POSTS

# import everything we will need
import vk
import re
import threading
import sys
import os

# check if there is a new post every x seconds for n times
# forever if repeat is less than 0
def CheckForNewPosts(vkapi, lastpid=0, interval=5.0, repeat=-1, printno=True):
	# get the latest post and its id
	try:
		post = GetLastPost(vkapi)
		postid = GetPostId(post)
		# check if the new posts id differs from the previous one
		if postid != lastpid:
			# print id, author and text of the post if it is new
			author = GetPostAuthor(vkapi, post)
			print('Post id: {0}\n'
			'Author: {1}\n'
			'-----------\n{2}\n\n'.format(postid, author, GetPostText(post)))
		else:
			# print message if there are no new posts
			if printno:
				print("Ничего... Ждём...\n")
		# introducing nrepeat (repeat - 1) - we don't want it to last forever, do we?
		nrepeat = repeat - 1 if repeat > 0 else repeat
		# setting a timer to call this function again in x seconds for n times
		if repeat != 0:
			threading.Timer(interval, CheckForNewPosts, args=[vkapi, postid, interval, nrepeat, printno]).start()
	# catch some timed out shit and get rid of it. bitch!
	except Exception as exc:
		# yeah... of course... print a beautiful error message... idiot...
		# it's usually timed out, so we'll print this
		print(u'Exception: {0}\n\n'
		u'---------------------------------\n'
		u'-THERE WAS A TIMED OUT EXCEPTION-\n'
		u'-         TRYING AGAIN          -\n'
		u'---------------------------------\n'.format(exc))
		# and call it again, hoping that it ends well
		CheckForNewPosts(vkapi, lastpid, interval, repeat, printno)

# returns the last post
def GetLastPost(vkapi, _owner_id='-<ID>', _offset='0', _count='1'):
	post = vkapi.wall.get(owner_id=_owner_id, offset=_offset, count=_count)
	return post

# returns the id of the specified post
def GetPostId(post):
	return post[1]['id']

# returns authors first and last names
def GetPostAuthor(vkapi, post):
	uid = str(post[1]['from_id'])[1:]
	# use group's name if it was them who posted the message
	if uid == str(post[1]['to_id'])[1:]:
		group = GetGroupById(vkapi, uid)
		return GetGroupName(group)
	# otherwise, use user's full name
	else:
		uid = uid[1:]
		usr = GetUser(vkapi, uid)
		return GetUserFullName(usr)

# returns a user object of a specified id
def GetUser(vkapi, userid):
	return vkapi.users.get(user_ids=[userid])

# returns specified users full name
def GetUserFullName(user):
	return '{0} {1}'.format(user[0]['first_name'], user[0]['last_name'])

# returns a group object of a specified id
def GetGroupById(vkapi, groupid):
	return vkapi.groups.getById(group_id=groupid)

# returns specified groups name
def GetGroupName(group):
	return group[0]['name']

# returns the text of the specified post
def GetPostText(post, pos=1):
	# getting rid of html tags
	raw_text = post[pos]['text']
	# creating two patterns
	nobr_ptrn = re.compile('<br>')  # - for the new line tags
	clean_ptrn = re.compile('<.*?>')  # - and for everything else
	# replacing new line tags with \n character
	nobr_text = re.sub(nobr_ptrn, '\n', raw_text)
	# removing other tags and returning the clean text
	return re.sub(clean_ptrn, '', nobr_text)

# if launched as a program, not as a module
if __name__ == '__main__':
	# set interval, repeat and printno variables
	interval = float(sys.argv[1]) if len(sys.argv) > 1 else 5.0
	repeat = int(sys.argv[2]) if len(sys.argv) > 2 else -1
	printno = sys.argv[3] == 'True' if len(sys.argv) > 3 else True
	# creating a session
	session = vk.Session(access_token='<TOKEN>')
	# assigning that session to vk api
	vkapi = vk.API(session)
	# check for new posts every x seconds
	CheckForNewPosts(vkapi, interval=interval, repeat=repeat, printno=printno)
