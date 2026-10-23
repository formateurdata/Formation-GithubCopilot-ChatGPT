from versions import comparer_versions, derniere_version


def test_versions_egales():
    assert comparer_versions("1.2.3", "1.2.3") == 0


def test_derniere_version_apres_1_9():
    assert derniere_version(["1.9.0", "1.10.0", "1.2.0"]) == "1.10.0"
