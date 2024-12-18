"""
Django settings for observation_portal project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import sentry_sdk

from lcogt_logging import LCOGTFormatter


def get_list_from_env(variable, default=None):
    value_as_list = []
    value = os.getenv(variable, default)
    if value:
        value_as_list = value.strip(', ').replace(' ', '').split(',')
    return value_as_list


def get_dramqtiq_broker_url():
    url = os.getenv("DRAMATIQ_BROKER_URL", "redis://redis:6379/0")
    # return URL as is if it exists and not a empty string
    if url:
        return url

    # construct a URL for backwards-compatibility
    return "redis://%s:%s" % (
        os.getenv("DRAMATIQ_BROKER_HOST", "redis"),
        os.getenv("DRAMATIQ_BROKER_PORT", 6379)
    )


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', '2xou30pi2va&ed@n2l79n807k%@szj1+^uj&)y09_w62eji!m^')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', False)

ALLOWED_HOSTS = get_list_from_env('ALLOWED_HOSTS', '*')  # Comma delimited list of django allowed hosts

SITE_ID = 1
ACCOUNT_ACTIVATION_DAYS = 7

## Email template and project constants
ORGANIZATION_NAME = os.getenv('ORGANIZATION_NAME', '')  # Base organization name, used in email titles/signatures
ORGANIZATION_EMAIL = os.getenv('ORGANIZATION_EMAIL', '')  # Base organization from email for the obs portal for outgoing emails
ORGANIZATION_DDT_EMAIL = os.getenv('ORGANIZATION_DDT_EMAIL', '')  # Organization email to receive alerts when ddt proposals are submitted
ORGANIZATION_SUPPORT_EMAIL = os.getenv('ORGANIZATION_SUPPORT_EMAIL', '')  # Organization email to receive account removal email requests
ORGANIZATION_ADMIN_EMAIL = os.getenv('ORGANIZATION_ADMIN_EMAIL', '')  # Admin email address to receive 500 error emails
OBSERVATION_PORTAL_BASE_URL = os.getenv('OBSERVATION_PORTAL_BASE_URL', 'http://localhost')

OBSERVATORY_DIRECTOR_NAME = os.getenv('OBSERVATORY_DIRECTOR_NAME', 'Foo Bar')

ADMINS = []

if os.getenv("SEND_ORG_ADMIN_ERROR_EMAILS", "no").lower() in {"yes", "true", "y"}:
    ADMINS.append(("Admins", ORGANIZATION_ADMIN_EMAIL))

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',
    'registration',  # must come before admin to use custom templates
    'django.contrib.admin',
    'rest_framework',
    'django_filters',
    'rest_framework.authtoken',
    'bootstrap4',
    'oauth2_provider',
    'corsheaders',
    'django_extensions',
    'django_dramatiq',
    'health_check',
    'observation_portal.accounts.apps.AccountsConfig',
    'observation_portal.requestgroups.apps.RequestGroupsConfig',
    'observation_portal.observations.apps.ObservationsConfig',
    'observation_portal.proposals.apps.ProposalsConfig',
    'observation_portal.sciapplications.apps.SciapplicationsConfig',
]

MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'observation_portal.common.middleware.RequestLogMiddleware',
]

ROOT_URLCONF = 'observation_portal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'observation_portal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# https://www.postgresql.org/docs/9.6/runtime-config-client.html#GUC-IDLE-IN-TRANSACTION-SESSION-TIMEOUT
PORTAL_IDLE_IN_TRANSACTION_TIMEOUT = 60 * 60 * 1000  # 1 hour

DATABASES = {
   'default': {
       'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.postgresql'),
       'NAME': os.getenv('DB_NAME', 'observation_portal'),
       'USER': os.getenv('DB_USER', 'postgres'),
       'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
       'HOST': os.getenv('DB_HOST', '127.0.0.1'),
       'PORT': os.getenv('DB_PORT', '5432'),
       'OPTIONS': {
           'options': f'-c idle_in_transaction_session_timeout={PORTAL_IDLE_IN_TRANSACTION_TIMEOUT}'
       }
   }
}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

OAUTH2_PROVIDER_ACCESS_TOKEN_MODEL = 'oauth2_provider.AccessToken'
OAUTH2_PROVIDER_APPLICATION_MODEL = 'oauth2_provider.Application'
OAUTH2_PROVIDER_REFRESH_TOKEN_MODEL = 'oauth2_provider.RefreshToken'
OAUTH2_PROVIDER_ID_TOKEN_MODEL = 'oauth2_provider.IDToken'
MIGRATION_MODULES = {
    'oauth2_provider': 'observation_portal.accounts.oauth2_migrations'
}

CACHES = {
     'default': {
         'BACKEND': os.getenv('CACHE_BACKEND', 'django.core.cache.backends.locmem.LocMemCache'),
         'LOCATION': os.getenv('CACHE_LOCATION', 'unique-snowflake')
     },
     'locmem': {
         'BACKEND': os.getenv('LOCAL_CACHE_BACKEND', 'django.core.cache.backends.locmem.LocMemCache'),
         'LOCATION': 'locmem-cache'
     }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = [
    'observation_portal.accounts.backends.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend',
    'oauth2_provider.backends.OAuth2Backend',
]

OAUTH2_PROVIDER = {
    'ACCESS_TOKEN_EXPIRE_SECONDS': 86400 * 30 * 24,  # 2 years
    'REFRESH_TOKEN_EXPIRE_SECONDS': 86400 * 30 * 24  # 2 years
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_URLS_REGEX = r'^/(api|accounts|media)/.*$|^/o/.*'
CORS_ORIGIN_WHITELIST = get_list_from_env('CORS_ORIGIN_WHITELIST')
CSRF_TRUSTED_ORIGINS = get_list_from_env('CSRF_TRUSTED_ORIGINS')
LOGIN_REDIRECT_URL = '/accounts/loggedinstate/'
LOGOUT_REDIRECT_URL = '/'

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = False

USE_TZ = True

DATETIME_FORMAT = 'Y-m-d H:i:s'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME', 'observation-portal-test-bucket')
AWS_S3_REGION_NAME = os.getenv('AWS_REGION', 'us-west-2')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', None)
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', None)
AWS_IS_GZIPPED = True
AWS_LOCATION = os.getenv('MEDIAFILES_DIR', 'media')
AWS_DEFAULT_ACL = None
AWS_S3_SIGNATURE_VERSION = 's3v4'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_URL = os.getenv('STATIC_URL', '/static/')
STATIC_ROOT = os.getenv('STATIC_ROOT', '/static/')
STATICFILES_STORAGE = os.getenv('STATIC_STORAGE', 'django.contrib.staticfiles.storage.StaticFilesStorage')
MEDIAFILES_DIR = os.getenv('MEDIAFILES_DIR', 'media')
MEDIA_URL = '' if AWS_ACCESS_KEY_ID else '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
DEFAULT_FILE_STORAGE = os.getenv('MEDIA_STORAGE', 'django.core.files.storage.FileSystemStorage')

EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_USE_TLS = True
EMAIL_HOST = os.getenv('EMAIL_HOST', 'localhost')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
DEFAULT_FROM_EMAIL = ORGANIZATION_EMAIL
SERVER_EMAIL = ORGANIZATION_EMAIL

OPENSEARCH_URL = os.getenv('OPENSEARCH_URL', 'http://localhost')
CONFIGDB_URL = os.getenv('CONFIGDB_URL', 'http://localhost')
DOWNTIMEDB_URL = os.getenv('DOWNTIMEDB_URL', 'http://localhost')

# Real time session booking variables for availability
# Availability from (current time + minutes in) to (current time + minutes in + days out)
REAL_TIME_AVAILABILITY_DAYS_OUT = int(os.getenv('REAL_TIME_AVAILABILITY_DAYS_OUT', 7))
REAL_TIME_AVAILABILITY_MINUTES_IN = int(os.getenv('REAL_TIME_AVAILABILITY_MINUTES_IN', 60))

REQUESTGROUP_DATA_DOWNLOAD_URL = os.getenv('REQUESTGROUP_DATA_DOWNLOAD_URL', '')  # use {requestgroup_id} to have it substituted in
REQUEST_DETAIL_URL = os.getenv('REQUEST_DETAIL_URL', '')  # use {request_id} to have it substituted in
SCIENCE_APPLICATION_DETAIL_URL = os.getenv('SCIENCE_APPLICATION_DETAIL_URL', '')  # use {scicapp_id} to have it substituted in
MAX_FAILURES_PER_REQUEST = int(os.getenv('MAX_FAILURES_PER_REQUEST', 0))  # 0 means unlimited / no max
DITHER = {
    'custom_pattern_key': 'custom', # Key used to indicate a custom dither pattern was created
    'valid_expansion_patterns': ('line', 'grid', 'spiral', )
}
MOSAIC = {
    'custom_pattern_key': 'custom', # Key used to indicate a custom mosaic pattern was created
    'valid_expansion_patterns': ('line', 'grid', )
}

REST_FRAMEWORK = {
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.ScopedRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'requestgroups.cancel': os.getenv('REQUESTGROUPS_CANCEL_DEFAULT_THROTTLE', '2000/day'),
        'requestgroups.create': os.getenv('REQUESTGROUPS_CREATE_DEFAULT_THROTTLE', '5000/day'),
        'requestgroups.validate': os.getenv('REQUESTGROUPS_VALIDATE_DEFAULT_THROTTLE', '20000/day')
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            '()': LCOGTFormatter
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO'
        },
        'rise_set': {
            'level': 'WARNING'
        },
        'portal_request': {
            'level': 'INFO',
            'propogate': False
        }
    }
}

## Duration constants for calculating overheads
MAX_IPP_VALUE = float(os.getenv('MAX_IPP_VALUE', 2.0))  # the maximum allowed value of ipp
MIN_IPP_VALUE = float(os.getenv('MIN_IPP_VALUE', 0.5))  # the minimum allowed value of ipp
PROPOSAL_TIME_OVERUSE_ALLOWANCE = float(os.getenv('PROPOSAL_TIME_OVERUSE_ALLOWANCE', 1.1))  # amount of leeway in a proposals timeallocation before rejecting that request

## This is a list of base URLs for each OAuth Client application which we want this Oauth server
## to update the token of a user in when the token is revoked and created.
OAUTH_CLIENT_APPS_BASE_URLS = get_list_from_env('OAUTH_CLIENT_APPS_BASE_URLS', '')
## This key must match the key setup in the Oauth Client applications to authenticate this as the server
OAUTH_SERVER_KEY = os.getenv('OAUTH_SERVER_KEY', '')

## Serializer setup - used to allow overriding of serializers
SERIALIZERS = {
    'observations': {
        'Summary': os.getenv('OBSERVATIONS_SUMMARY_SERIALIZER', 'observation_portal.observations.serializers.SummarySerializer'),
        'ConfigurationStatus': os.getenv('OBSERVATIONS_CONFIGURATIONSTATUS_SERIALIZER', 'observation_portal.observations.serializers.ConfigurationStatusSerializer'),
        'Target': os.getenv('OBSERVATIONS_TARGET_SERIALIZER', 'observation_portal.observations.serializers.ObservationTargetSerializer'),
        'Configuration': os.getenv('OBSERVATIONS_CONFIGURATION_SERIALIZER', 'observation_portal.observations.serializers.ObservationConfigurationSerializer'),
        'Request': os.getenv('OBSERVATIONS_REQUEST_SERIALIZER', 'observation_portal.observations.serializers.ObserveRequestSerializer'),
        'RequestGroup': os.getenv('OBSERVATIONS_REQUESTGROUP_SERIALIZER', 'observation_portal.observations.serializers.ObserveRequestGroupSerializer'),
        'Schedule': os.getenv('OBSERVATIONS_SCHEDULE_SERIALIZER', 'observation_portal.observations.serializers.ScheduleSerializer'),
        'RealTime': os.getenv('OBSERVATIONS_REALTIME_SERIALIZER', 'observation_portal.observations.serializers.RealTimeSerializer'),
        'Observation': os.getenv('OBSERVATIONS_OBSERVATION_SERIALIZER', 'observation_portal.observations.serializers.ObservationSerializer'),
        'Cancel': os.getenv('OBSERVATIONS_CANCEL_SERIALIZER', 'observation_portal.observations.serializers.CancelObservationsSerializer'),
        'CancelResponse': os.getenv('OBSERVATIONS_CANCEL_RESPONSE_SERIALIZER', 'observation_portal.observations.serializers.CancelObservationsResponseSerializer'),
        'LastScheduled': os.getenv('OBSERVATIONS_LAST_SCHEDULED_SERIALIZER', 'observation_portal.observations.serializers.LastScheduledSerializer'),
        'ObservationFilters': os.getenv('OBSERVATIONS_OBSERVATIONFILTERS_SERIALIZER', 'observation_portal.observations.serializers.ObservationFiltersSerializer'),
    },
    'requestgroups': {
        'Cadence': os.getenv('REQUESTGROUPS_CADENCE_SERIALIZER', 'observation_portal.requestgroups.serializers.CadenceSerializer'),
        'CadenceRequest': os.getenv('REQUESTGROUPS_CADENCEREQUEST_SERIALIZER', 'observation_portal.requestgroups.serializers.CadenceRequestSerializer'),
        'CadenceRequestGroup': os.getenv('REQUESTGROUPS_CADENCEREQUESTGROUP_SERIALIZER', 'observation_portal.requestgroups.serializers.CadenceRequestGroupSerializer'),
        'Constraints': os.getenv('REQUESTGROUPS_CONSTRAINTS_SERIALIZER', 'observation_portal.requestgroups.serializers.ConstraintsSerializer'),
        'RegionOfInterest': os.getenv('REQUESTGROUPS_REGIONOFINTEREST_SERIALIZER', 'observation_portal.requestgroups.serializers.RegionOfInterestSerializer'),
        'InstrumentConfig': os.getenv('REQUESTGROUPS_INSTRUMENTCONFIG_SERIALIZER', 'observation_portal.requestgroups.serializers.InstrumentConfigSerializer'),
        'AcquisitionConfig': os.getenv('REQUESTGROUPS_ACQUISITIONCONFIG_SERIALIZER', 'observation_portal.requestgroups.serializers.AcquisitionConfigSerializer'),
        'GuidingConfig': os.getenv('REQUESTGROUPS_GUIDINGCONFIG_SERIALIZER', 'observation_portal.requestgroups.serializers.GuidingConfigSerializer'),
        'Target': os.getenv('REQUESTGROUPS_TARGET_SERIALIZER', 'observation_portal.requestgroups.serializers.TargetSerializer'),
        'Configuration': os.getenv('REQUESTGROUPS_CONFIGURATION_SERIALIZER', 'observation_portal.requestgroups.serializers.ConfigurationSerializer'),
        'Location': os.getenv('REQUESTGROUPS_LOCATION_SERIALIZER', 'observation_portal.requestgroups.serializers.LocationSerializer'),
        'Window': os.getenv('REQUESTGROUPS_WINDOW_SERIALIZER', 'observation_portal.requestgroups.serializers.WindowSerializer'),
        'Request': os.getenv('REQUESTGROUPS_REQUEST_SERIALIZER', 'observation_portal.requestgroups.serializers.RequestSerializer'),
        'RequestGroup': os.getenv('REQUESTGROUPS_REQUESTGROUP_SERIALIZER', 'observation_portal.requestgroups.serializers.RequestGroupSerializer'),
        'DraftRequestGroup': os.getenv('REQUESTGROUPS_DRAFTREQUESTGROUP_SERIALIZER', 'observation_portal.requestgroups.serializers.DraftRequestGroupSerializer'),
        'Mosaic': os.getenv('REQUESTGROUPS_MOSAIC_SERIALIZER', 'observation_portal.requestgroups.serializers.MosaicSerializer'),
        'Dither': os.getenv('REQUESTGROUPS_DITHER_SERIALIZER', 'observation_portal.requestgroups.serializers.DitherSerializer'),
        'LastChanged': os.getenv('REQUESTGROUPS_LAST_CHANGED_SERIALIZER', 'observation_portal.requestgroups.serializers.LastChangedSerializer'),
    },
    'proposals': {
        'Proposal': os.getenv('PROPOSALS_PROPOSAL_SERIALIZER', 'observation_portal.proposals.serializers.ProposalSerializer'),
        'ProposalInvite': os.getenv('PROPOSALS_PROPOSALINVITE_SERIALIZER', 'observation_portal.proposals.serializers.ProposalInviteSerializer'),
        'ProposalInviteResponse': os.getenv('PROPOSALS_PROPOSALINVITE_RESPONSE_SERIALIZER', 'observation_portal.proposals.serializers.ProposalInviteResponseSerializer'),
        'Semester': os.getenv('PROPOSALS_SEMESTER_SERIALIZER', 'observation_portal.proposals.serializers.SemesterSerializer'),
        'Membership': os.getenv('PROPOSALS_MEMBERSHIP_SERIALIZER', 'observation_portal.proposals.serializers.MembershipSerializer'),
        'ProposalNotification': os.getenv('PROPOSALS_PROPOSALNOTIFICATION_SERIALIZER', 'observation_portal.proposals.serializers.ProposalNotificationSerializer'),
        'ProposalNotificationResponse': os.getenv('PROPOSALS_PROPOSALNOTIFICATION_RESPONSE_SERIALIZER', 'observation_portal.proposals.serializers.ProposalNotificationResponseSerializer'),
        'TimeLimit': os.getenv('PROPOSALS_TIMELIMIT_SERIALIZER', 'observation_portal.proposals.serializers.TimeLimitSerializer'),
        'TimeLimitResponse': os.getenv('PROPOSALS_TIMELIMIT_RESPONSE_SERIALIZER', 'observation_portal.proposals.serializers.TimeLimitResponseSerializer'),
        'TimeAllocation': os.getenv('PROPOSALS_TIMEALLOCATION_SERIALIZER', 'observation_portal.proposals.serializers.TimeAllocationSerializer'),
    },
    'accounts': {
        'Profile': os.getenv('ACCOUNTS_PROFILE_SERIALIZER', 'observation_portal.accounts.serializers.ProfileSerializer'),
        'User': os.getenv('ACCOUNTS_USER_SERIALIZER', 'observation_portal.accounts.serializers.UserSerializer'),
        'AccountRemovalRequest': os.getenv('ACCOUNTS_ACCOUNTREMOVAL_SERIALIZER', 'observation_portal.accounts.serializers.AccountRemovalRequestSerializer'),
        'AcceptTerms': os.getenv('ACCOUNTS_ACCEPTTERMS_SERIALIZER', 'observation_portal.accounts.serializers.AcceptTermsResponseSerializer'),
        'RevokeToken': os.getenv('ACCOUNTS_REVOKETOKEN_SERIALIZER', 'observation_portal.accounts.serializers.RevokeTokenResponseSerializer'),
        'AccountRemovalResponse': os.getenv('ACCOUNTS_ACCOUNTREMOVAL_RESPONSE_SERIALIZER', 'observation_portal.accounts.serializers.AccountRemovalResponseSerializer'),
        'CreateUserSerializer': os.getenv('ACCOUNTS_CREATEUSER_SERIALIZER', 'observation_portal.accounts.serializers.CreateUserSerializer'),
        'BulkCreateUsersSerializer': os.getenv('ACCOUNTS_BULKCREATEUSERS_SERIALIZER', 'observation_portal.accounts.serializers.BulkCreateUsersSerializer'),
    },
    'sciapplications': {
        'Call': os.getenv('SCIAPPLICATIONS_CALL_SERIALIZER', 'observation_portal.sciapplications.serializers.CallSerializer'),
        'ScienceApplication': os.getenv('SCIAPPLICATIONS_SCIENCEAPPLICATION_SERIALIZER', 'observation_portal.sciapplications.serializers.ScienceApplicationSerializer'),
    }
}

## model as_dict overrides - used to add or remove data from the detail and list viewsets.
#  The method must take in the model instance as the first argument. It may take other kwargs as additional arguments, but these are not used for basic list/detail views.
AS_DICT = {
    'observations': {
        'Summary': os.getenv('OBSERVATIONS_SUMMARY_AS_DICT', 'observation_portal.observations.models.summary_as_dict'),
        'ConfigurationStatus': os.getenv('OBSERVATIONS_CONFIGURATIONSTATUS_AS_DICT', 'observation_portal.observations.models.configurationstatus_as_dict'),
        'Observation': os.getenv('OBSERVATIONS_OBSERVATION_AS_DICT', 'observation_portal.observations.models.observation_as_dict'),
    },
    'requestgroups': {
        'Constraints': os.getenv('REQUESTGROUPS_CONSTRAINTS_AS_DICT', 'observation_portal.requestgroups.models.constraints_as_dict'),
        'RegionOfInterest': os.getenv('REQUESTGROUPS_REGIONOFINTEREST_AS_DICT', 'observation_portal.requestgroups.models.regionofinterest_as_dict'),
        'InstrumentConfig': os.getenv('REQUESTGROUPS_INSTRUMENTCONFIG_AS_DICT', 'observation_portal.requestgroups.models.instrumentconfig_as_dict'),
        'AcquisitionConfig': os.getenv('REQUESTGROUPS_ACQUISITIONCONFIG_AS_DICT', 'observation_portal.requestgroups.models.acquisitionconfig_as_dict'),
        'GuidingConfig': os.getenv('REQUESTGROUPS_GUIDINGCONFIG_AS_DICT', 'observation_portal.requestgroups.models.guidingconfig_as_dict'),
        'Target': os.getenv('REQUESTGROUPS_TARGET_AS_DICT', 'observation_portal.requestgroups.models.target_as_dict'),
        'Configuration': os.getenv('REQUESTGROUPS_CONFIGURATION_AS_DICT', 'observation_portal.requestgroups.models.configuration_as_dict'),
        'Location': os.getenv('REQUESTGROUPS_LOCATION_AS_DICT', 'observation_portal.requestgroups.models.location_as_dict'),
        'Window': os.getenv('REQUESTGROUPS_WINDOW_AS_DICT', 'observation_portal.requestgroups.models.window_as_dict'),
        'Request': os.getenv('REQUESTGROUPS_REQUEST_AS_DICT', 'observation_portal.requestgroups.models.request_as_dict'),
        'RequestGroup': os.getenv('REQUESTGROUPS_REQUESTGROUP_AS_DICT', 'observation_portal.requestgroups.models.requestgroup_as_dict'),
    },
    'proposals': {
        'Proposal': os.getenv('PROPOSALS_PROPOSAL_AS_DICT', 'observation_portal.proposals.models.proposal_as_dict'),
        'Membership': os.getenv('PROPOSALS_MEMBERSHIP_AS_DICT', 'observation_portal.proposals.models.membership_as_dict'),
        'TimeAllocation': os.getenv('PROPOSALS_TIMEALLOCATION_AS_DICT', 'observation_portal.proposals.models.timeallocation_as_dict'),
    }
}

# Overrides for Duration calculation functions
DURATION = {
    'instrument_configuration_duration_per_exposure': os.getenv('INSTRUMENT_CONFIGURATION_PER_EXPOSURE_DURATION', 'observation_portal.requestgroups.duration_utils.get_instrument_configuration_duration_per_exposure')
}

DRAMATIQ_BROKER = {
    "BROKER": "dramatiq.brokers.redis.RedisBroker",
    "OPTIONS": {
        "url": get_dramqtiq_broker_url()
    },
    "MIDDLEWARE": [
        "dramatiq.middleware.Prometheus",
        "dramatiq.middleware.AgeLimit",
        "dramatiq.middleware.TimeLimit",
        "dramatiq.middleware.Callbacks",
        "dramatiq.middleware.Retries",
        "django_dramatiq.middleware.DbConnectionsMiddleware",
    ]
}

TEST_RUNNER = 'observation_portal.test_runner.MyDiscoverRunner'

# Configure Sentry
SENTRY_DSN = os.getenv("SENTRY_DSN")

def traces_sampler(ctx):
    fallback = float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "0.10"))

    if ctx.get("parent_sampled") is not None:
        return ctx.get("parent_sampled")

    url = ctx.get("wsgi_environ", {}).get("PATH_INFO", "") or ctx.get("asgi_scope", {}).get("path", "")

    # Disable traces for all zpages (health, etc)
    if url.startswith("/zpages/"):
        return 0

    return fallback

def profiles_sampler(context):
    # This rate is on top of the traces collected
    return float(os.getenv("SENTRY_PROFILES_SAMPLE_RATE", "0.50"))

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        traces_sampler=traces_sampler,
        profiles_sampler=profiles_sampler,
    )

try:
    from local_settings import *  # noqa
except ImportError:
    pass

try:
    INSTALLED_APPS += LOCAL_INSTALLED_APPS  # noqa
    ALLOWED_HOSTS += LOCAL_ALLOWED_HOSTS  # noqa
except NameError:
    pass
