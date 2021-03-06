"""
Exceptions for Power Reg
"""
__docformat__ = "restructuredtext en"

# Python
import copy

# Django
from django.conf import settings

class PrException(Exception):
    """
    Power Reg 2 Exception
    """

    #: error code
    error_code = 1
    #: error message
    error_msg = u'unknown error'
    #: dictionary of details for the error
    details = {}

    def __new__(cls, *args, **kwds):
        instance = super(PrException, cls).__new__(cls, *args, **kwds)
        # Explicitly copy class attributes to instance attributes.
        for attr in ('error_code', 'error_msg', 'details'):
            setattr(instance, attr, copy.copy(getattr(cls, attr)))
        return instance

    def get_error_code(self):
        """
        Returns the exception's error code.

        :rtype: int
        """
        return self.error_code

    def get_error_msg(self):
        """
        Returns a suitable error message.

        :rtype: string
        """
        return self.error_msg

    def get_details(self):
        """
        Returns a dictionary containing additional information about the exception.

        :rtype: dict
        """
        return self.details

    def __str__(self):
        s = u'error %d: %s' % (self.error_code, self.error_msg)
        if len(self.details) != 0:
            s += u', details=[%s]' % (self.details)
        return s

    __unicode__ = __str__

class NotImplementedException(PrException):
    """
    not implemented
    """

    error_code = 2
    error_msg = "not implemented"

class FieldNameNotFoundException(PrException):
    """
    field name not recognized
    """

    error_code = 4
    error_msg = "field name not recognized"

    def __init__(self, explanation=''):
        if explanation != '':
            self.error_msg += ": %s" % (explanation)

class OperationNotPermittedException(PrException):
    """
    operation not permitted

    This should be thrown for things like trying
    to set fields that are not settable.

    The permission denied exception is for operations
    that could be allowed, given a user with
    enough privileges.
    """

    error_code = 5
    error_msg = "operation not permitted"

    def __init__(self, explanation=''):
        if explanation != '':
            self.error_msg += ": %s" % (explanation)

class DatetimeConversionError(PrException):
    """
    datetime conversion error
    """

    error_code = 12
    error_msg = "error converting ISO8601 string"

class AuthenticationFailureException(PrException):
    """
    failed authentication
    """

    error_code = 17
    error_msg = "authentication failed"

class CannotChangePkException(PrException):
    """
    cannot change a primary key
    """

    error_code = 19
    error_msg = "cannot change a primary key"

class PermissionDeniedException(PrException):
    """
    permission denied
    """

    error_code = 23
    error_msg = "permission denied"

    def __init__(self, denied_attribute='', denied_model=''):
        if denied_attribute != '':
            self.error_msg = 'permission denied for the "%s" attribute' % \
                (denied_attribute)
        if denied_model != '':
            self.error_msg += ' on the %s model' % (denied_model)

class DuplicateTokenGeneratedException(PrException):
    """
    duplicate token generated by a random number generator
    Trying the invoked operation again would be a sensible response here,
    preferably notifying the system administrator(s) of the failure.
    """

    error_code = 30
    error_msg = "generated unexpectedly duplicate session id!"

class CannotModifyBlameException(PrException):
    """
    cannot modify blame
    """

    error_code = 36
    error_msg = "cannot modify blame"

class CannotViewBlameException(PrException):
    """
    cannot view blame
    """

    error_code = 37
    error_msg = "cannot view blame"

class ForeignObjectNotFoundException(PrException):
    """
    foreign_object not found
    """

    error_code = 38
    error_msg = "foreign object not found"

    def __init__(self, error_msg=None):
        if error_msg is not None:
            self.error_msg += ': %s' % (error_msg)

class RangeTakesTwoArgsException(PrException):
    """
    range takes two arguments
    """

    error_code = 39
    error_msg = "range expression takes two arguments of the same type in" + \
        " an array"

