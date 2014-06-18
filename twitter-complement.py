from twitter import *
import time

CONSUMER_KEY = ''
CONSUMER_SECRET = ''

MY_TWITTER_CREDS = os.path.expanduser('~/.my_app_credentials')

if not os.path.exists(MY_TWITTER_CREDS):
    oauth_dance("Complement", CONSUMER_KEY, CONSUMER_SECRET,
                MY_TWITTER_CREDS)

oauth_token, oauth_secret = read_token_file(MY_TWITTER_CREDS)

t = Twitter(auth=OAuth(
    oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET))

# get lists
lists = t.lists.list()

# find all users across lists
list_users = []
for lst in lists:
    # if complement list already exits delete it
    if lst['name'] == 'Complement':
        try:
            t.lists.destroy(list_id=lst['id'])
        except:
            t.lists.destroy(slug=lst['slug'], owner_screen_name=lst['user']['screen_name'])
        pass
    check = True
    cursor = -1
    while check:        
        listmembers = t.lists.members(slug=lst['slug'], owner_screen_name='zubinjelveh', skip_status=True, cursor=cursor)
        for user in listmembers['users']:
            list_users.append(user['screen_name'])
        cursor = listmembers['next_cursor']
        if not cursor:
            break

list_users = set(list_users)

# get all followed users
following = []
cursor = -1
while True:    
    follow = t.friends.list(cursor=cursor)
    cursor = follow['next_cursor']
    for friends in follow['users']:
        following.append(friends['screen_name'])
    if not cursor:
        break

following = set(following)

# find users who are followed but not in a list
complement = list(following.difference(list_users))

# create complement list
comp = t.lists.create(name='Complement', mode='private', description='Everyone else not in a list.')

# add users to complement list
factor = int(len(complement)/20) + 1
add_list = []
for i in range(factor):
    add_list.append(complement[i * 20 : (i+1) * 20 ])

for comp_list in add_list:
    print len(add_list) - i
    temp = t.lists.members.create_all(list_id=comp['id'], screen_name=','.join(comp_list))
    time.sleep(2)
