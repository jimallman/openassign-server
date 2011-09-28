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
        'check_usernames',
        'change_password_of_other_users',
        'exceed_enrollment_capacity',
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
            'r' : ['component_achievements', 'description', 'name', 'users', 'yielded_achievements'],
            'u' : ['component_achievements', 'description', 'name', 'users', 'yielded_achievements'],
            'd' : True,
        },
        'AchievementAward' : {
            'c' : True,
            'r' : ['assignment', 'date'],
            'u' : ['assignment', 'date'],
            'd' : True,
        },
        'Answer' : {
            'c' : True,
            'r' : ['correct', 'end_exam', 'end_question_pool', 'label',
                   'next_question_pool', 'order', 'question',
                   'text_response', 'value'],
            'u' : ['correct', 'end_exam', 'end_question_pool', 'label',
                   'next_question_pool', 'order', 'question',
                   'text_response', 'value'],
            'd' : True,
        },
        'Assignment' : {
            'c' : True,
            'r' : ['task', 'task_content_type', 'user', 'date_started',
                   'date_completed', 'due_date', 'prerequisites_met',
                   'effective_date_assigned', 'status', 'status_change_log', 
                   'assignment_attempts'],
            'u' : ['due_date', 'effective_date_assigned', 'status', 'date_started',
                   'date_completed'],
            'd' : True,
        },
        'AssignmentAttempt' : {
            'c' : True,
            'r' : ['assignment', 'date_started', 'date_completed'],
            'u' : ['date_started', 'date_completed'],
            'd' : True,
        },
        'Category' : {
            'c' : True,
            'r' : ['authorized_groups', 'managers', 'name', 'locked', 'videos', 'approved_videos'],
            'u' : ['authorized_groups', 'managers', 'name', 'locked', 'videos'],
            'd' : True,
        },
        'ConditionTest' : {
            'c' : True,
            'r' : ['sequence', 'condition_test_collection', 'match_all_defined_parameters',
                    'groups', 'credentials', 'events', 'sessions',
                    'session_user_role_requirements', 'start', 'end'],
            'u' : ['sequence', 'condition_test_collection', 'match_all_defined_parameters',
                    'groups', 'credentials', 'events', 'sessions',
                    'session_user_role_requirements', 'start', 'end'],
            'd' : True,
        },
        'ConditionTestCollection' : {
            'c' : True,
            'r' : ['name', 'condition_tests'],
            'u' : ['name'],
            'd' : True,
        },
        'CSVData' : {
            'c' : True,
            'r' : [],
            'u' : [],
            'd' : True,
        },
        'Curriculum' : {
            'c' : True,
            'r' : ['name', 'organization', 'achievements', 'tasks', 'curriculum_task_associations'],
            'u' : ['name', 'organization', 'achievements', 'tasks'],
            'd' : True,
        },
        'CurriculumEnrollment' : {
            'c' : True,
            'r' : ['assignments', 'curriculum', 'curriculum_name', 'users', 'user_completion_statuses', 'start', 'end'],
            'u' : ['curriculum', 'users', 'start', 'end'],
            'd' : True,
        },
        'CurriculumEnrollmentUserAssociation' : {
            'c' : True,
            'r' : [],
            'u' : [],
            'd' : True,
        },
        'CurriculumTaskAssociation' : {
            'c' : True,
            'r' : ['curriculum', 'task', 'task_name', 'task_bundle', 'days_to_complete', 'days_before_start', 'presentation_order', 'continue_automatically'],
            'u' : ['curriculum', 'task', 'task_bundle', 'days_to_complete', 'days_before_start', 'presentation_order', 'continue_automatically'],
            'd' : True,
        },
        'CustomAction' : {
            'c' : True,
            'r' : ['name', 'description', 'function_name'],
            'u' : ['name', 'description', 'function_name'],
            'd' : True,
        },
        'Domain' : {
            'c' : True,
            'r' : ['authentication_ip', 'name', 'users'],
            'u' : ['authentication_password_hash', 'authentication_ip', 'name'],
            'd' : True,
        },
        'DomainAffiliation' : {
            'c' : True,
            'r' : ['default', 'domain', 'may_log_me_in', 'user', 'username'],
            'u' : ['default', 'domain', 'may_log_me_in', 'user', 'username'],
            'd' : True,
        },
        'FormPage' : {
            'c' : True,
            'r' : ['exam', 'form_widgets', 'number', 'photo'],
            'u' : ['exam', 'form_widgets', 'number'],
            'd' : True,
        },
        'FormWidget' : {
            'c' : True,
            'r' : ['answer', 'form_page', 'question', 'height', 'width', 'x', 'y'],
            'u' : ['answer', 'form_page', 'question', 'height', 'width', 'x', 'y'],
            'd' : True,
        },
        'forum.ForumPostAttachment' : {
            'c' : True,
            'r' : ['description', 'name', 'post'],
            'u' : ['description', 'name', 'post'],
            'd' : True,
        },
        'forum.ForumCategory' : {
            'c' : True,
            'r' : ['name', 'forums'],
            'u' : ['name'],
            'd' : True,
        },
        'forum.Forum' : {
            'c' : True,
            'r' : ['category', 'description', 'name', 'topics'],
            'u' : ['category', 'description', 'name'],
            'd' : True,
        },
        'forum.ForumPost' : {
            'c' : True,
            'r' : ['topic', 'body', 'attachments'],
            'u' : ['topic', 'body'],
            'd' : True,
        },
        'forum.ForumTopic' : {
            'c' : True,
            'r' : ['closed', 'forum', 'name', 'posts', 'sticky'],
            'u' : ['closed', 'forum', 'name', 'sticky'],
            'd' : True,
        },
        'SessionTemplate' : {
            'c' : True,
            'r' : ['active', 'audience', 'description', 'duration', 'fullname', 'lead_time', 'sequence',
                    'price', 'product_line', 'shortname', 'version', 'event_template',
                    'session_template_resource_type_requirements', 'session_template_user_role_requirements',
                    'sessions', 'modality'],
            'u' : ['active', 'audience', 'description', 'duration', 'fullname', 'lead_time', 'event_template', 'sequence',
                   'price', 'product_line', 'shortname', 'version', 'modality'],
            'd' : True,
        },
        'SessionTemplateResourceTypeReq' : {
            'c' : True,
            'r' : ['max', 'min', 'resource_type', 'session_template'],
            'u' : ['max', 'min', 'resource_type', 'session_template'],
            'd' : True,
        },
        'SessionTemplateUserRoleReq' : {
            'c' : True,
            'r' : ['max', 'min', 'session_template', 'session_user_role'],
            'u' : ['max', 'min', 'session_template', 'session_user_role'],
            'd' : True,
        },
        'Credential' : {
            'c' : True,
            'r' : ['authority', 'credential_type', 'date_assigned',
                   'date_expires', 'date_granted', 'date_started',
                   'serial_number', 'status', 'user', 'notes'],
            'u' : ['authority', 'credential_type', 'date_assigned',
                   'date_expires', 'date_granted', 'date_started',
                   'serial_number', 'status', 'user'],
            'd' : True,
        },
        'CredentialType' : {
            'c' : True,
            'r' : ['description', 'name', 'notes', 'min_required_tasks',
                   'required_achievements', 'prerequisite_credential_types'],
            'u' : ['description', 'name', 'notes', 'min_required_tasks',
                   'required_achievements', 'prerequisite_credential_types'],
            'd' : True,
        },
        'EncodedVideo' : {
            'c' : True,
            'r' : ['video', 'bitrate', 'url', 'http_url'],
            'u' : [],
            'd' : True,
        },
        'EventTemplate' : {
            'c' : True,
            'r' : ['external_reference', 'lag_time', 'organization', 'events',
                    'lead_time', 'name_prefix', 'title', 'description', 'session_templates',
                    'url', 'product_line', 'facebook_message', 'twitter_message',],
            'u' : ['external_reference', 'lag_time', 'lead_time', 'name_prefix', 'organization',
                    'title', 'description', 'url', 'product_line', 'facebook_message', 'twitter_message',],
            'd' : True,
        },
        'Event' : {
            'c' : True,
            'r' : ['external_reference', 'region', 'lag_time', 'organization', 'event_template',
                      'lead_time', 'name', 'title', 'description', 'start', 'end', 'sessions',
                      'owner', 'venue', 'status', 'url', 'product_line', 'facebook_message', 'twitter_message',],
            'u' : ['external_reference', 'region', 'lag_time', 'lead_time', 'name', 'organization', 'event_template',
                   'owner', 'title', 'description', 'start', 'end', 'venue', 'url', 'product_line', 'facebook_message', 'twitter_message',],
            'd' : True,
        },
        'Exam' : {
            'c' : True,
            'r' : ['passing_score', 'question_pools', 'title', 'achievements',
                   'description', 'name', 'prerequisite_tasks', 'type',
                   'version_id', 'version_label', 'version_comment',],
            'u' : ['passing_score', 'question_pools', 'title', 'achievements',
                   'description', 'name', 'prerequisite_tasks',
                   'version_id', 'version_label', 'version_comment',],
            'd' : True,
        },
        'ExamSession' : {
            'c' : True,
            'r' : ['date_started', 'date_completed', 'exam', 'response_questions',
                      'passing_score', 'number_correct', 'passed', 'score', 'user'],
            'u' : ['date_completed'],
            'd' : True,
        },
        'Group' : {
            'c' : True,
            'r' : ['categories', 'default', 'managers', 'name', 'users', 'notes'],
            'u' : ['categories', 'default', 'managers', 'name', 'users'],
            'd' : True,
        },
        'Note' : {
            'c' : True,
            'r' : ['text'],
            'u' : ['text'],
            'd' : True,
        },
        'Organization' : {
            'c' : True,
            'r' : ['address', 'department', 'description', 'email', 'fax', 'name', 'notes', 'phone', 'photo_url',
                    'parent', 'children', 'ancestors', 'descendants', 'org_email_domains',
                    'primary_contact_first_name', 'primary_contact_last_name', 'primary_contact_office_phone',
                    'primary_contact_cell_phone', 'primary_contact_other_phone', 'primary_contact_email',
                    'purchase_orders', 'training_unit_accounts', 'url', 'roles', 'users', 'user_org_roles'],
            'u' : ['address', 'department', 'description', 'email', 'fax', 'name', 'notes', 'phone', 'photo_url', 'parent',
                    'primary_contact_first_name', 'primary_contact_last_name', 'primary_contact_office_phone', 'primary_contact_cell_phone',
                    'primary_contact_other_phone', 'primary_contact_email', 'url', 'roles', 'users'],
            'd' : True,
        },
        'OrgEmailDomain' : {
            'c' : True,
            'r' : ['email_domain', 'organization', 'role', 'effective_role', 'effective_role_name'],
            'u' : ['email_domain', 'organization', 'role'],
            'd' : True,
        },
        'OrgRole' : {
            'c' : True,
            'r' : ['name', 'organizations', 'users', 'user_org_roles'],
            'u' : ['name', 'organizations', 'users'],
            'd' : True,
        },
        'Payment' : {
            'c' : True,
            'r' : ['refunds', 'card_type', 'exp_date', 'amount',
                      'first_name', 'last_name', 'city', 'state', 'zip', 'country',
                      'sales_tax', 'transaction_id', 'invoice_number', 'result_message', 'purchase_order',
                      'date'],
            'u' : [],
            'd' : False,
        },
        'Product' : {
            'c' : True,
            'r' : ['custom_actions', 'description', 'display_order', 'inventory', 'cost', 'name', 'price', 'sku', 'starting_quantity', 'training_units'],
            'u' : ['custom_actions', 'description', 'display_order', 'cost', 'name', 'price', 'sku', 'starting_quantity', 'training_units'],
            'd' : True,
        },
        'ProductDiscount' : {
            'c' : True,
            'r' : ['condition_test_collection', 'cumulative', 'currency', 'percentage', 'products', 'product_offers', 'promo_code'],
            'u' : ['condition_test_collection', 'cumulative', 'currency', 'percentage', 'products', 'product_offers', 'promo_code'],
            'd' : True,
        },
        'ProductLine' : {
            'c' : True,
            'r' : ['instructor_managers', 'instructors', 'managers',
                      'name', 'notes'],
            'u' : ['instructor_managers', 'instructors', 'managers', 'name'],
            'd' : True,
        },
        'ProductOffer' : {
            'c' : True,
            'r' : ['product', 'seller', 'description', 'price'],
            'u' : ['product', 'seller', 'description', 'price'],
            'd' : True,
        },
        'ProductClaim' : {
            'c' : True,
            'r' : ['product', 'purchase_order', 'quantity'],
            'u' : ['quantity'],
            'd' : True,
        },
        'PurchaseOrder' : {
            'c' : True,
            'r' : ['user', 'product_offers', 'products', 'promo_code',
                      'product_discounts', 'organization',
                      'expiration', 'payments', 'total_price', 'training_units_purchased',
                      'training_units_price', 'is_paid'],
            'u' : ['user', 'organization', 'promo_code',
                    'expiration', 'training_units_purchased', 'training_units_price'],
            'd' : True,
        },
        'Question' : {
            'c' : True,
            'r' : ['answers', 'rejoinder', 'label', 'help_text',
                   'max_answers', 'min_answers', 'max_length', 'min_length',
                   'max_value', 'min_value', 'order', 'question_pool',
                   'question_type', 'required', 'text_regex',
                   'text_response', 'text_response_label', 'widget'],
            'u' : ['answers', 'rejoinder', 'label', 'help_text',
                   'max_answers', 'min_answers', 'max_length', 'min_length',
                   'max_value', 'min_value', 'order', 'question_pool',
                   'question_type', 'required', 'text_regex',
                   'text_response', 'text_response_label', 'widget'],
            'd' : True,
        },
        'QuestionPool' : {
            'c' : True,
            'r' : ['exam', 'name', 'number_to_answer', 'order',
                   'questions', 'randomize_questions', 'title'],
            'u' : ['exam', 'name', 'number_to_answer', 'order',
                   'questions', 'randomize_questions', 'title'],
            'd' : True,
        },
        'Refund' : {
            'c' : True,
            'r' : [],
            'u' : [],
            'd' : False,
        },
        'Region' : {
            'c' : True,
            'r' : ['name', 'notes', 'events', 'venues'],
            'u' : ['name', 'events', 'venues'],
            'd' : True,
        },
        'Resource' : {
            'c' : True,
            'r' : ['name', 'notes', 'resource_types',
                   'session_resource_type_requirements'],
            'u' : ['name', 'resource_types',
                   'session_resource_type_requirements'],
            'd' : True,
        },
        'ResourceType' : {
            'c' : True,
            'r' : ['name', 'notes', 'resources',
                   'sessionresourcetyperequirements',
                   'sessiontemplateresourcetypereqs'],
            'u' : ['name', 'resources', 'sessionresourcetyperequirements',
                   'sessiontemplateresourcetypereqs'],
            'd' : True,
        },
        'Response' : {
            'c' : True,
            'r' : ['exam_session', 'correct', 'question', 'text', 'valid',
                   'value'],
            'u' : [],
            'd' : True,
        },
        'Role' : {
            'c' : True,
            'r' : ['name', 'ac_check_methods', 'acl', 'notes'],
            'u' : ['name', 'ac_check_methods', 'acl', 'notes'],
            'd' : True,
        },
        'Room' : {
            'c' : True,
            'r' : ['name', 'capacity', 'venue'],
            'u' : ['name', 'capacity', 'venue'],
            'd' : True,
        },
        'Sco' : {
            'c' : True,
            'r' : ['achievements', 'course', 'completion_requirement', 'data', 'url',
                   'description', 'name', 'title', 'prerequisite_tasks',
                   'version_id', 'version_label', 'version_comment',],
            'u' : ['achievements', 'completion_requirement', 'description', 'name', 'title',
                   'prerequisite_tasks', 'version_id', 'version_label',
                   'version_comment',],
            'd' : True,
        },
        'ScoSession' : {
            'c' : True,
            'r' : ['cmi_core_lesson_location',
                      'cmi_core_lesson_status', 'cmi_core_score_max', 'cmi_core_score_min',
                      'shared_object', 'sco', 'date_completed', 'date_started'],
            'u' : ['date_completed', 'date_started'],
            'd' : True,
        },
        'Session' : {
            'c' : True,
            'r' : ['session_user_role_requirements', 'audience',
                      'confirmed', 'session_template', 'default_price',
                    'description', 'end', 'evaluation', 'modality', 'name',
                    'room', 'start', 'status', 'title', 'url', 'event',
                    'paypal_url'],
            'u' : [ 'session_user_role_requirements', 'audience', 'confirmed', 'session_template', 'default_price', 'description',
                    'end', 'modality', 'name', 'room', 'start', 'status',
                    'title', 'url', 'event'],
            'd' : True,
        },
        'SessionResourceTypeRequirement' : {
            'c' : True,
            'r' : ['session', 'max', 'min', 'resource_type', 'resources'],
            'u' : ['session', 'max', 'min', 'resource_type', 'resources'],
            'd' : True,
        },
        'SessionUserRole' : {
            'c' : True,
            'r' : ['name', 'session_user_role_requirements'],
            'u' : ['name', 'session_user_role_requirements'],
            'd' : True,
        },
        'SessionUserRoleRequirement' : {
            'c' : True,
            'r' : ['credential_types', 'max', 'users',
                      'remaining_capacity', 'session', 'session_user_role', 'min',
                      'ignore_room_capacity'],
            'u' : ['credential_types', 'max', 'users', 'session',
                      'session_user_role', 'min', 'ignore_room_capacity'],
            'd' : True,
        },
        'Task' : {
            'c' : True,
            'r' : ['description', 'name', 'title', 'prerequisite_tasks', 'achievements',
                   'remaining_capacity', 'type', 'min', 'max',
                   'version_id', 'version_label', 'version_comment', 'yielded_tasks'],
            'u' : ['description', 'name', 'title', 'prerequisite_tasks', 'achievements',
                   'version_id', 'version_label', 'min', 'max',
                   'version_comment', 'yielded_tasks'],
            'd' : True,
        },
        'TaskBundle': {
            'c': True,
            'r': ['name', 'description', 'tasks'],
            'u': ['name', 'description', 'tasks'],
            'd': True,
        },
        'TaskFee' : {
            'c' : True,
            'r' : ['custom_actions', 'description', 'display_order', 'inventory', 'cost', 'name', 'price', 'sku', 'starting_quantity', 'task', 'training_units'],
            'u' : ['custom_actions', 'description', 'display_order', 'cost', 'name', 'price', 'sku', 'starting_quantity', 'task', 'training_units'],
            'd' : True,
        },
        'TrainingUnitAccount' : {
            'c' : True,
            'r' : ['organization', 'user', 'balance',
                      'training_unit_transactions'],
            'u' : ['organization', 'user', 'starting_value'],
            'd' : True,
        },
        'TrainingUnitAuthorization' : {
            'c' : True,
            'r' : ['start', 'training_unit_account', 'end', 'user',
                      'used_value', 'max_value'],
            'u' : ['start', 'training_unit_account', 'end', 'user', 'max_value'],
            'd' : True,
        },
        'TrainingUnitTransaction' : {
            'c' : True,
            'r' : ['training_unit_authorizations',
                      'value', 'purchase_order'],
            'u' : ['training_unit_authorizations'],
            'd' : True,
        },
        'TrainingVoucher' : {
            'c' : True,
            'r' : ['price', 'session_user_role_requirement',
                      'code', 'purchase_order'],
            'u' : ['session_user_role_requirement', 'purchase_order'],
            'd' : True,
        },
        'User' : {
            'c' : True,
            'r' : ['credentials',
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
                   'default_username_and_domain', 'alleged_organization'],
            'u' : [ 'credentials',
                    'groups', 'roles', 'photo_url',
                    'url',
                    'title', 'first_name', 'middle_name', 'last_name', 'name_suffix',
                    'phone', 'phone2', 'phone3',
                    'email', 'email2', 'status', 'color_code', 'biography',
                    'shipping_address', 'billing_address', 'organizations',
                    'preferred_venues',
                    'paypal_address',
                    'enable_paypal', 'suppress_emails', 'is_staff', 'alleged_organization'],
            'd' : True,
        },
        'UserOrgRole' : {
            'c' : True,
            'r' : ['owner', 'organization', 'organization_name', 'role', 'role_name', 'parent', 'children'],
            'u' : ['owner', 'organization', 'role', 'parent'],
            'd' : True,
        },
        'Venue' : {
            'c' : True,
            'r' : ['contact', 'region', 'address', 'owner', 'phone',
                      'name', 'events', 'rooms', 'hours_of_operation'],
            'u' : ['contact', 'region', 'address', 'owner', 'phone', 'name', 'events', 'hours_of_operation'],
            'd' : True,
        },
        'Video' : {
            'c' : True,
            'r' : ['id', 'approved_categories', 'aspect_ratio', 'author',
                   'categories', 'category_relationships', 'create_timestamp',
                   'deleted', 'description',
                   'encoded_videos', 'is_ready', 'length', 'live', 'name', 'title', 'num_views', 'owner',
                   'photo_url', 'prerequisite_tasks', 'public', 'src_file_size',
                   'status', 'tags', 'users_who_watched',
                   'version_id', 'version_label', 'version_comment',],
            'u' : ['aspect_ratio', 'author', 'categories', 'description',
                   'encoded_videos', 'length', 'live', 'name', 'title', 'owner',
                   'photo_url', 'prerequisite_tasks', 'public',
                   'tags', 'version_id', 'version_label', 'version_comment',],
            'd' : True,
        },
        'VideoCategory' : {
            'c' : True,
            'r' : ['status', 'category', 'category_name', 'video'],
            'u' : ['status'],
            'd' : True,
        },
        'VideoSession' : {
            'c' : True,
            'r' : ['assignment', 'date_started', 'date_completed', 'user', 'video'],
            'u' : ['date_started', 'date_completed'],
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
