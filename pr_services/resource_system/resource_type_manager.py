"""
ResourceType manager class
"""

from pr_services.object_manager import ObjectManager
from pr_services.rpc.service import service_method
import facade

class ResourceTypeManager(ObjectManager):
    """
    Manage ResourceTypes in the Power Reg system
    """
    SETTERS = {
        'name': 'set_general',
        'notes': 'set_many',
        'resources': 'set_many',
        'sessionresourcetyperequirements': 'set_many',
        'sessiontemplateresourcetypereqs': 'set_many',
    }
    GETTERS = {
        'name': 'get_general',
        'notes': 'get_many_to_many',
        'resources': 'get_many_to_many',
        'sessionresourcetyperequirements': 'get_many_to_one',
        'sessiontemplateresourcetypereqs': 'get_many_to_one',
    }
    def __init__(self):
        """ constructor """

        ObjectManager.__init__(self)
        self.my_django_model = facade.models.ResourceType

    @service_method
    def create(self, auth_token, name):
        """
        Create a new ResourceType

        @param name               name of the ResourceType
        @return                   isntance of ResourceType
        """

        r = self.my_django_model(name=name)
        r.save()
        self.authorizer.check_create_permissions(auth_token, r)
        return r

# vim:tabstop=4 shiftwidth=4 expandtab
