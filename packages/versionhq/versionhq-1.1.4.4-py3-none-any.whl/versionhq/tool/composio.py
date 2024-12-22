import os
from dotenv import load_dotenv
from typing import Any, Callable, Type, get_args, get_origin
from composio import ComposioToolSet, Action, App


load_dotenv(override=True)
DEFAULT_REDIRECT_URL = os.environ.get("DEFAULT_REDIRECT_URL")
DEFAULT_APP_NAME = "hubspot"
DEFAULT_USER_ID = os.environ.get("DEFAULT_USER_ID")


def connect(app_name: str = DEFAULT_APP_NAME, user_id: str = DEFAULT_USER_ID, redirect_url: str = DEFAULT_REDIRECT_URL, *args, **kwargs):
    """
    Connect with the data pipelines or destination services.
    """

    composio_toolset = ComposioToolSet(api_key=os.environ.get("COMPOSIO_API_KEY"))


    if not user_id:
        return None

    auth_scheme = "OAUTH2"
    connection_request = composio_toolset.initiate_connection(
        app=app_name,
        redirect_url = redirect_url, # user comes here after oauth flow
        entity_id=user_id,
        auth_scheme=auth_scheme,
    )

    print(connection_request.connectedAccountId,connection_request.connectionStatus)
    print(connection_request.redirectUrl)



    # connection_request_id = "connection_request_id" # replace connection_request_id from earlier response
    # # validate the connection is active
    # connected_account = composio_toolset.get_connected_account(id=connection_request_id)
    # print(connected_account.status)  # should be 


# @action(toolname="hubspot")
# def deploy_on_hubspot(param1: str, param2: str, execute_request: Callable) -> str:
#     """
#     Deploy the messaging workflow on the third-party service using Composio.
#     List of the services: https://composio.dev/tools?category=marketing

#     my custom action description which will be passed to llm

#     :param param1: param1 description which will be passed to llm
#     :param param2: param2 description which will be passed to llm
#     :return info: return description
#     """

#     response = execute_request(
#         "/my_action_endpoint",
#         "GET",
#         {} # body can be added here
#     )    # execute requests by appending credentials to the request
#     return str(response) # complete auth dict is available for local use if needed

    
#     toolset = ComposioToolSet(entity_id=D)
#     tools = composio_toolset.get_tools(actions=[deploy_on_hubspot])


# rag_tools = composio_toolset.get_tools(
#     apps=[App.RAGTOOL],
#     actions=[
#         Action.FILETOOL_LIST_FILES,
#         Action.FILETOOL_CHANGE_WORKING_DIRECTORY,
#         Action.FILETOOL_FIND_FILE,
#     ],
# )

# rag_query_tools = composio_toolset.get_tools(
#     apps=[App.RAGTOOL],
# )

# # can pass multiple actions
# tools = composio_toolset.get_tools(
#     actions=[Action.GITHUB_CREATE_AN_ISSUE]
# )

# rag_tools = composio_toolset.get_tools(
#     apps=[App.RAGTOOL],
#     actions=[
#         Action.FILETOOL_LIST_FILES,
#         Action.FILETOOL_CHANGE_WORKING_DIRECTORY,
#         Action.FILETOOL_FIND_FILE,
#     ],
# )

# rag_query_tools = composio_toolset.get_tools(
#     apps=[App.RAGTOOL],
# )


if __name__ == "__main__":
    connect()

