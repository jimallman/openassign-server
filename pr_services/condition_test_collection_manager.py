from pr_services.object_manager import ObjectManager
from pr_services.rpc.service import service_method
import facade

class ConditionTestCollectionManager(ObjectManager):
    """
    Manage ConditionTestCollections
    """
    GETTERS = {
        'condition_tests': 'get_many_to_many',
        'name': 'get_general',
    }
    SETTERS = {
        'name': 'set_general',
    }
    def __init__(self):

        ObjectManager.__init__(self)
        self.my_django_model = facade.models.ConditionTestCollection

    @service_method
    def create(self, auth_token, name):
        """
        Create a new ConditionTestCollection

        @param name     Human readable name
        """

        blame = facade.managers.BlameManager().create(auth_token)

        new_collection = self.my_django_model.objects.create(name=name)

        self.authorizer.check_create_permissions(auth_token, new_collection)
        return new_collection

