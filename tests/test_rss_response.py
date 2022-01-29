from lxml import etree


def test_rss_sample_response(client, expected_response):
    response = client.get('/1')
    assert response.status_code == 200
    assert response.text.replace('\n', '').replace(' ', '') == expected_response


def test_rss_guid(client):
    response = client.get('/2')
    tree = etree.fromstring(response.content)
    assert response.status_code == 200
    assert tree.xpath('//guid') != []
    assert tree.xpath('//guid')[0].text == 'abcdefghijklmnopqrstuvwxyz'


def test_rss_item_category(client):
    response = client.get('/2')
    tree = etree.fromstring(response.content)
    assert response.status_code == 200
    assert tree.xpath('//category') != []
    assert tree.xpath('//category')[0].attrib['domain'] == 'test'
    assert tree.xpath('//category')[0].text == '0001'
