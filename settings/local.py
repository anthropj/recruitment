from .base import *

# import sentry_sdk
# from sentry_sdk.integrations.django import DjangoIntegration


DINGTALK_WEB_HOOK = 'https://oapi.dingtalk.com/robot/send?access_token=3ee456a7de50cb5c1da467bf3f5102ca49b739d6d1da1b451b108e240e59a00e'

# sentry_sdk.init(
#     dsn="http://e4212707b7cd4c45aa15328756fd3fef@119.45.160.103:9000/2",
#     integrations=[DjangoIntegration()],
#     traces_sample_rate=1.0,

#     # If you wish to associate users to errors (assuming you are using
#     # django.contrib.auth) you may enable sending PII data.
#     send_default_pii=True
# )

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERYD_MAX_TASKS_PER_CHILD = 10
CELERYD_LOG_FILE = os.path.join(BASE_DIR, "logs", "celery_work.log")
CELERYBEAT_LOG_FILE = os.path.join(BASE_DIR, "logs", "celery_beat.log")

DEFAULT_FILE_STORAGE = 'django_oss_storage.backends.OssMediaStorage'

OSS_ACCESS_KEY_ID = 'LTAI4G7wqwAMdGxDi9o8vmso'
OSS_ACCESS_KEY_SECRET = 'RM77W77Q6ClITqbHeZd1B6mPa674e0'
# The name of the bucket to store files in
OSS_BUCKET_NAME = 'recruitment-anthropj'

# The URL of AliCloud OSS endpoint
# Refer https://www.alibabacloud.com/help/zh/doc-detail/31837.htm for OSS Region & Endpoint
OSS_ENDPOINT = 'oss-cn-hangzhou.aliyuncs.com'