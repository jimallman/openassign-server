# Exposes models managers and subsystems in a way extendable by plugins and
# variants
from utils import LazyImporter, LazyImportObjectProxy

__all__ = ['managers', 'subsystems', 'models']

# LazyImporter subclasses to name the facade type (helps with debugging)
class SubsystemsFacade(LazyImporter):
    pass

class ManagersFacade(LazyImporter):
    pass

class ModelsFacade(LazyImporter):
    pass

# On with the imports! (but later because these are all lazy object proxies)
subsystems = SubsystemsFacade()
subsystems.add_import('Authorizer', 'pr_services.authorizer')
subsystems.add_import('Getter', 'pr_services.gettersetter')
subsystems.add_import('InitialSetupMachine', 'pr_services.initial_setup')
subsystems.add_import('Logger', 'pr_services.logger')
subsystems.add_import('ScormServer', 'pr_services.scorm_system.scorm_server')
subsystems.add_import('Setter', 'pr_services.gettersetter')
subsystems.add_import('TableData', 'pr_services.utils')
subsystems.add_import('Utils', 'pr_services.utils')

managers = ManagersFacade()
managers.add_import('AchievementManager', 'pr_services.credential_system.achievement_manager')
managers.add_import('AnswerManager', 'pr_services.exam_system.answer_manager')
managers.add_import('AssignmentAttemptManager', 'pr_services.credential_system.assignment_attempt_manager')
managers.add_import('AssignmentManager', 'pr_services.credential_system.assignment_manager')
managers.add_import('BackendInfo', 'pr_services.backend_info')
managers.add_import('BlameManager', 'pr_services.blame_manager')
managers.add_import('ConditionTestCollectionManager', 'pr_services.condition_test_collection_manager')
managers.add_import('ConditionTestManager', 'pr_services.condition_test_manager')
managers.add_import('CredentialManager', 'pr_services.credential_system.credential_manager')
managers.add_import('CredentialTypeManager', 'pr_services.credential_system.credential_type_manager')
managers.add_import('CurriculumEnrollmentManager', 'pr_services.credential_system.curriculum_enrollment_manager')
managers.add_import('CurriculumManager', 'pr_services.credential_system.curriculum_manager')
managers.add_import('CurriculumTaskAssociationManager', 'pr_services.credential_system.curriculum_task_association_manager')
managers.add_import('CustomActionManager', 'pr_services.custom_action_manager')
managers.add_import('DBSettingManager', 'pr_services.dbsettings')
managers.add_import('DomainAffiliationManager', 'pr_services.user_system.domain_affiliation_manager')
managers.add_import('DomainManager', 'pr_services.user_system.domain_manager')
managers.add_import('EventManager', 'pr_services.event_system.event_manager')
managers.add_import('EventTemplateManager', 'pr_services.event_system.event_template_manager')
managers.add_import('ExamManager', 'pr_services.exam_system.exam_manager')
managers.add_import('ExamSessionManager', 'pr_services.exam_system.exam_session_manager')
managers.add_import('FormPageManager', 'pr_services.exam_system.form_page_manager')
managers.add_import('FormWidgetManager', 'pr_services.exam_system.form_widget_manager')
managers.add_import('GroupManager', 'pr_services.user_system.group_manager')
managers.add_import('ImportManager', 'pr_services.import_manager')
managers.add_import('LogManager', 'pr_services.log_manager')
managers.add_import('NoteManager', 'pr_services.note_manager')
managers.add_import('OrganizationManager', 'pr_services.user_system.organization_manager')
managers.add_import('OrgEmailDomainManager', 'pr_services.user_system.organization_email_domain_manager')
managers.add_import('OrgRoleManager', 'pr_services.user_system.organization_role_manager')
managers.add_import('PaymentManager', 'pr_services.product_system.payment_manager')
managers.add_import('ProductClaimManager', 'pr_services.product_system.product_claim_manager')
managers.add_import('ProductDiscountManager', 'pr_services.product_system.product_discount_manager')
managers.add_import('ProductLineManager', 'pr_services.product_system.product_line_manager')
managers.add_import('ProductManager', 'pr_services.product_system.product_manager')
managers.add_import('ProductOfferManager', 'pr_services.product_system.product_offer_manager')
managers.add_import('PurchaseOrderManager', 'pr_services.product_system.purchase_order_manager')
managers.add_import('QuestionManager', 'pr_services.exam_system.question_manager')
managers.add_import('QuestionPoolManager', 'pr_services.exam_system.question_pool_manager')
managers.add_import('RegionManager', 'pr_services.resource_system.region_manager')
managers.add_import('ResourceManager', 'pr_services.resource_system.resource_manager')
managers.add_import('ResourceTypeManager', 'pr_services.resource_system.resource_type_manager')
managers.add_import('ResponseManager', 'pr_services.exam_system.response_manager')
managers.add_import('RoleManager', 'pr_services.role_manager')
managers.add_import('RoomManager', 'pr_services.resource_system.room_manager')
managers.add_import('ScoManager', 'pr_services.scorm_system.sco_manager')
managers.add_import('ScoSessionManager', 'pr_services.scorm_system.sco_session_manager')
managers.add_import('SessionManager', 'pr_services.event_system.session_manager')
managers.add_import('SessionResourceTypeRequirementManager', 'pr_services.event_system.session_resource_type_requirement_manager')
managers.add_import('SessionTemplateManager', 'pr_services.event_system.session_template_manager')
managers.add_import('SessionTemplateResourceTypeRequirementManager', 'pr_services.event_system.session_template_resource_type_requirement_manager')
managers.add_import('SessionTemplateUserRoleRequirementManager', 'pr_services.event_system.session_template_user_role_requirement_manager')
managers.add_import('SessionUserRoleManager', 'pr_services.event_system.session_user_role_manager')
managers.add_import('SessionUserRoleRequirementManager', 'pr_services.event_system.session_user_role_requirement_manager')
managers.add_import('TaskBundleManager', 'pr_services.credential_system.task_bundle_manager')
managers.add_import('TaskFeeManager', 'pr_services.event_system.task_fee_manager')
managers.add_import('TaskManager', 'pr_services.credential_system.task_manager')
managers.add_import('TrainingUnitAccountManager', 'pr_services.product_system.training_unit_account_manager')
managers.add_import('TrainingUnitAuthorizationManager', 'pr_services.product_system.training_unit_authorization_manager')
managers.add_import('TrainingUnitTransactionManager', 'pr_services.product_system.training_unit_transaction_manager')
managers.add_import('TrainingVoucherManager', 'pr_services.product_system.training_voucher_manager')
managers.add_import('UserManager', 'pr_services.user_system.user_manager')
managers.add_import('UserOrgRoleManager', 'pr_services.user_system.user_organization_role_manager')
managers.add_import('VenueManager', 'pr_services.resource_system.venue_manager')
managers.add_import('UtilsManager', 'pr_services.utils_manager')

