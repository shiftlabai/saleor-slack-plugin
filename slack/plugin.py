import json
from typing import Any
from urllib import request

from django.core.exceptions import ValidationError
from saleor.account.models import User
from saleor.plugins.base_plugin import BasePlugin, ConfigurationTypeField
from saleor.plugins.models import PluginConfiguration


class SlackPlugin(BasePlugin):
    PLUGIN_ID = "ai.shiftlab.slack"
    PLUGIN_NAME = "Slack Plugin"
    PLUGIN_DESCRIPTION = "Do various things with Slack from Saleor"
    CONFIG_STRUCTURE = {
        "webhook_url": {
            "type": ConfigurationTypeField.STRING,
            "help_text": "The Slack webhook URL for your channel",
            "label": "Webhook URL",
        },
    }
    DEFAULT_CONFIGURATION = [{"name": "webhook_url", "value": None}]

    @classmethod
    def validate_plugin_configuration(cls, plugin_configuration: PluginConfiguration):
        """Validate if provided configuration is correct"""
        missing_fields = []
        configuration = {
            item["name"]: item["value"] for item in plugin_configuration.configuration
        }
        if not configuration["webhook_url"]:
            missing_fields.append("Webhook URL")

        if plugin_configuration.active and missing_fields:
            error_msg = f"To enable this plugin, please provide values for the following fields: {', '.join(missing_fields)}"
            raise ValidationError(error_msg)


    def customer_updated(self, user: User, previous_value: Any) -> Any:
        if self.active:
            self.post_to_slack(message=f"User {user.first_name} {user.last_name} ({user.email}) updated their details!")
        return previous_value


    def post_to_slack(self, message: str):
        """
        Writes a message to the slack channel associated with the `webhook_url`
        configuration value, using Slack's Incoming Webhook API
        (https://api.slack.com/messaging/webhooks)
        """
        configuration = {
            item["name"]: item["value"] for item in self.configuration
        }
        if not configuration["webhook_url"]:
            return

        url = configuration["webhook_url"]
        data = json.dumps({"text": message}).encode('utf-8')
        req = request.Request(url, data)
        req.add_header('Content-Type', 'application/json')
        request.urlopen(req)
