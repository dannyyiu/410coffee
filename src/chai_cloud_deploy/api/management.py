from django.db.models import signals
from django.contrib.auth.models import Group, Permission
import models

def create_user_groups(app, created_models, verbosity, **kwargs):
    api_group_permissions = {
        "Customer": [
            "add_customer",
            "change_customer",
            "delete_customer",
            "add_order",
            "add_orderdetail"
        ],
        "Store": [
            "add_inventory",
            "change_inventory",
            "delete_inventory",
            "change_order",
        ],
    }

    if verbosity > 0:
        print "Starting post_syncdb custom scripts..."
    for group in api_group_permissions:
        role, created = Group.objects.get_or_create(name=group)
        if verbosity > 1 and created:
            print 'Creating group', group
        for perm in api_group_permissions[group]:
            role.permissions.add(Permission.objects.get(codename=perm))
            if verbosity > 1:
                print "Permitting", group, 'to', perm
        role.save()

signals.post_syncdb.connect(
    create_user_groups,
    sender=models, # run only when models are created
    dispatch_uid = 'api.models.create_user_groups'
    )