"""
curriculum manager class
"""

from pr_services.object_manager import ObjectManager
from pr_services.rpc.service import service_method
from pr_services.utils import Utils
import facade

class CurriculumManager(ObjectManager):
    """
    Manage curriculums in the Power Reg system
    """
    GETTERS = {
        'achievements': 'get_many_to_many',
        'curriculum_task_associations': 'get_many_to_one',
        'name': 'get_general',
        'organization': 'get_foreign_key',
        'tasks': 'get_many_to_many',
    }
    SETTERS = {
        'achievements': 'set_many',
        'name': 'set_general',
        'organization': 'set_foreign_key',
        'tasks': 'set_many',
    }
    def __init__(self):
        """ constructor """

        ObjectManager.__init__(self)

        self.my_django_model = facade.models.Curriculum

    @service_method
    def create(self, auth_token, name, organization=None):
        """
        Create a new curriculum.

        :param  name:           human-readable name
        :param  organization:   organization to which this belongs
        :return:                a reference to the newly created curriculum
        """

        c = self.my_django_model(name=name)
        if organization is not None:
            c.organization = self._find_by_id(organization, facade.models.Organization)
        c.save()
        self.authorizer.check_create_permissions(auth_token, c)
        return c

    @service_method
    def admin_curriculums_view(self, auth_token):
        ret = self.get_filtered(auth_token, {}, ['name', 'curriculum_task_associations', 'achievements', 'organization'])

        ret = Utils.merge_queries(ret, facade.managers.AchievementManager(), auth_token, ['name'], 'achievements')

        return Utils.merge_queries(ret, facade.managers.CurriculumTaskAssociationManager(), auth_token, ['task', 'task_name'], 'curriculum_task_associations')


# vim:tabstop=4 shiftwidth=4 expandtab
