class Permission:
    USER_READ = "user.read"
    USER_CREATE = "user.create"
    USER_UPDATE = "user.update"
    USER_DELETE = "user.delete"

    ROLE_READ = "role.read"
    ROLE_CREATE = "role.create"
    ROLE_UPDATE = "role.update"
    ROLE_DELETE = "role.delete"

    PERMISSION_READ = "permission.read"

    ADMIN_ALL = "admin.all"


DEFAULT_PERMISSIONS = [
    Permission.USER_READ,
    Permission.USER_CREATE,
    Permission.USER_UPDATE,
    Permission.USER_DELETE,
    Permission.ROLE_READ,
    Permission.ROLE_CREATE,
    Permission.ROLE_UPDATE,
    Permission.ROLE_DELETE,
    Permission.PERMISSION_READ,
    Permission.ADMIN_ALL,
]


DEFAULT_ADMIN_ROLE = {
    "role_name": "Admin",
    "description": "Full tenant administrator access.",
    "permissions": DEFAULT_PERMISSIONS,
    "is_system_role": True,
}


DEFAULT_MARKETING_ROLE = {
    "role_name": "Marketing Manager",
    "description": "Marketing and campaign access.",
    "permissions": [
        Permission.USER_READ,
    ],
    "is_system_role": True,
}