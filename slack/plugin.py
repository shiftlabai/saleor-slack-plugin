import json
from typing import Any, Union
from urllib import request

from django.core.exceptions import ValidationError
from saleor.account.models import Address, User
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

    def change_user_address(
        self,
        address: Address,
        address_type: Union[str, None],
        user: Union[User, None],
        previous_value: Address,
    ) -> Address:
        if self.active and user:
            self.post_to_slack(
                message=f"{user.first_name} {user.last_name} ({user.email}) updated their address"
            )

        # Should we return address or previous_value here? It's not clear.
        return address

    def post_to_slack(self, message: str):
        """
        Writes a message to the slack channel associated with the `webhook_url`
        configuration value, using Slack's Incoming Webhook API
        (https://api.slack.com/messaging/webhooks)
        """
        configuration = {item["name"]: item["value"] for item in self.configuration}
        if not configuration["webhook_url"]:
            return

        url = configuration["webhook_url"]
        data = json.dumps({"text": message}).encode("utf-8")
        req = request.Request(url, data)
        req.add_header("Content-Type", "application/json")
        request.urlopen(req)
