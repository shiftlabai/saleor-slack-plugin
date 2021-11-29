# Saleor Slack Plugin

A simple Saleor plugin that posts to a specific Slack channel via a Slack webhook in response to certain events in Saleor.

NB: this plugin imports from the `saleor` package, so if you open it in e.g. VS Code you might see import errors. So far I've got round that by just working in the same virtualenv I use when hacking on `saleor`.

## Getting started

Set up Slack

1. Create a temporary Slack channel for testing
2. Create a [Slack App](https://api.slack.com/apps)
3. In the Slack app settings, click **Incoming Webhooks** > **Add New Webhook to Workspace**, and associate the webhook with the channel you created. Make a note of the webhook's URL. (Run the `curl` example code shown in the Slack API console to make sure it's working as you expect.)

Set up Saleor

```
cd path/to/saleor
pip install -e path/to/saleor-slack-plugin
python3 manage.py runserver
```

Now run the Saleor dashboard, go to http://localhost:9000/ and log in. Then go to http://localhost:9000/plugins/ai.shiftlab.slack/, enable the plugin and enter the webhook URL.

Then go and e.g. edit a customer at http://localhost:9000/customers/ and you should see some messages in your Slack channel.
