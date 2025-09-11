from TEM_comms import topics


def test_documentation():
    for topic, msg in topics.items():
        assert msg.__doc__ is not None and len(
            msg.__doc__.strip()
        ), f"{topic} has no documentation!"
        for field, info in msg.model_fields.items():
            assert info.description is not None and len(
                info.description.strip()
            ), f"Field {field} in {topic} has no description!"
