from classes.user import User
from classes.forum import Forum
from asyncio import *

# In-memory storage
forums = {}
users = {}

async def admin_retrieve_forum_data():
    forum_dict = {}

    # Loop through each forum in the forums dictionary
    for forum_id, forum in forums.items():
        forum_dict[forum_id] = await forum.to_dict() # Convert the forum object to a dictionary and add it to the result dictionary

    return forum_dict

async def admin_retrieve_author_name(session_token):
    for user_obj in users.values():
        if await user_obj.validate_session_token(session_token):
            return f"{user_obj.first_name} {user_obj.last_name}"
    return None