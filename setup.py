from setuptools import setup

setup(
    name="slack-plugin",
    version="1.0",
    packages=["slack"],
    package_dir={"slack": "slack"},
    install_requires=[],
    entry_points={"saleor.plugins": ["slack = slack.plugin:SlackPlugin"]},
)
