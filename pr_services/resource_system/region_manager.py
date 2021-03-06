"""
Region manager class
"""

from pr_services.object_manager import ObjectManager
from pr_services.rpc.service import service_method
import facade

class RegionManager(ObjectManager):
    """
    Manage Regions in the Power Reg system
    """
    SETTERS = {
        'events': 'set_many',
        'name': 'set_general',
        'notes': 'set_many',
        'venues': 'set_many',
    }
    GETTERS = {
        'events': 'get_many_to_one',
        'name': 'get_general',
        'notes': 'get_many_to_many',
        'venues': 'get_many_to_one',
    }
    def __init__(self):
        """ constructor """

        ObjectManager.__init__(self)
        self.my_django_model = facade.models.Region

    @service_method
    def create(self, auth_token, name, optional_attributes=None):
        """
        Create a new Region

        @param name                name of the Region
        @return                    a reference to the newly created Region
        """

        r = self.my_django_model(name=name)
        if optional_attributes:
            facade.subsystems.Setter(auth_token, self, r, optional_attributes)
        r.save()
        self.authorizer.check_create_permissions(auth_token, r)
        return r

# vim:tabstop=4 shiftwidth=4 expandtab