class InternalErrorException(PrException):
    """
    internal error

    The system has reached an unacceptable state outside of its design
    parameters if this exception is raised -- it's like an assertion error.
    It can be initialized with a textual description of the condition.
    """

    error_code = 46
    error_msg = "internal error"

    def __init__(self, description=""):
        if description:
            self.error_msg += ': %s' % (description)

class AuthTokenExpiredException(PrException):
    """
    auth token has expired - needs to be renewed
    """

    error_code = 49
    error_msg = "the authentication token has expired"

class InvalidFilterOperatorException(PrException):
    """
    invalid filter operator
    """

    error_code = 53
    error_msg = "invalid filter operator"

    def __init__(self, operator):
        self.error_msg += ': %s' % (operator)

class UploadUserMismatchException(PrException):
    """
    upload user mismatch

    This exception is raised when one user uploads a CSV file, and another user
    tries to call the import_manager to import that file.
    """

    error_code = 54
    error_msg = "you are not the uploading user"

class InvalidDataException(PrException):
    """
    invalid data
    """

    error_code = 56
    error_msg = "invalid data"

    def __init__(self, message):
        self.error_msg += ": %s" % (message)

class TrainingVoucherAlreadyUsedException(PrException):
    """
    training_voucher is already in use
    """

    error_code = 60
    error_msg = "training voucher has already been used"

class RefundOverflowException(PrException):
    """
    refund overflow
    """

    error_code = 61
    error_msg = "the sum of refunds for a payment may not exceed the " + \
        "payment's original amount"

class InvalidAmountException(PrException):
    """
    invalid amount
    """

    error_code = 62
    error_msg = "the amount must be represented as cents with only digits"

class NotQualifiedException(PrException):
    """
    not qualified
    """

    error_code = 76
    error_msg = "missing qualification"

    def __init__(self, qualification):
        self.error_msg += ': %s' % (qualification)

class NotPaidException(PrException):
    """
    not paid
    """

    error_code = 78
    error_msg = "purchase order or item has not been paid for"

class AttributeNotFoundException(PrException):
    """
    attribute not found
    """

    error_code = 79
    error_msg = "attribute not found"

    def __init__(self, attribute_name):
        self.error_msg = "attribute '%s' not found" % (attribute_name)

class InvalidUsageException(PrException):
    """
    invalid usage
    """

    error_code = 80
    error_msg = "invalid usage"

    def __init__(self, explanation):
        self.error_msg += ': %s' % (explanation)

class SessionNotConfirmedException(PrException):
    """
    session not confirmed
    """

    error_code = 83
    error_msg = "session not confirmed"

class InvalidStartingStatusException(PrException):
    """
    invalid starting status
    """

    error_code = 84
    error_msg = "invalid starting status"

class InvalidEndingStatusException(PrException):
    """
    invalid ending status
    """

    error_code = 85
    error_msg = "invalid ending status"

class NoMoreCapacityException(PrException):
    """
    no more capacity
    """

    error_code = 87
    error_msg = "no more capacity"

class UnableToConnectToMTAException(PrException):
    """
    unable to connect to the MTA
    """

    error_code = 88
    error_msg = "Powerreg was unable to connect to the MTA"

class PurchaseOrderAlreadyPaidException(PrException):
    """
    purchase order already paid for
    """

    error_code = 92
    error_msg = "the purchase order has already been paid"

class InvalidImageUploadException(PrException):
    """
    invalid image has been uploaded
    """

    error_code = 94
    error_msg = "Unable to parse uploaded image, or image format is" + \
        " unrecognized"

class GetterNotFoundException(PrException):
    """
    getter not found
    """

    error_code = 96
    error_msg = "getter not found"

    def __init__(self, getter_name='(unknown)'):
        self.error_msg += ': %s' % (getter_name)

class ObjectNotFoundException(PrException):
    """
    object not found
    """

    error_code = 97
    error_msg = "object not found"

    def __init__(self, type_name='(unknown)', primary_key=None):
        self.error_msg = "object of type %s and id %s not found" % \
            (type_name, str(primary_key))
        self.details = {'type_name': type_name, 'primary_key': primary_key}

