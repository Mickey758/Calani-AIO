from .base import AnycaptchaClient
from pkg_resources import get_distribution, DistributionNotFound
from .tasks import (
RecaptchaV2Task,
    RecaptchaV2TaskProxyless,
    RecaptchaV3TaskProxyless,
    HCaptchaTask,
    HCaptchaTaskProxyless,
    ImageToTextTask,FunCaptchaProxylessTask,ZaloTask
)
from .exceptions import AnycaptchaException
from .fields import (
    SimpleText,
    Image,
    WebLink,
    TextInput,
    Textarea,
    Checkbox,
    Select,
    Radio,
    ImageUpload,
)

AnycatpchaException = AnycaptchaException

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    pass
