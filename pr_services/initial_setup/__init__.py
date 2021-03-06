"""
initial setup for the power reg 2 application
"""

import cPickle
import collections

from operator import itemgetter

import facade

from admin_crud import admin_crud

# the default fields that everyone should be able to read for any
# model they have access to
default_read_fields = frozenset(('id',
                                 'content_type',
                                 'create_timestamp',
                                 'save_timestamp'))

class InitialSetupMachine(object):
    def __init__(self):
        # what initializer methods to call, by category name
        # category base is always called, legacy is the default
        self.initializers = {
            'base' : [
              'import_ac_check_methods',
              'create_default_domains',
              'create_admin_user_group_and_role',
              'create_object_owner_role',
              'create_authenticated_user_role',
              'create_guest_role',
              'create_task_taker_role',
              'import_message_templates',
              'import_regions',
              'import_venues',
            ],
            'legacy' : [
              'create_legacy_user_role',
              'create_legacy_student_group_and_role',
              'create_legacy_instructor_group_surs_and_role',
              'create_legacy_group_manager_role',
              'create_legacy_product_line_manager_role',
              'create_legacy_instructor_manager_role',
              'create_legacy_paid_purchase_order_owner_role',
              'create_legacy_unpaid_purchase_order_owner_role',
              # we have tests that depend on this fixture, but also on legacy
              # roles, so let's import this here too
              'import_precor_org_roles',
            ],
            'precor' : [
              'import_precor_org_roles',
              'import_precor_orgs',
              'create_category_manager_group_and_role',
              'create_video_uploader_role',
              'create_video_watcher_role',
              'create_file_downloader_role',
              'create_file_uploader_role',
              'create_exam_taker_role',
              'create_precor_default_group',
              'create_session_participant_role',
            ],
        }

        self.user_manager = facade.managers.UserManager()
        self.import_manager = facade.managers.ImportManager()

    @classmethod
    def normalize_acl(cls, role_name, acl):
        """
        Adds restrictive default values for unspecified CRUD fields. Also adds
        default read attributes to the set of readable attributes for every
        model listed in the ACL.

        :param acl: dictionary representation of the ACL
        :type acl: dict
        """
        for model_name, crud in acl.iteritems():
            # set restrictive defaults if not specified
            crud.setdefault('c', False)
            crud.setdefault('d', False)
            updateable = crud.setdefault('u', set())
            readable = crud.setdefault('r', set())
            if not (isinstance(readable, collections.MutableSet)
                    and isinstance(updateable, collections.MutableSet)):
                raise TypeError("expecting a set of attributes in %s crud "
                    "for %s role" % (model_name, role_name))
            else:
                readable.update(default_read_fields)

    @classmethod
    def validate_acl(cls, role_name, acl):
        """
        Validate an ACL by checking the crud definition for appropriate values.
        The ACL should first be normalized by `normalize_acl` before validating.

        The specific checks performed ensure:
            - crud dicts only contains keys (c, r, u, and d)
            - attribute sets contain valid attributes
        """
        _read_update = itemgetter('r', 'u')
        for model_name, crud in acl.iteritems():
            if len(crud) != 4:
                # check that there are only keys for c, r, u, d
                raise ValueError("crud dict should contain only c, r, u, and d")

            for operation, attributes in zip("ru", _read_update(crud)):
                # check for extraneous attributes defined by the role
                valid_attributes = admin_crud[model_name][operation]
                invalid_attributes = list(attributes - valid_attributes)
                if invalid_attributes:
                    raise ValueError("invalid attributes %r for '%s' in %s crud"
                            " for '%s' role" % (invalid_attributes, operation,
                                model_name, role_name))

    def add_acl_to_role(self, name, methods, crud, arbitrary_perms=None):
        """
        Create model objects to represent an ACL for an authorizer role.

        :param name: Name of the role to work with (created if necessary).
        :type name: str
        :param methods: A list of dictionaries, each containing the name of an ACCheckMethod and a dict of params to pass to it.
        :type methods: list
        :param crud: A dictionary that maps model names to CRUD permissions.
        :type crud: dict
        :param arbitrary_perms: A list of strings representing arbitrary permissions.
        :type arbitrary_perms: list
        """
        role, created = facade.models.Role.objects.get_or_create(name=name)
        InitialSetupMachine.normalize_acl(name, crud)
        InitialSetupMachine.validate_acl(name, crud)
        crud = cPickle.dumps(crud)
        if arbitrary_perms is not None:
            arbitrary_perms = cPickle.dumps(arbitrary_perms)
        else:
            arbitrary_perms = ''
        acl = facade.models.ACL.objects.create(role=role, acl=crud,
            arbitrary_perm_list=arbitrary_perms)
        for m in methods:
            method = facade.models.ACCheckMethod.objects.get(name=m['name'])
            facade.models.ACMethodCall.objects.create(acl=acl,
                ac_check_method=method,
                ac_check_parameters=cPickle.dumps(m.get('params', {})))

    def call_setup_method(self, name, authz_only=False):
        """A helper for calling the setup methods we define in this package's modules."""
        exec 'from . import %s as method' % name
        authz_method = getattr(method.setup, 'authz', False)
        if not authz_only or authz_method:
            method.setup(self)

    def initial_setup(self, *args, **options):
        """Set up the initial state of the database."""
        self.options = options
        if not len(args):
            args = ['base', 'legacy']
        else:
            args = list(args)
            if 'base' in args:
                args.remove('base')
            args.insert(0, 'base')
        if options.get('templates_only'):
            self.call_setup_method('clear_message_templates')
            self.call_setup_method('import_message_templates')
            return
        if not options.has_key('authz_only'):
            options['authz_only'] = False
        elif options['authz_only']:
            self.call_setup_method('clear_authz_data')
        for category in args:
            for method in self.initializers[category]:
                self.call_setup_method(method, options['authz_only'])
        # remove the admin_token we may have created during setup
        if self.options.has_key('admin_token'):
            self.user_manager.logout(self.options['admin_token'])
        # we need to reload the ACLs because we just modified them
        facade.subsystems.Authorizer()._load_acls()

# vim:tabstop=4 shiftwidth=4 expandtab
