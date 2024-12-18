import http

import pytest

from h2o_engine_manager.clients.exception import CustomApiException


@pytest.mark.timeout(60)
def test_h2o_engine_profile_usage(clients, admin_clients, h2o_engine_profile_p1):
    workspace_id = "687cc72b-8061-4e59-a866-5bcad26aa4b7"
    engine_id = "e1"

    # Regular user does not have matching OIDC roles -> cannot create engine with this profile.
    with pytest.raises(CustomApiException) as exc:
        clients.h2o_engine_client.create_engine(
            version="mock",
            workspace_id=workspace_id,
            engine_id=engine_id,
            profile=h2o_engine_profile_p1.name,
        )
    assert exc.value.status == http.HTTPStatus.BAD_REQUEST

    # Admin client has matching OIDC role -> can create engine with this profile.
    eng = admin_clients.h2o_engine_client.create_engine(
        version="mock",
        workspace_id=workspace_id,
        engine_id=engine_id,
        profile=h2o_engine_profile_p1.name,
    )

    try:
        assert eng.name == f"workspaces/{workspace_id}/h2oEngines/e1"
        assert eng.profile == "workspaces/global/h2oEngineProfiles/p1"
    finally:
        admin_clients.h2o_engine_client.client_info.api_instance.h2_o_engine_service_delete_h2_o_engine(
            name_4=f"workspaces/{workspace_id}/h2oEngines/{engine_id}", allow_missing=True
        )