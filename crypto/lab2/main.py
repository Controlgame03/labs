user_roles = {
    'mark': ['admin'],
    'anton': ['manager'],
    'kostya': ['guest'],
    'denis': ['user'],
    'egor': ['user'],
    'misha': ['admin'],
    'petya': ['manager'],
    'vasya': ['guest'],
    'oleg': ['user'],
    'kirill': ['user'],
    'irina': ['admin'],
    'masha': ['manager'],
    'arina': ['guest'],
    'valya': ['user'],
    'natalya': ['user'],
}

resource_roles = {
    'super_user': ['admin'],
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

#print(resource_roles)
print(user_roles.keys())
print('Welcome!!!')
print('what is your name? ----> ', end=' ')
name = input()

print('what do you want to do? ')
print(resource_roles.keys())
print('action ----> ', end=' ')
action = input()

if check_access(name, action):
    print('fine. you did it')
else:
    print('sorry, but we cannot grant you the right for this action. check the correctness of the data')