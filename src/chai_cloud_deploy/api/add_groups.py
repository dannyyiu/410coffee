from django.db.models import signals
from django.contrib.auth.models import Group, Permission
import models

if __name__ == '__main__':
    api_group_permissions = {
        "Customer": [
            "Can add customer",
            "Can change customer",
            "Can delete customer",
            "Can add order",
            "Can add orderdetail"
        ],
        "Store": [
            "Can add inventory",
            "Can change inventory",
            "Can delete inventory",
            "Can change order",
        ],
    }

    for group in api_group_permissions:
        role, created = Group.objects.get_or_create(name=group)
        if created:
            print 'Creating group', group
        for perm in api_group_permissions[group]:
            print "ASDF::::",perm
            role.permissions.add(Permission.objects.get(codename=perm))
            print "Permitting", group, 'to', perm
        role.save()