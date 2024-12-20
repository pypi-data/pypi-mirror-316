import requests
import json
import click.core as click_core


def create_dashboard(api_url, user_id, title, desc, size, url):
    """API request to create a dashboard"""
    endpoint = api_url
    headers = {"X-UserId": user_id, "Content-Type": "application/json"}
    payload = {
        "title": title,
        "description": desc,
        "size": size,
        "url": url,
        "userId": int(user_id)
    }

    try:
        response = requests.post(endpoint, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Error creating dashboard: {response.status_code} {response.text}"
    except requests.RequestException as e:
        return f"Request failed: {e}"


def list_dashboard(api_url, user_id, page, limit, sort):
    """API request to list dashboards"""
    endpoint = f"{api_url}?page={page}&limit={limit}&sort={sort}"
    headers = {"X-UserId": user_id, "Content-Type": "application/json"}

    try:
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Error listing dashboards: {response.status_code} {response.text}"
    except requests.RequestException as e:
        return f"Request failed: {e}"


def get_dashboard(api_url, user_id, dashboard_id):
    """API request to get dashboard details"""
    endpoint = f"{api_url}/{dashboard_id}"
    headers = {"X-UserId": user_id, "Content-Type": "application/json"}

    try:
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Error getting dashboard: {response.status_code} {response.text}"
    except requests.RequestException as e:
        return f"Request failed: {e}"


def update_dashboard(ctx, api_url, user_id, dashboard_id, title, desc, size, url):
    """API request to update a dashboard"""
    endpoint = f"{api_url}/{dashboard_id}"
    headers = {"X-UserId": user_id, "Content-Type": "application/json"}

    # First, send a GET request to fetch current dashboard data
    try:
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 200:
            current_data = response.json()
        else:
            return f"Error fetching dashboard: {response.status_code} {response.text}"
    except requests.RequestException as e:
        return f"Request failed: {e}"

    # Prepare payload, replacing with current values if params are None or empty
    payload = {
        "title": title if ctx.get_parameter_source('title') == click_core.ParameterSource.COMMANDLINE else current_data.get("title"),
        "description": desc if ctx.get_parameter_source('desc') == click_core.ParameterSource.COMMANDLINE else current_data.get("description"),
        "size": size if ctx.get_parameter_source('size') == click_core.ParameterSource.COMMANDLINE else current_data.get("size"),
        "url": url if ctx.get_parameter_source('url') == click_core.ParameterSource.COMMANDLINE else current_data.get("url"),
        "userId": int(user_id)
    }

    # Now send the PATCH request to update the dashboard
    try:
        response = requests.patch(endpoint, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Error updating dashboard: {response.status_code} {response.text}"
    except requests.RequestException as e:
        return f"Request failed: {e}"


def delete_dashboard(api_url, user_id, dashboard_id):
    """API request to delete a dashboard"""
    endpoint = f"{api_url}/{dashboard_id}"
    headers = {"X-UserId": user_id, "Content-Type": "application/json"}

    try:
        response = requests.delete(endpoint, headers=headers)
        if response.status_code == 200:
            return "Dashboard successfully deleted."
        else:
            return f"Error deleting dashboard: {response.status_code} {response.text}"
    except requests.RequestException as e:
        return f"Request failed: {e}"