class SetterNotFoundException(PrException):
    """
    setter not found
    """

    error_code = 98
    error_msg = "setter not found"

    def __init__(self, setter_name='(unknown)'):
        self.error_msg += ': %s' % (setter_name)

class InvalidActeeTypeException(PrException):
    """
    a method has been passed an object to be acted on with an
    incorrect type
    """

    error_code = 100
    error_msg = "an invalid actee type has been passed to a security check, a getter function, or a setter function"

class ModelNotSpecifiedException(PrException):
    """
    model not specified
    """

    error_code = 101
    error_msg = "model not specified"

class InvalidReportTypeException(PrException):
    """
    invalid report type
    """

    error_code = 102
    error_msg = "invalid report type"

    def __init__(self, attempted_report_type):
        self.error_msg = '%s is not a valid report type, try one of these: %s' % \
               (attempted_report_type, settings.PENTAHO_REPORTS.keys())

class RequiredReportParameterMissingException(PrException):
    """
    required report parameter missing
    """

    error_code = 103
    error_msg = "required report parameter missing"

    def __init__(self, missing_parameter):
        self.error_msg += ': %s' % (missing_parameter)

class UnableToConnectToReportingServerException(PrException):
    """
    unable to connect to reporting server
    """

    error_code = 104
    error_msg = 'unable to connect to reporting server.'

class UserInactiveException(PrException):
    """
    user is inactive
    """

    error_code = 107
    error_msg = "user is inactive"

    def __init__(self, username=u'', domain=u''):
        self.error_msg = u"The user %s (domain '%s') is inactive." % \
            (username, domain)

class CascadingDeleteException(PrException):
    """
    a cascading deletion has been prevented
    """

    error_code = 108
    error_msg = "a cascading delete has been prevented"

    def __init__(self, msg, protected_objects):
        """
        this is like a django.db.models.ProtectedError (which it's reraised
        from) but styled as a PRException
        """
        self.error_msg = msg
        self.details = { 'protected_objects' : protected_objects }

class EventStatusUnknownException(PrException):
    """
    event status could not be derived
    """

    error_code = 109
    error_msg = "Event status could not be derived"

class AlreadyEnrolledException(PrException):
    """
    already enrolled
    """

    error_code = 110
    error_msg = "User is already enrolled."

    def __init__(self, username):
        self.error_msg = "User %s is already enrolled." % (username)

class AsciiConversionFailedException(PrException):
    """
    A conversion to ASCII failed, probably due to something like a Han
    character.  This gets thrown by the Utils.asciify() method if
    it produces an ASCII string that has fewer characters than its
    input.
    """

    error_code = 111
    error_msg = u"Failed conversion to ASCII"

    def __init__(self, unicode_str, ascii_str):
        self.error_msg += u': [%s] -> [%s]' % (unicode_str, ascii_str)
        self.details = {'unicode_str': unicode_str, 'ascii_str': ascii_str}

class UnableToSendEmailReportException(PrException):
    """
    unable to send email report
    """

    error_code = 112
    error_msg = "unable to send email report"

    def __init__(self, pentaho_result=''):
        if pentaho_result:
            self.error_msg += ', result from Pentaho was [%s]' % (pentaho_result)
            self.details = {'pentaho_result': pentaho_result}

class XMLReportFailedException(PrException):
    """
    XML report failed
    """

    error_code = 113
    error_msg = "unable to fetch XML report"

    def __init__(self, pentaho_result=''):
        if pentaho_result:
            self.error_msg += ', result from Pentaho was [%s]' % (pentaho_result)
            self.details = {'pentaho_result' : pentaho_result}

class UserSuspendedException(PrException):
    """
    user is suspended
    """

    error_code = 114
    error_msg = u"The user is suspended."

    def __init__(self, username='', domain=u''):
        self.error_msg = u"The user %s (domain '%s') is suspended." % \
            (username, domain)

class AuthenticationErrorException(PrException):
    """
    there was an error during authentication
    """

    error_code = 115
    error_msg = "There was an error during authentication."

