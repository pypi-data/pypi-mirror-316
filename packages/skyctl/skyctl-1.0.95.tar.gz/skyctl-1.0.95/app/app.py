import requests
import click.core as click_core


def create_app(api_url, user_id, title, desc, repo, version, config, acct_id):
    payload = {
        "title": title,
        "description": desc,
        "repo": repo,
        "version": version,
        "config": config,
        "acctId": int(acct_id),
        "userId": int(user_id)
    }
    headers = {"X-UserId": user_id, "Content-Type": "application/json"}
    response = requests.post(f"{api_url}", json=payload, headers=headers)
    return response.json() if response.status_code == 200 else f"Error creating app: {response.status_code} {response.text}"


def update_app(ctx, api_url, user_id, app_id, title, desc, repo, acct_id):

    headers = {"X-UserId": user_id, "Content-Type": "application/json"}
    response = requests.get(f"{api_url}/{app_id}", headers=headers)
    if response.status_code != 200:
        return f"Error fetching app: {response.status_code} {response.text}"
    else:
        existing_data = response.json()
    payload = {
        "title": title if ctx.get_parameter_source('title') == click_core.ParameterSource.COMMANDLINE else existing_data.get("title"),
        "description": desc if ctx.get_parameter_source('desc') == click_core.ParameterSource.COMMANDLINE else existing_data.get("desc"),
        "repo": repo if ctx.get_parameter_source('title') == click_core.ParameterSource.COMMANDLINE else existing_data.get("repo"),
        "accountId": acct_id if ctx.get_parameter_source('acct_id') == click_core.ParameterSource.COMMANDLINE else existing_data.get("acct_id"),
        "version": existing_data.get("version"),
        "userId": int(user_id)
    }
    response = requests.patch(f"{api_url}", json=payload, headers=headers)
    return response.json() if response.status_code == 200 else f"Error updating app: {response.status_code} {response.text}"


def delete_app(api_url, user_id, app_id, force):
    headers = {"X-UserId": user_id, "Content-Type": "application/json"}
    response = requests.delete(f"{api_url}/{app_id}",headers=headers)
    return response.json() if response.status_code == 200 else f"Error deleting app: {response.status_code} {response.text}"


def get_app(api_url, user_id, app_id):
    """获取 App 详情"""
    headers = {"X-UserId": str(user_id), "Content-Type": "application/json"}
    response = requests.get(f"{api_url}/{app_id}", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error getting app: {response.status_code} {response.text}"



def list_apps(api_url, user_id, page, limit, sort):
    endpoint = f"{api_url}?page={page}&limit={limit}&sort={sort}"
    headers = {"X-UserId": str(user_id), "Content-Type": "application/json"}

    try:
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Error listing apps: {response.status_code} {response.text}"
    except requests.RequestException as e:
        return f"Request failed: {e}"
