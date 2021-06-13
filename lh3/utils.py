try:
    import lh3.api

    client = lh3.api.Client()
except:
    import lh3.api

    client = lh3.api.Client()

import re

# Example...

content_range_pattern = re.compile(r"chats (\d+)-(\d+)\/(\d+)")


def extract_content_range(content_range):
    matches = content_range_pattern.match(content_range)
    begin = matches.group(1)
    end = matches.group(2)
    total = matches.group(3)
    return (begin, end, total)


def search_chats(client, query, chat_range):
    begin, end = chat_range
    try:
        _, x_api_version = lh3.api._API.versions.get("v4")
    except:
        _, x_api_version = _API.versions.get("v4")
    headers = {
        "Content-Type": "application/json",
        "Range": "chats {begin}-{end}",
        "X-Api-Version": x_api_version,
    }

    request = getattr(client.api().session, "post")
    response = request(
        client.api()._api("v4", "/chat/_search"), headers=headers, json=query
    )
    chats = client.api()._maybe_json(response)
    content_range = extract_content_range(response.headers["Content-Range"])
    return chats, content_range


"""
# Query chats on a specific queue for a date range.
query = {
    'query': {
        'queue': ['western'],
        'from': '2021-01-01',
        'to': '2021-05-19'
    },
    'sort': [
        {'started': 'descending'}
    ]
}
chats, content_range = search_chats(client, query, chat_range=(0, 100))
results_begin, results_end, results_total = content_range

"""
