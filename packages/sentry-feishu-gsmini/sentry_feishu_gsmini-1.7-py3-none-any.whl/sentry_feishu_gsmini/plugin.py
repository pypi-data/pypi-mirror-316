# coding: utf-8

import json
import logging
import requests
from django.urls import re_path
from sentry.exceptions import PluginError
from rest_framework.response import Response
from sentry_plugins.base import CorePluginMixin
from sentry.plugins.bases.issue2 import IssuePlugin2
from sentry.integrations.base import FeatureDescription, IntegrationFeatures
from .forms import FeiShuOptionsForm
from sentry.plugins.bases.issue2 import IssueGroupActionEndpoint, IssuePlugin2
from sentry_plugins.utils import get_secret_field_config

logger = logging.getLogger(__name__)
DESCRIPTION = """
飞书机器人通知插件
你需要先去飞书群聊创建一个机器人，然后获取起webhook地址才能使用此插件
"""


class FeiShuPlugin(CorePluginMixin, IssuePlugin2):
    """
    Sentry plugin to send error counts to FeiShu.
    """
    description = DESCRIPTION
    slug = "feishu"
    title = "飞书"
    version = "1.7"
    conf_title = title
    conf_key = "feishu"
    required_field = "webhook_url"
    feature_descriptions = [
        FeatureDescription(
            """
            添加飞书通知机器人地址，把sentry 接入你自己的飞书通知群。
            """,
            IntegrationFeatures.ISSUE_BASIC,
        )
    ]

    resource_links = [
        ('Source', 'https://github.com/gsmini/sentry-feishu'),
        ('Bug Tracker', 'https://github.com/gsmini/sentry-feishu/issues'),
        ('README', 'https://github.com/gsmini/sentry-feishu/blob/master/README.md'),
    ]

    project_conf_form = FeiShuOptionsForm

    # 检查参数是否填写
    def is_configured(self, project):
        """
        Check if plugin is configured.
        """
        return bool(self.get_option(self.required_field, project))

    def get_group_urls(self):
        return super().get_group_urls() + [
            re_path(
                r"^autocomplete",
                IssueGroupActionEndpoint.as_view(view_method_name="view_autocomplete", plugin=self),
            )
        ]

    # 报错的时候函数
    def handle_api_error(self, error: Exception) -> Response:
        msg = "Error communicating with gsmini@sina.cn"
        status = 400 if isinstance(error, PluginError) else 502
        return Response({"error_type": "validation", "errors": {"__all__": msg}}, status=status)

    def get_configure_plugin_fields(self, project, **kwargs):
        webhook_url = self.get_option(self.required_field, project)
        helptext = (
            "输出你的飞书机器人的地址 比如: https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxxxxxxx"
        )
        secret_field = get_secret_field_config(webhook_url, helptext, include_prefix=True)
        secret_field.update(
            {
                "name": "webhook_url",
                "label": "feishu webhook_url",
                "placeholder": "e.g.  https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxxxxxxx",
            }
        )
        return [
            secret_field
        ]

    def notify_users(self, group, event, *args, **kwargs):
        if not self.is_configured(group.project):
            return None
        if self.should_notify(group, event):
            self.post_process(group, event, *args, **kwargs)
        else:
            return None

    def findrepeatstart(self, origin, matchlen):
        if matchlen < 2 or len(origin) <= matchlen:
            return -1
        i = origin.find(origin[0:matchlen], 1)
        if i == -1:
            return self.findrepeatstart(origin, matchlen // 2)
        return i

    def findrepeatend(self, origin):
        return origin.rfind("...")

    def cutrepeat(self, origin):
        repeatstart = self.findrepeatstart(origin, 120)
        if repeatstart == -1:
            return origin
        repeatend = self.findrepeatend(origin)
        if (repeatend == -1):
            return origin
        return origin[0:repeatstart] + origin[repeatend:]

    def post_process(self, group, event, *args, **kwargs):
        """
        Process error.
        """
        if not self.is_configured(group.project):
            return

        if group.is_ignored():
            return

        send_url = self.get_option(self.required_field, group.project)
        title = u"New alert from {}".format(event.project.slug)
        message = self.cutrepeat(event.message)

        data = {
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": title,
                        "content": [
                            [
                                {
                                    "tag": "text",
                                    "text": message
                                },
                                {
                                    "tag": "a",
                                    "text": "href",
                                    "href": u"{}events/{}/".format(group.get_absolute_url(), event.id)
                                }
                            ]
                        ]
                    }
                }
            }
        }

        try:
            resp = requests.post(
                url=send_url,
                headers={"Content-Type": "application/json"},
                data=json.dumps(data).encode("utf-8")
            )
            if resp.status_code != 200:
                logger.info(f"request uri {send_url} status !=200")
                logger.info(f"request uri {send_url} response:{resp.text} ")
        except requests.exceptions.Timeout as e:
            logger.info(f"request uri {send_url} timeout")
