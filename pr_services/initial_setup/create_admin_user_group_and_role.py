import facade
from pr_services.utils import Utils
from decorators import authz

@authz
def setup(machine):
    group, created = facade.models.Group.objects.get_or_create(
        name="Super Administrators")

    if not machine.options['authz_only']:
        if machine.options.has_key('default_admin_password'):
            password = machine.options['default_admin_password']
        else:
            password = 'admin'
        salt = machine.user_manager._generate_password_salt()
        password_hash = Utils._hash(password + salt, 'SHA-512')

        user = facade.models.User.objects.create(first_name="admin",
            last_name="user", status='active', email='admin@admin.org')
        user.groups.add(group) # no need to save(), it's a ManyToManyField

        local_domain = facade.models.Domain.objects.get(name='local')
        da = facade.models.DomainAffiliation.objects.create(user=user,
            username='admin', domain=local_domain, default=True,
            password_hash=password_hash, password_salt=salt)

    methods = [
        {'name' : 'actor_member_of_group', 'params' : {'group_id' : group.id}},
        {'name' : 'refund_does_not_exceed_payment', 'params' : {}},
    ]
    arb_perm_list = [
        'access_db_settings',
        'change_password_of_other_users',
        'check_usernames',
        'exceed_enrollment_capacity',
        'export_exam_to_xml',
        'import_exam_from_xml',
        'logging',
        'read_reports',
        'regenerate_payment_confirmations',
        'resend_payment_confirmations',
        'send_email',
        'upload_scorm_course',
    ]
    crud = {
        'Achievement' : {
            'c' : True,
            'r' : set(('component_achievements', 'description', 'name', 'users', 'yielded_achievements',)),
            'u' : set(('component_achievements', 'description', 'name', 'users', 'yielded_achievements',)),
            'd' : True,
            },
        'AchievementAward' : {
            'c' : True,
            'r' : set(('achievement', 'assignment', 'date', 'user')),
            'u' : set(('achievement', 'assignment', 'date', 'user')),
            'd' : True,
            },
        'Answer' : {
            'c' : True,
            'r' : set(('correct', 'end_exam', 'end_question_pool', 'label',
                'next_question_pool', 'order', 'question',
                'text_response', 'value',)),
            'u' : set(('correct', 'end_exam', 'end_question_pool', 'label',
                'next_question_pool', 'order', 'question',
                'text_response', 'value',)),
            'd' : True,
            },
        'Assignment' : {
            'c' : True,
            'r' : set(('task', 'task_content_type', 'user', 'date_started',
                'date_completed', 'due_date', 'prerequisites_met',
                'effective_date_assigned', 'status', 'status_change_log',
                'assignment_attempts',)),
            'u' : set(('due_date', 'effective_date_assigned', 'status', 'date_started',
                'date_completed',)),
            'd' : True,
            },
        'AssignmentAttempt' : {
            'c' : True,
            'r' : set(('assignment', 'date_started', 'date_completed',)),
            'u' : set(('date_started', 'date_completed',)),
            'd' : True,
            },
        'Category' : {
            'c' : True,
            'r' : set(('authorized_groups', 'managers', 'name', 'locked', 'videos', 'approved_videos',)),
            'u' : set(('authorized_groups', 'managers', 'name', 'locked', 'videos',)),
            'd' : True,
            },
        'ConditionTest' : {
            'c' : True,
            'r' : set(('sequence', 'condition_test_collection', 'match_all_defined_parameters',
                'groups', 'credentials', 'events', 'sessions',
                'session_user_role_requirements', 'start', 'end',)),
            'u' : set(('sequence', 'condition_test_collection', 'match_all_defined_parameters',
                'groups', 'credentials', 'events', 'sessions',
                'session_user_role_requirements', 'start', 'end',)),
            'd' : True,
            },
        'ConditionTestCollection' : {
                'c' : True,
                'r' : set(('name', 'condition_tests',)),
                'u' : set(('name',)),
                'd' : True,
                },
        'CSVData' : {
                'c' : True,
                'r' : set(),
                'u' : set(),
                'd' : True,
                },
        'Curriculum' : {
                'c' : True,
                'r' : set(('name', 'organization', 'achievements', 'tasks', 'curriculum_task_associations',)),
                'u' : set(('name', 'organization', 'achievements', 'tasks',)),
                'd' : True,
                },
        'CurriculumEnrollment' : {
                'c' : True,
                'r' : set(('assignments', 'curriculum', 'curriculum_name', 'users', 'user_completion_statuses', 'start', 'end',)),
                'u' : set(('curriculum', 'users', 'start', 'end',)),
                'd' : True,
                },
        'CurriculumEnrollmentUserAssociation' : {
                'c' : True,
                'r' : set(),
                'u' : set(),
                'd' : True,
                },
        'CurriculumTaskAssociation' : {
                'c' : True,
                'r' : set(('curriculum', 'task', 'task_name', 'task_bundle', 'days_to_complete', 'days_before_start', 'presentation_order', 'continue_automatically',)),
                'u' : set(('curriculum', 'task', 'task_bundle', 'days_to_complete', 'days_before_start', 'presentation_order', 'continue_automatically',)),
                'd' : True,
                },
        'CustomAction' : {
                'c' : True,
                'r' : set(('name', 'description', 'function_name',)),
                'u' : set(('name', 'description', 'function_name',)),
                'd' : True,
                },
        'Domain' : {
                'c' : True,
                'r' : set(('authentication_ip', 'name', 'users',)),
                'u' : set(('authentication_password_hash', 'authentication_ip', 'name',)),
                'd' : True,
                },
        'DomainAffiliation' : {
                'c' : True,
                'r' : set(('default', 'domain', 'may_log_me_in', 'user', 'username',)),
                'u' : set(('default', 'domain', 'may_log_me_in', 'user', 'username',)),
                'd' : True,
                },
        'FormPage' : {
                'c' : True,
                'r' : set(('exam', 'form_widgets', 'number', 'photo',)),
                'u' : set(('exam', 'form_widgets', 'number',)),
                'd' : True,
                },
        'FormWidget' : {
                'c' : True,
                'r' : set(('answer', 'form_page', 'question', 'height', 'width', 'x', 'y',)),
                'u' : set(('answer', 'form_page', 'question', 'height', 'width', 'x', 'y',)),
                'd' : True,
                },
        'forum.ForumPostAttachment' : {
                'c' : True,
                'r' : set(('description', 'name', 'post',)),
                'u' : set(('description', 'name', 'post',)),
                'd' : True,
                },
        'forum.ForumCategory' : {
                'c' : True,
                'r' : set(('name', 'forums',)),
                'u' : set(('name',)),
                'd' : True,
                },
        'forum.Forum' : {
                'c' : True,
                'r' : set(('category', 'description', 'name', 'topics',)),
                'u' : set(('category', 'description', 'name',)),
                'd' : True,
                },
        'forum.ForumPost' : {
                'c' : True,
                'r' : set(('topic', 'body', 'attachments',)),
                'u' : set(('topic', 'body',)),
                'd' : True,
                },
        'forum.ForumTopic' : {
                'c' : True,
                'r' : set(('closed', 'forum', 'name', 'posts', 'sticky',)),
                'u' : set(('closed', 'forum', 'name', 'sticky',)),
                'd' : True,
                },
        'SessionTemplate' : {
                'c' : True,
                'r' : set(('active', 'audience', 'description', 'duration', 'fullname', 'lead_time', 'sequence',
                    'price', 'product_line', 'shortname', 'version', 'event_template',
                    'session_template_resource_type_requirements', 'session_template_user_role_requirements',
                    'sessions', 'modality',)),
                'u' : set(('active', 'audience', 'description', 'duration', 'fullname', 'lead_time', 'event_template', 'sequence',
                    'price', 'product_line', 'shortname', 'version', 'modality',)),
                'd' : True,
                },
        'SessionTemplateResourceTypeReq' : {
                'c' : True,
                'r' : set(('max', 'min', 'resource_type', 'session_template',)),
                'u' : set(('max', 'min', 'resource_type', 'session_template',)),
                'd' : True,
                },
        'SessionTemplateUserRoleReq' : {
                'c' : True,
                'r' : set(('max', 'min', 'session_template', 'session_user_role',)),
                'u' : set(('max', 'min', 'session_template', 'session_user_role',)),
                'd' : True,
                },
        'Credential' : {
                'c' : True,
                'r' : set(('authority', 'credential_type', 'date_assigned',
                    'date_expires', 'date_granted', 'date_started',
                    'serial_number', 'status', 'user', 'notes',)),
                'u' : set(('authority', 'credential_type', 'date_assigned',
                    'date_expires', 'date_granted', 'date_started',
                    'serial_number', 'status', 'user',)),
                'd' : True,
                },
        'CredentialType' : {
                'c' : True,
                'r' : set(('description', 'name', 'notes', 'min_required_tasks',
                    'required_achievements', 'prerequisite_credential_types',)),
                'u' : set(('description', 'name', 'notes', 'min_required_tasks',
                    'required_achievements', 'prerequisite_credential_types',)),
                'd' : True,
                },
        'EncodedVideo' : {
                'c' : True,
                'r' : set(('video', 'bitrate', 'url', 'http_url',)),
                'u' : set(),
                'd' : True,
                },
        'EventTemplate' : {
                'c' : True,
                'r' : set(('external_reference', 'lag_time', 'organization', 'events',
                    'lead_time', 'name_prefix', 'title', 'description', 'session_templates',
                    'url', 'product_line', 'facebook_message', 'twitter_message',)),
                'u' : set(('external_reference', 'lag_time', 'lead_time', 'name_prefix', 'organization',
                    'title', 'description', 'url', 'product_line', 'facebook_message', 'twitter_message',)),
                'd' : True,
                },
        'Event' : {
                'c' : True,
                'r' : set(('external_reference', 'region', 'lag_time', 'organization', 'event_template',
                    'lead_time', 'name', 'title', 'description', 'start', 'end', 'sessions',
                    'owner', 'venue', 'status', 'url', 'product_line', 'facebook_message', 'twitter_message',)),
                'u' : set(('external_reference', 'region', 'lag_time', 'lead_time', 'name', 'organization', 'event_template',
                    'owner', 'title', 'description', 'start', 'end', 'venue', 'url', 'product_line', 'facebook_message', 'twitter_message',)),
                'd' : True,
                },
        'Exam' : {
                'c' : True,
                'r' : set(('passing_score', 'question_pools', 'title', 'achievements',
                    'description', 'name', 'prerequisite_tasks', 'type',
                    'version_id', 'version_label', 'version_comment',)),
                'u' : set(('passing_score', 'question_pools', 'title', 'achievements',
                    'description', 'name', 'prerequisite_tasks',
                    'version_id', 'version_label', 'version_comment',)),
                'd' : True,
                },
        'ExamSession' : {
                'c' : True,
                'r' : set(('date_started', 'date_completed', 'exam', 'response_questions',
                    'passing_score', 'number_correct', 'passed', 'score', 'user',)),
                'u' : set(('date_completed',)),
                'd' : True,
                },
        'FileDownload' : {
                'c' : True,
                'r' : set(('achievements', 'name', 'description', 'file_size', 'file_url', 'deleted', 'title', 'prerequisite_tasks')),
                'u' : set(('achievements', 'name', 'description', 'title', 'prerequisite_tasks')),
                'd' : True,
                },
        'FileDownloadAttempt' : {
                'c' : True,
                'r' : set(('assignment', 'date_started', 'date_completed', 'file_download',
                    'user',)),
                'u' : set(('date_completed',)),
                'd' : True,
                },
        'FileUpload' : {
                'c' : True,
                'r' : set(('achievements', 'name', 'description',)),
                'u' : set(('achievements', 'name', 'description',)),
                'd' : True,
                },
        'FileUploadAttempt' : {
                'c' : True,
                'r' : set(('assignment', 'date_started', 'date_completed', 'file_upload',
                    'user', 'file_name', 'file_size', 'file_url', 'deleted',)),
                'u' : set(('date_completed',)),
                'd' : True,
                },
        'Group' : {
                'c' : True,
                'r' : set(('categories', 'default', 'managers', 'name', 'users', 'notes',)),
                'u' : set(('categories', 'default', 'managers', 'name', 'users',)),
                'd' : True,
                },
        'Note' : {
                'c' : True,
                'r' : set(('text',)),
                'u' : set(('text',)),
                'd' : True,
                },
        'Organization' : {
                'c' : True,
                'r' : set(('address', 'department', 'description', 'email', 'fax', 'name', 'notes', 'phone', 'photo_url',
                    'parent', 'children', 'ancestors', 'descendants', 'org_email_domains',
                    'primary_contact_first_name', 'primary_contact_last_name', 'primary_contact_office_phone',
                    'primary_contact_cell_phone', 'primary_contact_other_phone', 'primary_contact_email',
                    'purchase_orders', 'training_unit_accounts', 'url', 'roles', 'users', 'user_org_roles',)),
                'u' : set(('address', 'department', 'description', 'email', 'fax', 'name', 'notes', 'phone', 'photo_url', 'parent',
                    'primary_contact_first_name', 'primary_contact_last_name', 'primary_contact_office_phone', 'primary_contact_cell_phone',
                    'primary_contact_other_phone', 'primary_contact_email', 'url', 'roles', 'users',)),
                'd' : True,
                },
        'OrgEmailDomain' : {
                'c' : True,
                'r' : set(('email_domain', 'organization', 'role', 'effective_role', 'effective_role_name',)),
                'u' : set(('email_domain', 'organization', 'role',)),
                'd' : True,
                },
        'OrgRole' : {
                'c' : True,
                'r' : set(('name', 'organizations', 'users', 'user_org_roles',)),
                'u' : set(('name', 'organizations', 'users',)),
                'd' : True,
                },
        'Payment' : {
                'c' : True,
                'r' : set(('refunds', 'card_type', 'exp_date', 'amount',
                    'first_name', 'last_name', 'city', 'state', 'zip', 'country',
                    'sales_tax', 'transaction_id', 'invoice_number', 'result_message', 'purchase_order',
                    'date',)),
                'u' : set(),
                'd' : False,
                },
        'Product' : {
                'c' : True,
                'r' : set(('custom_actions', 'description', 'display_order', 'inventory', 'cost', 'name', 'price', 'sku', 'starting_quantity', 'training_units',)),
                'u' : set(('custom_actions', 'description', 'display_order', 'cost', 'name', 'price', 'sku', 'starting_quantity', 'training_units',)),
                'd' : True,
                },
        'ProductDiscount' : {
                'c' : True,
                'r' : set(('condition_test_collection', 'cumulative', 'currency', 'percentage', 'products', 'product_offers', 'promo_code',)),
                'u' : set(('condition_test_collection', 'cumulative', 'currency', 'percentage', 'products', 'product_offers', 'promo_code',)),
                'd' : True,
                },
        'ProductLine' : {
                'c' : True,
                'r' : set(('instructor_managers', 'instructors', 'managers',
                    'name', 'notes',)),
                'u' : set(('instructor_managers', 'instructors', 'managers', 'name',)),
                'd' : True,
                },
        'ProductOffer' : {
                'c' : True,
                'r' : set(('product', 'seller', 'description', 'price',)),
                'u' : set(('product', 'seller', 'description', 'price',)),
                'd' : True,
                },
        'ProductClaim' : {
                'c' : True,
                'r' : set(('product', 'purchase_order', 'quantity',)),
                'u' : set(('quantity',)),
                'd' : True,
                },
        'PurchaseOrder' : {
                'c' : True,
                'r' : set(('user', 'product_offers', 'products', 'promo_code',
                    'product_discounts', 'organization',
                    'expiration', 'payments', 'total_price', 'training_units_purchased',
                    'training_units_price', 'is_paid',)),
                'u' : set(('user', 'organization', 'promo_code',
                    'expiration', 'training_units_purchased', 'training_units_price',)),
                'd' : True,
                },
        'Question' : {
                'c' : True,
                'r' : set(('answers', 'rejoinder', 'label', 'help_text',
                    'max_answers', 'min_answers', 'max_length', 'min_length',
                    'max_value', 'min_value', 'order', 'question_pool',
                    'question_type', 'required', 'text_regex',
                    'text_response', 'text_response_label', 'widget',)),
                'u' : set(('answers', 'rejoinder', 'label', 'help_text',
                    'max_answers', 'min_answers', 'max_length', 'min_length',
                    'max_value', 'min_value', 'order', 'question_pool',
                    'question_type', 'required', 'text_regex',
                    'text_response', 'text_response_label', 'widget',)),
                'd' : True,
                },
        'QuestionPool' : {
                'c' : True,
                'r' : set(('exam', 'name', 'number_to_answer', 'order',
                    'questions', 'randomize_questions', 'title',)),
                'u' : set(('exam', 'name', 'number_to_answer', 'order',
                    'questions', 'randomize_questions', 'title',)),
                'd' : True,
                },
        'Refund' : {
                'c' : True,
                'r' : set(),
                'u' : set(),
                'd' : False,
                },
        'Region' : {
                'c' : True,
                'r' : set(('name', 'notes', 'events', 'venues',)),
                'u' : set(('name', 'events', 'venues',)),
                'd' : True,
                },
        'Resource' : {
                'c' : True,
                'r' : set(('name', 'description', 'notes', 'resource_types',
                    'session_resource_type_requirements',)),
                'u' : set(('name', 'description', 'resource_types',
                    'session_resource_type_requirements',)),
                'd' : True,
                },
        'ResourceType' : {
                'c' : True,
                'r' : set(('name', 'notes', 'resources',
                    'sessionresourcetyperequirements',
                    'sessiontemplateresourcetypereqs',)),
                'u' : set(('name', 'resources', 'sessionresourcetyperequirements',
                    'sessiontemplateresourcetypereqs',)),
                'd' : True,
                },
        'Response' : {
                'c' : True,
                'r' : set(('exam_session', 'correct', 'question', 'text', 'valid',
                    'value',)),
                'u' : set(),
                'd' : True,
                },
        'Role' : {
                'c' : True,
                'r' : set(('name', 'ac_check_methods', 'acl', 'notes',)),
                'u' : set(('name', 'ac_check_methods', 'acl', 'notes',)),
                'd' : True,
                },
        'Room' : {
                'c' : True,
                'r' : set(('name', 'capacity', 'venue', 'venue_name', 'venue_address',)),
                'u' : set(('name', 'capacity', 'venue',)),
                'd' : True,
                },
        'Sco' : {
                'c' : True,
                'r' : set(('achievements', 'course', 'completion_requirement', 'data', 'url',
                    'description', 'name', 'title', 'prerequisite_tasks',
                    'version_id', 'version_label', 'version_comment',)),
                'u' : set(('achievements', 'completion_requirement', 'description', 'name', 'title',
                    'prerequisite_tasks', 'version_id', 'version_label',
                    'version_comment',)),
                'd' : True,
                },
        'ScoSession' : {
                'c' : True,
                'r' : set(('cmi_core_lesson_location',
                    'cmi_core_lesson_status', 'cmi_core_score_max', 'cmi_core_score_min',
                    'shared_object', 'sco', 'date_completed', 'date_started',)),
                'u' : set(('date_completed', 'date_started',)),
                'd' : True,
                },
        'Session' : {
                'c' : True,
                'r' : set(( 'session_user_role_requirements', 'session_resource_type_requirements', 'audience',
                    'confirmed', 'session_template', 'default_price',
                    'description', 'end', 'evaluation', 'fullname', 'lead_time', 'modality',
                    'room', 'shortname', 'start', 'status', 'title', 'url', 'event',
                    'session_user_roles', 'paypal_url',)),
                'u' : set(( 'session_user_role_requirements', 'session_resource_type_requirements', 'audience',
                    'confirmed', 'session_template', 'default_price', 'description',
                    'end', 'fullname', 'lead_time', 'modality', 'room', 'shortname', 'start', 'status',
                    'session_user_roles', 'title', 'url', 'event',)),
                'd' : True,
                },
        'SessionResourceTypeRequirement' : {
                'c' : True,
                'r' : set(('session', 'max', 'min', 'resource_type', 'resources',)),
                'u' : set(('session', 'max', 'min', 'resource_type', 'resources',)),
                'd' : True,
                },
        'SessionUserRole' : {
                'c' : True,
                'r' : set(('name', 'session_user_role_requirements',)),
                'u' : set(('name', 'session_user_role_requirements',)),
                'd' : True,
                },
        'SessionUserRoleRequirement' : {
                'c' : True,
                'r' : set(('achievements', 'credential_types', 'max', 'users',
                    'remaining_capacity', 'session', 'session_user_role', 'min',
                    'prerequisite_tasks', 'role_name', 'ignore_room_capacity',)),
                'u' : set(('achievements', 'credential_types', 'max', 'users', 'session',
                    'prerequisite_tasks', 'session_user_role', 'min', 'ignore_room_capacity',)),
                'd' : True,
                },
        'Task' : {
                'c' : True,
                'r' : set(('description', 'name', 'title', 'prerequisite_tasks', 'achievements',
                    'remaining_capacity', 'type', 'min', 'max',
                    'version_id', 'version_label', 'version_comment', 'yielded_tasks',)),
                'u' : set(('description', 'name', 'title', 'prerequisite_tasks', 'achievements',
                    'version_id', 'version_label', 'min', 'max',
                    'version_comment', 'yielded_tasks',)),
                'd' : True,
                },
        'TaskBundle': {
                'c': True,
                'r': set(('name', 'description', 'tasks', 'tasks_depr',)),
                'u': set(('name', 'description', 'tasks', 'tasks_depr',)),
                'd': True,
                },
        'TaskBundleTaskAssociation': {
                'c': True,
                'r': set(('task', 'task_bundle', 'presentation_order', 'continue_automatically',)),
                'u': set(('task', 'task_bundle', 'presentation_order', 'continue_automatically',)),
                'd': True,
                },
        'TaskFee' : {
                'c' : True,
                'r' : set(('custom_actions', 'description', 'display_order', 'inventory', 'cost', 'name', 'price', 'sku', 'starting_quantity', 'task', 'training_units',)),
                'u' : set(('custom_actions', 'description', 'display_order', 'cost', 'name', 'price', 'sku', 'starting_quantity', 'task', 'training_units',)),
                'd' : True,
                },
        'TrainingUnitAccount' : {
                'c' : True,
                'r' : set(('organization', 'user', 'balance',
                    'training_unit_transactions',)),
                'u' : set(('organization', 'user', 'starting_value',)),
                'd' : True,
                },
        'TrainingUnitAuthorization' : {
                'c' : True,
                'r' : set(('start', 'training_unit_account', 'end', 'user',
                    'used_value', 'max_value',)),
                'u' : set(('start', 'training_unit_account', 'end', 'user', 'max_value',)),
                'd' : True,
                },
        'TrainingUnitTransaction' : {
                'c' : True,
                'r' : set(('training_unit_authorizations',
                    'value', 'purchase_order',)),
                'u' : set(('training_unit_authorizations',)),
                'd' : True,
                },
        'TrainingVoucher' : {
                'c' : True,
                'r' : set(('price', 'session_user_role_requirement',
                    'code', 'purchase_order',)),
                'u' : set(('session_user_role_requirement', 'purchase_order',)),
                'd' : True,
                },
        'User' : {
                'c' : True,
                'r' : set(('credentials',
                    'session_user_role_requirements', 'product_lines_managed',
                    'product_lines_instructor_manager_for',
                    'product_lines_instructor_for', 'groups',
                    'roles', 'photo_url', 'url', 'username', 'domains',
                    'title', 'first_name', 'middle_name', 'last_name',
                    'name_suffix', 'full_name',
                    'phone', 'phone2', 'phone3', 'email', 'email2', 'status',
                    'color_code', 'biography',
                    'shipping_address', 'billing_address', 'organizations', 'owned_userorgroles',
                    'preferred_venues',
                    'completed_curriculum_enrollments',
                    'incomplete_curriculum_enrollments', 'paypal_address', 'enable_paypal',
                    'suppress_emails', 'is_staff',
                    'default_username_and_domain', 'alleged_organization',)),
                'u' : set(( 'credentials',
                    'groups', 'roles', 'photo_url',
                    'url',
                    'title', 'first_name', 'middle_name', 'last_name', 'name_suffix',
                    'phone', 'phone2', 'phone3',
                    'email', 'email2', 'status', 'color_code', 'biography',
                    'shipping_address', 'billing_address', 'organizations',
                    'preferred_venues',
                    'paypal_address',
                    'enable_paypal', 'suppress_emails', 'is_staff', 'alleged_organization',)),
                'd' : True,
                },
        'UserOrgRole' : {
                'c' : True,
                'r' : set(('owner', 'organization', 'organization_name', 'role', 'role_name', 'parent', 'children', 'persistent', 'title',)),
                'u' : set(('owner', 'organization', 'role', 'parent', 'persistent', 'title',)),
                'd' : True,
                },
        'Venue' : {
                'c' : True,
                'r' : set(('blackout_periods', 'contact', 'region', 'address', 'owner', 'phone',
                    'name', 'events', 'rooms', 'hours_of_operation',)),
                'u' : set(('contact', 'region', 'address', 'owner', 'phone', 'name', 'events', 'hours_of_operation',)),
                'd' : True,
                },
        'BlackoutPeriod' : {
                'c' : True,
                'r' : set(('venue', 'start', 'end', 'description',)),
                'u' : set(('venue', 'start', 'end', 'description',)),
                'd' : True,
                },
        'Video' : {
                'c' : True,
                'r' : set(('id', 'approved_categories', 'aspect_ratio', 'author',
                    'categories', 'category_relationships', 'create_timestamp',
                    'deleted', 'description',
                    'encoded_videos', 'is_ready', 'length', 'live', 'name', 'title', 'num_views', 'owner',
                    'photo_url', 'prerequisite_tasks', 'public', 'src_file_size',
                    'status', 'tags', 'users_who_watched',
                    'version_id', 'version_label', 'version_comment',)),
                'u' : set(('aspect_ratio', 'author', 'categories', 'description',
                    'encoded_videos', 'length', 'live', 'name', 'title', 'owner',
                    'photo_url', 'prerequisite_tasks', 'public',
                    'tags', 'version_id', 'version_label', 'version_comment',)),
                'd' : True,
                },
        'VideoCategory' : {
                'c' : True,
                'r' : set(('status', 'category', 'category_name', 'video',)),
                'u' : set(('status',)),
                'd' : True,
                },
        'VideoSession' : {
                'c' : True,
                'r' : set(('assignment', 'date_started', 'date_completed', 'user', 'video',)),
                'u' : set(('date_started', 'date_completed',)),
                'd' : True,
                },
    }
    machine.add_acl_to_role('Admin', methods, crud, arb_perm_list)

    if not machine.options['authz_only']:
        # we need to reload ACLs that were just modified before using them to login
        facade.subsystems.Authorizer()._load_acls()

        # we log in here so that other setup methods can have an admin_token
        token_str = machine.user_manager.login('admin', password)['auth_token']
        machine.options['admin_token'] = Utils.get_auth_token_object(token_str)
