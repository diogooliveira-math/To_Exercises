def test_create_and_get(client):
    payload = {
        "checksum": "abc123",
        "checksum_algorithm": "sha256",
        "file_path": "ex1.tex",
        "tags_json": "[\"alg\"]",
        "metadata_json": "{}"
    }
    r = client.post("/v1/exercises/", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["checksum"] == "abc123"
    ex_id = data["id"]
    r2 = client.get(f"/v1/exercises/{ex_id}")
    assert r2.status_code == 200
    data2 = r2.json()
    assert data2["id"] == ex_id
