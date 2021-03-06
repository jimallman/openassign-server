"""
SessionTemplateResourceTypeRequirementManager class
"""

from pr_services.object_manager import ObjectManager
from pr_services.rpc.service import service_method
import facade

class SessionTemplateResourceTypeRequirementManager(ObjectManager):
    """
    Manage SessionTemplateResourceTypeRequirements in the Power Reg system
    """

    GETTERS = {
        'max': 'get_general',
        'min': 'get_general',
        'notes': 'get_many_to_many',
        'resource_type': 'get_foreign_key',
        'session_template': 'get_foreign_key',
    }
    SETTERS = {
        'max': 'set_general',
        'min': 'set_general',
        'notes': 'set_many',
        'resource_type': 'set_foreign_key',
        'session_template': 'set_foreign_key',
    }
    def __init__(self):
        """ constructor """

        ObjectManager.__init__(self)
        self.my_django_model = facade.models.SessionTemplateResourceTypeReq

    @service_method
    def create(self, auth_token, session_template_id, resource_type_id, min, max):
        """
        Create a new SessionTemplateResourceTypeRequirement

        @param session_template_id  Foreign key for an session_template
        @param resource_type_id     Foreign key for an resource_type
        @param min                  Minimum number required
        @param max                  Maximum number allowed
        @return                     A reference to the newly created SessionTemplateResourceTypeRequirement
        """

        session_template_instance = self._find_by_id(session_template_id, facade.models.SessionTemplate)
        resource_type_instance = self._find_by_id(resource_type_id, facade.models.ResourceType)
        c = self.my_django_model(session_template = session_template_instance,
                resource_type=resource_type_instance, min=min, max=max)
        c.save()
        self.authorizer.check_create_permissions(auth_token, c)
        return c

# vim:tabstop=4 shiftwidth=4 expandtab
