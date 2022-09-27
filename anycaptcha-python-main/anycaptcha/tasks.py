import base64
from .fields import BaseField


class BaseTask(object):
    def serialize(self, **result):
        return result


class ProxyMixin(BaseTask):
    def __init__(self, *args, **kwargs):
        self.proxyType = kwargs.pop("proxy_type")
        self.userAgent = kwargs.pop("user_agent")
        self.proxyAddress = kwargs.pop("proxy_address")
        self.proxyPort = kwargs.pop("proxy_port")
        self.proxyLogin = kwargs.pop("proxy_login")
        self.proxyPassword = kwargs.pop("proxy_password")

        self.cookies = kwargs.pop("cookies", "")
        super(ProxyMixin, self).__init__(*args, **kwargs)

    def serialize(self, **result):
        result = super(ProxyMixin, self).serialize(**result)
        result["userAgent"] = self.userAgent
        result["proxyType"] = self.proxyType
        result["proxyAddress"] = self.proxyAddress
        result["proxyPort"] = self.proxyPort
        if self.proxyLogin:
            result["proxyLogin"] = self.proxyLogin
            result["proxyPassword"] = self.proxyPassword
        if self.cookies:
            result["cookies"] = self.cookies
        return result


class RecaptchaV2TaskProxyless(BaseTask):
    type = "RecaptchaV2TaskProxyless"
    websiteURL = None
    websiteKey = None
    websiteSToken = None
    recaptchaDataSValue = None
    time_sleep=3
    def __init__(
        self,
        website_url,
        website_key,
        website_s_token=None,
        is_invisible=None,
        recaptcha_data_s_value=None,
    ):
        self.websiteURL = website_url
        self.websiteKey = website_key
        self.websiteSToken = website_s_token
        self.recaptchaDataSValue = recaptcha_data_s_value
        self.isInvisible = is_invisible

    def serialize(self):
        data = {
            "type": self.type,
            "websiteURL": self.websiteURL,
            "websiteKey": self.websiteKey,
        }
        if self.websiteSToken is not None:
            data["websiteSToken"] = self.websiteSToken
        if self.isInvisible is not None:
            data["isInvisible"] = self.isInvisible
        if self.recaptchaDataSValue is not None:
            data["recaptchaDataSValue"] = self.recaptchaDataSValue
        return data

class RecaptchaV2Task(BaseTask):
    type = "RecaptchaV2Task"
    websiteURL = None
    websiteKey = None
    websiteSToken = None
    recaptchaDataSValue = None
    time_sleep=3

    def __init__(
        self,
        website_url,
        website_key,proxy_address,proxy_port,proxy_type,user_agent,proxy_login=None,proxy_password=None,cookies=None,
        website_s_token=None,
        is_invisible=None,
        recaptcha_data_s_value=None):
        self.websiteURL = website_url
        self.websiteKey = website_key
        self.websiteSToken = website_s_token
        self.recaptchaDataSValue = recaptcha_data_s_value
        self.isInvisible = is_invisible
        self.proxyType = proxy_type
        self.userAgent = user_agent
        self.proxyAddress = proxy_address
        self.proxyPort = proxy_port
        self.proxyLogin = proxy_login
        self.proxyPassword = proxy_password
        self.cookies = cookies

    def serialize(self):
        data = {
            "type": self.type,
            "websiteURL": self.websiteURL,
            "websiteKey": self.websiteKey,
            "proxyType": self.proxyType,
            "proxyAddress": self.proxyAddress,
            "proxyPort": self.proxyPort,
            "userAgent": self.userAgent
        }
        if self.websiteSToken is not None:
            data["websiteSToken"] = self.websiteSToken
        if self.isInvisible is not None:
            data["isInvisible"] = self.isInvisible
        if self.recaptchaDataSValue is not None:
            data["recaptchaDataSValue"] = self.recaptchaDataSValue
        if self.proxyLogin is not None:
            data["proxyLogin"]= self.proxyLogin
        if self.proxyPassword is not None:
            data["proxyPassword"]= self.proxyPassword
        if self.cookies is not None:
            data["cookies"]= self.cookies
        return data





class FunCaptchaProxylessTask(BaseTask):
    type = "FunCaptchaTaskProxyless"
    websiteURL = None
    websiteKey = None
    time_sleep = 0.1
    def __init__(self, website_url, website_key, *args, **kwargs):
        self.websiteURL = website_url
        self.websiteKey = website_key
        super(FunCaptchaProxylessTask, self).__init__(*args, **kwargs)

    def serialize(self, **result):
        result = super(FunCaptchaProxylessTask, self).serialize(**result)
        result.update(
            {
                "type": self.type,
                "websiteURL": self.websiteURL,
                "websitePublicKey": self.websiteKey,
            }
        )
        return result



