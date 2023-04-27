user_roles = {
    'admin': ['admin'],
    'manager': ['manager'],
    'user1': ['user'],
    'user2': ['user'],
}

resource_roles = {
    'add_user': ['admin', 'manager'],
    'delete_user': ['admin', 'manager'],
    'edit_user': ['admin', 'manager'],
    'view_users': ['admin', 'manager'],
    'view_resources': ['admin', 'manager', 'user'],
    'edit_resource': ['admin', 'manager', 'user'],
    'delete_resource': ['admin', 'manager', 'user'],
    'create_resource': ['admin', 'manager', 'user'],
}

def check_access(user, resource):
    if user in user_roles and resource in resource_roles:
        roles = user_roles[user]
        allowed_roles = resource_roles[resource]
        for role in roles:
            if role in allowed_roles:
                return True
    return False

print(check_access('user1', 'create_resource'))