from chess_spy import chess_com


PGN = """
[Event "Live Chess"]
[Site "Chess.com"]
[Date "2026.05.17"]
[Round "-"]
[White "dissolved-peat"]
[Black "opponent"]
[Result "1-0"]

1. e4 e5 1-0
""".strip()


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        pass

    def json(self):
        return self.payload


class FakeSession:
    def __init__(self):
        self.headers = {}
        self.requested_urls = []

    def get(self, url):
        self.requested_urls.append(url)

        if url.endswith("/archives"):
            return FakeResponse(
                {
                    "archives": [
                        "https://example.test/2026/01",
                        "https://example.test/2026/02",
                        "https://example.test/2026/03",
                        "https://example.test/2026/04",
                    ]
                }
            )

        return FakeResponse({"games": [{"pgn": PGN}]})


def test_chess_com_imports_last_three_archives(monkeypatch):
    fake_session = FakeSession()
    monkeypatch.setattr(chess_com.requests, "Session", lambda: fake_session)
    monkeypatch.setattr(chess_com.time, "sleep", lambda seconds: None)

    client = chess_com.ChessCom("dissolved-peat")

    assert fake_session.headers["Accept-Encoding"] == "gzip, deflate"
    assert fake_session.requested_urls == [
        chess_com.ARCHIVES_URL.format(username="dissolved-peat"),
        "https://example.test/2026/02",
        "https://example.test/2026/03",
        "https://example.test/2026/04",
    ]
    assert len(client.games) == 3
