from unittest.mock import patch

from backend.services.moderation import moderate_image


def test_moderation_uses_image_input():
    fake_result = type(
        "Result",
        (),
        {
            "flagged": False,
            "categories": {},
            "category_scores": {},
        },
    )()
    fake_response = type("Response", (), {"results": [fake_result]})()

    with patch("backend.services.moderation.client.moderations.create", return_value=fake_response) as mock_create:
        result = moderate_image("data:image/jpeg;base64,abc")

    assert result["verdict"] == "ALLOW"
    mock_create.assert_called_once()
    assert mock_create.call_args.kwargs["model"] == "omni-moderation-latest"