models = ModelsFacade()
models.add_import('ACCheckMethod', 'pr_services.models')
models.add_import('Achievement', 'pr_services.models')
models.add_import('AchievementAward', 'pr_services.models')
models.add_import('ACL', 'pr_services.models')
models.add_import('ACMethodCall', 'pr_services.models')
models.add_import('Address', 'pr_services.models')
models.add_import('Answer', 'pr_services.models')
models.add_import('AssignmentAttempt', 'pr_services.models')
models.add_import('Assignment', 'pr_services.models')
models.add_import('AuthToken', 'pr_services.models')
models.add_import('AuthTokenVoucher', 'pr_services.models')
models.add_import('Blame', 'pr_services.models')
models.add_import('CachedCookie', 'pr_services.models')
models.add_import('ClaimProductOffers', 'pr_services.models')
models.add_import('ConditionTestCollection', 'pr_services.models')
models.add_import('ConditionTest', 'pr_services.models')
models.add_import('Course', 'pr_services.models')
models.add_import('Credential', 'pr_services.models')
models.add_import('CredentialType', 'pr_services.models')
models.add_import('CSVData', 'pr_services.models')
models.add_import('CurriculumEnrollment', 'pr_services.models')
models.add_import('CurriculumEnrollmentUserAssociation', 'pr_services.models')
models.add_import('Curriculum', 'pr_services.models')
models.add_import('CurriculumTaskAssociation', 'pr_services.models')
models.add_import('CustomAction', 'pr_services.models')
models.add_import('DomainAffiliation', 'pr_services.models')
models.add_import('Domain', 'pr_services.models')
models.add_import('Event', 'pr_services.models')
models.add_import('EventTemplate', 'pr_services.models')
models.add_import('Exam', 'pr_services.models')
models.add_import('ExamSession', 'pr_services.models')
models.add_import('FormPage', 'pr_services.models')
models.add_import('FormWidget', 'pr_services.models')
models.add_import('Group', 'pr_services.models')
models.add_import('ModelDataValidationError', 'pr_services.models')
models.add_import('Note', 'pr_services.models')
models.add_import('Organization', 'pr_services.models')
models.add_import('OrgEmailDomain', 'pr_services.models')
models.add_import('OrgRole', 'pr_services.models')
models.add_import('Payment', 'pr_services.models')
models.add_import('ProductClaim', 'pr_services.models')
models.add_import('ProductDiscount', 'pr_services.models')
models.add_import('ProductLine', 'pr_services.models')
models.add_import('ProductOffer', 'pr_services.models')
models.add_import('Product', 'pr_services.models')
models.add_import('ProductTransaction', 'pr_services.models')
models.add_import('PurchaseOrder', 'pr_services.models')
models.add_import('QuestionPool', 'pr_services.models')
models.add_import('Question', 'pr_services.models')
models.add_import('Refund', 'pr_services.models')
models.add_import('Region', 'pr_services.models')
models.add_import('Resource', 'pr_services.models')
models.add_import('ResourceType', 'pr_services.models')
models.add_import('Response', 'pr_services.models')
models.add_import('Role', 'pr_services.models')
models.add_import('Room', 'pr_services.models')
models.add_import('Sco', 'pr_services.models')
models.add_import('ScoSession', 'pr_services.models')
models.add_import('Session', 'pr_services.models')
models.add_import('SessionResourceTypeRequirement', 'pr_services.models')
models.add_import('SessionTemplate', 'pr_services.models')
models.add_import('SessionTemplateResourceTypeReq', 'pr_services.models')
models.add_import('SessionTemplateUserRoleReq', 'pr_services.models')
models.add_import('SessionUserRole', 'pr_services.models')
models.add_import('SessionUserRoleRequirement', 'pr_services.models')
models.add_import('SingleUseAuthToken', 'pr_services.models')
models.add_import('TaskBundle', 'pr_services.models')
models.add_import('TaskBundleTaskAssociation', 'pr_services.models')
models.add_import('TaskFee', 'pr_services.models')
models.add_import('Task', 'pr_services.models')
models.add_import('TrainingUnitAccount', 'pr_services.models')
models.add_import('TrainingUnitAuthorization', 'pr_services.models')
models.add_import('TrainingUnitTransaction', 'pr_services.models')
models.add_import('TrainingVoucher', 'pr_services.models')
models.add_import('User', 'pr_services.models')
models.add_import('UserOrgRole', 'pr_services.models')
models.add_import('Venue', 'pr_services.models')

# vim:tabstop=4 shiftwidth=4 expandtab
