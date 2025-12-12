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


def test_update_and_delete(client):
    payload = {
        "checksum": "def456",
        "checksum_algorithm": "sha256",
        "file_path": "ex2.tex",
        "tags_json": "[]",
        "metadata_json": "{}"
    }
    r = client.post("/v1/exercises/", json=payload)
    assert r.status_code == 200
    ex_id = r.json()["id"]

    # Update file_path
    update_payload = {"file_path": "ex2_updated.tex"}
    r2 = client.put(f"/v1/exercises/{ex_id}", json=update_payload)
    assert r2.status_code == 200
    assert r2.json()["file_path"] == "ex2_updated.tex"

    # Delete
    r3 = client.delete(f"/v1/exercises/{ex_id}")
    assert r3.status_code == 200
    assert r3.json()["status"] == "deleted"
    assert r3.json()["id"] == ex_id
