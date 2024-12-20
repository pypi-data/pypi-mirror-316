import requests
import click.core as click_core


def create_account(api_url, user_id, title, desc, host, type, username, password):
    payload = {
        "title": title,
        "description": desc,
        "host": host,
        "type": type,
        "username": username,
        "password": password,
        "userId": int(user_id)
    }
    headers = {"X-UserId": user_id, "Content-Type": "application/json"}
    response = requests.post(f"{api_url}", json=payload, headers=headers)
    return response.json() if response.status_code == 200 else f"Error creating dashboard: {response.status_code} {response.text}"


def get_account_details(api_url, user_id, account_id):
    headers = {"X-UserId": user_id}
    response = requests.get(f"{api_url}/{account_id}", headers=headers)
    return response.json() if response.status_code == 200 else f"Error creating dashboard: {response.status_code} {response.text}"


def update_account(ctx, api_url, user_id, account_id, title, desc, host, type, username, password):
    # Get existing account details
    existing_account = get_account_details(api_url, user_id, account_id)

    # If no existing data, use provided values directly
    if not existing_account:
        return f"No existing account found. Using provided values."

    # Prepare payload, prioritizing provided values
    payload = {
        "title": title if ctx.get_parameter_source('title') == click_core.ParameterSource.COMMANDLINE else existing_account.get("title"),
        "description": desc if ctx.get_parameter_source('desc') == click_core.ParameterSource.COMMANDLINE else  existing_account.get("description"),
        "host": host if ctx.get_parameter_source('title') == click_core.ParameterSource.COMMANDLINE else existing_account.get("host"),
        "type": type if ctx.get_parameter_source('title') == click_core.ParameterSource.COMMANDLINE else existing_account.get("type"),
        "username": username if ctx.get_parameter_source('username') == click_core.ParameterSource.COMMANDLINE else existing_account.get("username"),
        "password": password if ctx.get_parameter_source('password') == click_core.ParameterSource.COMMANDLINE else existing_account.get("password"),
        "userId": int(user_id)
    }

    headers = {"X-UserId": user_id, "Content-Type": "application/json"}
    response = requests.patch(f"{api_url}/{account_id}", json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return f"Error updating account: {response.status_code} {response.text}"


def delete_account(api_url, user_id, account_id, force=False):
    headers = {"X-UserId": user_id}
    response = requests.delete(f"{api_url}/{account_id}", headers=headers)
    return response.json() if response.status_code == 200 else f"Error creating dashboard: {response.status_code} {response.text}"


def list_accounts(api_url, user_id, page, limit, sort):
    headers = {"X-UserId": user_id}
    response = requests.get(f"{api_url}?page={page}&limit={limit}&sort={sort}", headers=headers)
    return response.json() if response.status_code == 200 else f"Error creating dashboard: {response.status_code} {response.text}"