class CannotChangeForeignPasswordException(PrException):
    """
    cannot change the password on a foreign authentication system
    """

    error_code = 116
    error_msg = "Cannot change the password on a foreign authentication system."

class AttributeNotUpdatedException(PrException):
    """
    An ac_check_method was run to check whether a user was updating an attribute
    that isn't in the update_dict, or if it is, it will not cause any change to the actee.
    """

    error_code = 117
    error_msg = "Update dict does not modify the attribute in question on the actee."

class InvalidSessionEvaluationCodeException(PrException):
    """
    session evaluation code is not valid
    """

    error_code = 118
    error_msg = "Session evaluation code is not valid"

class UnsupportedScormVersionException(PrException):
    """
    The SCORM archive being examined is for an unsupported version of SCORM.
    """

    error_code = 119
    error_msg = "The SCORM package is for an unsupported version of SCORM"

    def __init__(self, unsupported_version):
        self.error_msg += " (%s). Please use SCORM v1.2." % unsupported_version

class ArchiveMissingFileException(PrException):
    """
    The SCORM archive being examined does not contain all of the files in its manifest.
    """

    error_code = 120
    error_msg = "The SCORM package is missing a file from its manifest"

    def __init__(self, missing_file_name):
        self.error_msg += ': %s' % missing_file_name

class ValidationException(PrException):
    """
    a validation error occurred
    """

    error_code = 121
    error_msg = u"A validation error occurred"

    def __init__(self, model_data_validation_error=None):
        """
        :param model_data_validation_error: the ModelDataValidationError that occurred
        """
        self.error_msg += u": %s" % unicode(model_data_validation_error)
        self.details = { 'messages': model_data_validation_error.validation_errors if model_data_validation_error is not None else ''}

class ImportException(PrException):
    """
    an import error occurred
    """

    error_code = 122
    error_msg = u"An import error occurred"

    def __init__(self, messages=None):
        """
        :param messages:  dictionary of other exception messages that were
                          encountered while importing, indexed by line number
                          in the import file.
        """
        self.details = { 'messages' : messages } if messages else {}

class InvalidFilterException(PrException):
    """
    An invalid filter structure was passed to the object
    manager's get_filtered() method.  This could occur if the
    filter dictionary had a boolean operator key that was not its
    only key.
    """

    error_code = 123
    error_msg = u"invalid filter"

    def __init__(self, filter_dict, reason):
        self.error_msg += u" [%s]" % (unicode(filter_dict))
        if reason:
            self.error_msg += u': %s' % (reason)
        self.details = {'filter_dict': filter_dict, 'reason': reason}

class InvalidInputException(PrException):
    """
    a function has received invalid input
    """

    error_code = 124
    error_msg = u"function received invalid input"

    def __init__(self, messages=None):
        self.details = { 'messages' : messages } if messages else {}

class PasswordPolicyViolation(PrException):

    error_code = 126
    error_msg = u"password policy violation"

    def __init__(self, messages=None):
        self.details = { 'messages' : messages } if messages else {}

class DuplicateAssignmentException(PrException):
    """
    an assignment already exists for this user and task
    """

    error_code = 127
    error_msg = "assignment already exists for this user and task"

    def __init__(self, new_assignment=None):
        if new_assignment is not None:
            self.new_assignment = new_assignment

class NotLoggedInException(PrException):

    error_code = 128
    error_msg = u"not logged in"

class UserConfirmationException(PrException):
    """
    user has not confirmed their email address
    """

    error_code = 129
    error_msg = u"user has not confirmed their email address."

    def __init__(self, username='', domain=u'', msg=None):
        if msg is None:
            self.error_msg = u"user %s (domain '%s') has not confirmed their email address." % \
                (username, domain)
        else:
            self.error_msg = msg

class VideoMustHaveCategory(PrException):
    """Video being uploaded has not been assigned to any categories"""
    error_code = 130
    error_msg = u"Video being uploaded has not been assigned to any categories"

# vim:tabstop=4 shiftwidth=4 expandtab
