from textwrap import dedent

from fastapi.testclient import TestClient
from lxml import etree


def test_rss_sample_response(client: TestClient, expected_response: str, capsys):
    response = client.get('/1')
    assert response.status_code == 200
    tree = etree.fromstring(response.content)
    pretty: str = etree.tostring(tree, pretty_print=True, xml_declaration=True).decode('ascii')
    for line, expected_line in zip(pretty.splitlines(), expected_response.splitlines()):
        assert dedent(line) == dedent(expected_line), f'{line} != {expected_line}'


def test_rss_guid(client: TestClient):
    response = client.get('/2')
    tree: etree._Element = etree.fromstring(response.content)
    assert response.status_code == 200
    assert tree.xpath('//guid') != []
    assert tree.xpath('//guid')[0].text == 'abcdefghijklmnopqrstuvwxyz'


def test_rss_item_category(client: TestClient):
    response = client.get('/2')
    tree: etree._Element = etree.fromstring(response.content)
    assert response.status_code == 200
    assert tree.xpath('//category') != []
    assert tree.xpath('//category')[0].attrib['domain'] == 'test'
    assert tree.xpath('//category')[0].text == '0001'
