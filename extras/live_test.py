"""
Run some simple test on an actual cachet setup.
This can be set up locally with docker fairly quickly.

Set the following enviroment variables before running the script:

- CACHET_ENDPOINT (eg: http://test.example.com/api/v1)
- CACHET_API_TOKEN (eg. Wohc7eeGhaewae7zie1E)
"""
import os
import pprint

import cachetclient
from cachetclient.v1.client import Client
from cachetclient.v1 import enums

CACHET_ENDPOINT = os.environ.get('CACHET_ENDPOINT')
CACHET_API_TOKEN = os.environ.get('CACHET_API_TOKEN')
CLIENT = None


def client() -> Client:
    global CLIENT
    if CLIENT is None:
        CLIENT = cachetclient.Client(endpoint=CACHET_ENDPOINT, api_token=CACHET_API_TOKEN)

    return CLIENT


def main():
    if CACHET_ENDPOINT is None:
        raise ValueError("CACHET_ENDPOINT enviroment variable missing")

    if CACHET_API_TOKEN is None:
        raise ValueError("CACHET_API_TOKEN enviroment variable missing")

    test_ping()
    test_version()
    test_components()
    test_component_groups()
    test_subscribers()
    test_issues()
    test_issue_updates()
    test_metrics()
    test_metric_points()


def test_ping():
    result = client().ping()
    if result is not True:
        raise ValueError("Ping failed. {} ({}) returned instead of True (bool)".format(result, type(result)))


def test_version():
    version = client().version()
    if version.value is not str and len(version.value) < 3:
        raise ValueError("Version value string suspicious? '{}'".format(version.value))

    # {
    #     'meta': {
    #         'on_latest': True,
    #         'latest': {
    #             'tag_name': 'v2.3.16',
    #             'prelease': False,
    #             'draft': False
    #         }
    #     },
    #     'data': '2.3.14-dev'
    # }
    print("Version   :", version.value)
    print("on_latest :", version.on_latest)
    print("latest    :", version.latest)


def test_components():
    comp = client().components.create(
        "Test Component",
        description="This is a test"
    )
    print(comp.status)
    assert comp.status == enums.COMPONENT_STATUS_OPERATIONAL

    # Create component
    comp.name = "Test Thing"
    comp = comp.update()
    assert comp.name == "Test Thing"
    assert comp.description == "This is a test"
    assert comp.status == enums.COMPONENT_STATUS_OPERATIONAL

    pprint.pprint(comp.attrs)
    comp = client().components.update(comp.id, "moo")
    pprint.pprint(comp.attrs)

    comp.delete()



def test_component_groups():
    pass


def test_subscribers():
    pass


def test_issues():
    pass


def test_issue_updates():
    pass


def test_metrics():
    pass


def test_metric_points():
    pass


if __name__ == '__main__':
    main()
