from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_empty_message():
    message = {
        "recipient_id": "test-recipient",
        "sender_id": "test-sender",
        "text": "",
        "timestamp": "2022-06-15T11:00:00",
    }
    words_to_highlight = ["HELLO", "world"]
    response = client.post(
        "/message/highlight",
        json={
            "message": message,
            "words_to_highlight": words_to_highlight,
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        **message,
        "fragments": [],
    }


def test_text_with_empty_words():
    arg = "Just a random piece of words"
    message = {
        "recipient_id": "test-recipient",
        "sender_id": "test-sender",
        "text": arg,
        "timestamp": "2022-06-15T11:00:00",
    }
    words_to_highlight = []
    response = client.post(
        "/message/highlight",
        json={
            "message": message,
            "words_to_highlight": words_to_highlight,
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        **message,
        "fragments": [{'is_highlighted': False, 'text': arg}],
    }


def test_text_with_multiple_spaces():
    arg = "This message has   multiple  spaces between  words."
    message = {
        "recipient_id": "test-recipient",
        "sender_id": "test-sender",
        "text": arg,
        "timestamp": "2022-06-15T11:00:00",
    }
    words_to_highlight = []
    response = client.post(
        "/message/highlight",
        json={
            "message": message,
            "words_to_highlight": words_to_highlight,
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        **message,
        "fragments": [{'is_highlighted': False,
                        'text': "This message has multiple spaces between words."}],
    }


def test_text_in_multigroups():
    arg = "Hello World! hello world! HeLLo WoRlD! HELLO WORLD!"
    message = {
        "recipient_id": "test-recipient",
        "sender_id": "test-sender",
        "text": arg,
        "timestamp": "2022-06-15T11:00:00",
    }
    words_to_highlight = ['hello']
    response = client.post(
        "/message/highlight",
        json={
            "message": message,
            "words_to_highlight": words_to_highlight,
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        **message,
        "fragments": [{'is_highlighted': True,
                        'text': "Hello"},
                      {'is_highlighted': False,
                        'text': "World!"},
                      {'is_highlighted': True,
                        'text': "hello"},
                      {'is_highlighted': False,
                        'text': "world!"},
                      {'is_highlighted': True,
                        'text': "HeLLo"},
                      {'is_highlighted': False,
                        'text': "WoRlD!"},
                      {'is_highlighted': True,
                        'text': "HELLO"},
                      {'is_highlighted': False,
                        'text': "WORLD!"}
        ],
    }


def test_text_diff_case_words():
    arg = "Hello hello HeLLo HELLO"
    message = {
        "recipient_id": "test-recipient",
        "sender_id": "test-sender",
        "text": arg,
        "timestamp": "2022-06-15T11:00:00",
    }
    words_to_highlight = ['hello']
    response = client.post(
        "/message/highlight",
        json={
            "message": message,
            "words_to_highlight": words_to_highlight,
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        **message,
        "fragments": [{'is_highlighted': True,
                        'text': arg}],
    }


def test_malformed_args():
    message = {
        "recipient_id": "test-recipient",
        "sender_id": "test-sender",
        "text": None,
        "timestamp": "2022-06-15T11:00:00",
    }
    words_to_highlight = []
    response = client.post(
        "/message/highlight",
        json={
            "message": message,
            "words_to_highlight": words_to_highlight,
        }
    )
    assert response.status_code == 422

    # Interestgingly enough we can't check for Ints passed into Strs
    # because jsonifying the message turns ints into strings :-D