class ImageToTextTask(object):
    type = "ImageToTextTask"
    fp = None
    phrase = None
    case = None
    numeric = None
    math = None
    minLength = None
    maxLength = None
    time_sleep = 1
    def __init__(
        self,
        fp,
        phrase=None,
        case=None,
        numeric=None,
        math=None,
        min_length=None,
        max_length=None,
    ):
        self.fp = fp
        self.phrase = phrase
        self.case = case
        self.numeric = numeric
        self.math = math
        self.minLength = min_length
        self.maxLength = max_length

    def serialize(self):
        return {
            "type": self.type,
            "body": base64.b64encode(self.fp.read()).decode("utf-8"),
            "phrase": self.phrase,
            "case": self.case,
            "numeric": self.numeric,
            "math": self.math,
            "minLength": self.minLength,
            "maxLength": self.maxLength,
        }

class CustomCaptchaTask(BaseTask):
    type = "CustomCaptchaTask"
    imageUrl = None
    assignment = None
    form = None

    def __init__(self, imageUrl, form=None, assignment=None):
        self.imageUrl = imageUrl
        self.form = form or {}
        self.assignment = assignment

    def serialize(self):
        data = super(CustomCaptchaTask, self).serialize()
        data.update({"type": self.type, "imageUrl": self.imageUrl})
        if self.form:
            forms = []
            for name, field in self.form.items():
                if isinstance(field, BaseField):
                    forms.append(field.serialize(name))
                else:
                    field = field.copy()
                    field["name"] = name
                    forms.append(field)
            data["forms"] = forms
        if self.assignment:
            data["assignment"] = self.assignment
        return data


class RecaptchaV3TaskProxyless(BaseTask):
    type = "RecaptchaV3TaskProxyless"
    websiteURL = None
    websiteKey = None
    minScore = None
    pageAction = None
    time_sleep = 3
    def __init__(self, website_url, website_key, min_score, page_action=""):
        self.websiteURL = website_url
        self.websiteKey = website_key
        self.minScore = min_score
        self.pageAction = page_action

    def serialize(self):
        data = super(RecaptchaV3TaskProxyless, self).serialize()
        data["type"] = self.type
        data["websiteURL"] = self.websiteURL
        data["websiteKey"] = self.websiteKey
        data["minScore"] = self.minScore
        data["pageAction"] = self.pageAction
        return data


class HCaptchaTaskProxyless(BaseTask):
    type = "HCaptchaTaskProxyless"
    websiteURL = None
    websiteKey = None
    time_sleep = 2
    def __init__(self, website_url, website_key, *args, **kwargs):
        self.websiteURL = website_url
        self.websiteKey = website_key
        super(HCaptchaTaskProxyless, self).__init__(*args, **kwargs)

    def serialize(self, **result):
        data = super(HCaptchaTaskProxyless, self).serialize(**result)
        data["type"] = self.type
        data["websiteURL"] = self.websiteURL
        data["websiteKey"] = self.websiteKey
        return data
    
class ZaloTask(BaseTask):
    type = "ZaloTask"
    websiteURL = None
    websiteKey = None
    time_sleep = 2
    def __init__(self, *args, **kwargs):
        super(ZaloTask, self).__init__(*args, **kwargs)

    def serialize(self, **result):
        data = super(ZaloTask, self).serialize(**result)
        data["type"] = self.type
        return data

class HCaptchaTask(BaseTask):
    type = "HCaptchaTask"
    websiteURL = None
    websiteKey = None
    websiteSToken = None
    recaptchaDataSValue = None
    time_sleep = 2

    def __init__(
            self,
            website_url,
            website_key, proxy_address, proxy_port, proxy_type, user_agent, proxy_login=None, proxy_password=None):
        self.websiteURL = website_url
        self.websiteKey = website_key

        self.proxyType = proxy_type
        self.userAgent = user_agent
        self.proxyAddress = proxy_address
        self.proxyPort = proxy_port
        self.proxyLogin = proxy_login
        self.proxyPassword = proxy_password

    def serialize(self):
        data = {
            "type": self.type,
            "websiteURL": self.websiteURL,
            "websiteKey": self.websiteKey,
            "proxyType": self.proxyType,
            "proxyAddress": self.proxyAddress,
            "proxyPort": self.proxyPort,
            "userAgent": self.userAgent
        }
        if self.proxyLogin is not None:
            data["proxyLogin"] = self.proxyLogin
        if self.proxyPassword is not None:
            data["proxyPassword"] = self.proxyPassword
        return data





