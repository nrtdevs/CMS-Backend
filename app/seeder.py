from app.extensions import db
from app.models import Permission, Role, User
from werkzeug.security import generate_password_hash

permissions = [
    {
        "name": "read",
        "permission_group": "Dashboard",
        "description": "Permission to read the dashboard",
    },
    {
        "name": "create",
        "permission_group": "User",
        "description": "Permission to create  users",
    },
    {
        "name": "read",
        "permission_group": "User",
        "description": "Permission to view  users",
    },
    {
        "name": "update",
        "permission_group": "User",
        "description": "Permission to update  users",
    },
    {
        "name": "delete",
        "permission_group": "User",
        "description": "Permission to delete  users",
    },
    {
        "name": "block",
        "permission_group": "User",
        "description": "Permission to block  users",
    },
    {
        "name": "create",
        "permission_group": "Bidding",
        "description": "Permission to create  bidding",
    },
    {
        "name": "read",
        "permission_group": "Bidding",
        "description": "Permission to view  bidding",
    },
    {
        "name": "update",
        "permission_group": "Bidding",
        "description": "Permission to update  bidding",
    },
    {
        "name": "delete",
        "permission_group": "Bidding",
        "description": "Permission to delete  bidding",
    },
    {
        "name": "approve",
        "permission_group": "Bidding",
        "description": "Permission to approve  bidding",
    },
]


def seed_permissions():
    """Seed the Permission table with initial data."""
    for perm in permissions:
        existing_perm = Permission.query.filter_by(
            name=perm["name"], permission_group=perm["permission_group"]
        ).first()
        if existing_perm:
            print(f"Permission '{perm['name']}' already exists.")
        else:
            new_permission = Permission(
                name=perm["name"],
                permission_group=perm["permission_group"],
                description=perm["description"],
            )
            db.session.add(new_permission)
    db.session.commit()
    print("Permission table seeded successfully!")


def seed_roles():
    """Seed the Role table with initial data."""
    roles = [
        {
            "name": "Master Admin",
            "userType": "master_admin",
            "description": "Administrator with full access",
        },
        {
            "name": "Super Admin",
            "userType": "super_admin",
            "description": "Administrator with full access",
        },
    ]
    all_permissions = Permission.query.all()

    for role_data in roles:
        existing_role = Role.query.filter_by(name=role_data["name"]).first()
        if existing_role:
            print(f"Role '{role_data['name']}' already exists.")
        else:
            # Create new role
            new_role = Role(
                name=role_data["name"],
                userType=role_data["userType"],
                description=role_data["description"],
            )

            # Assign all permissions to the role
            new_role.permissions.extend(all_permissions)

            db.session.add(new_role)
    db.session.commit()
    print("Role table seeded successfully!")


def seed_users():
    """Seed the User table with initial data."""
    master = User.query.filter_by(userType="master_admin").first()
    if master:
        print("Master Admin Already Exists")
        return
    Hashed_Password = generate_password_hash("admin@2025")
    users = [
        User(
            firstName="Master",
            lastName="Admin",
            countryCode="+91",
            mobileNo=7987809375,
            email="nrt@gmail.com",
            password=Hashed_Password,
            userType="master_admin",
            empID="NRT-89",
            role_id=1,
        ),
    ]

    db.session.bulk_save_objects(users)
    db.session.commit()
    print("User table seeded successfully!")
