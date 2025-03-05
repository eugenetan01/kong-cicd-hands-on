import os
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Environment variables
API_BASE_URL = os.getenv("KONNECT_API_BASE_URL")
CONTROL_PLANE_ID = os.getenv("CONTROL_PLANE_ID")  # The ID of the control plane
AUTH_TOKEN = os.getenv("KONNECT_AUTH_TOKEN")

# HTTP headers
HEADERS = {
    "Authorization": f"Bearer {AUTH_TOKEN}",
    "accept": "*/*"
}

def delete_gitops_resources(resource_type: str) -> int:
    """
    Delete all resources of a given type (services or routes) that have the tag 'gitops'.
    """
    try:
        with httpx.Client() as client:
            # Fetch all resources
            endpoint = f"{API_BASE_URL}/v2/control-planes/{CONTROL_PLANE_ID}/core-entities/{resource_type}"
            response = client.get(endpoint, headers=HEADERS)
            if response.status_code != 200:
                print(f"Failed to fetch {resource_type}: {response.text}")
                return 0

            resources = response.json().get("data", [])
            deleted_count = 0

            # Filter and delete resources with the tag 'gitops'
            for resource in resources:
                if "tags" in resource and "gitops" in resource["tags"]:
                    resource_id = resource["id"]
                    delete_response = client.delete(f"{endpoint}/{resource_id}", headers=HEADERS)
                    if delete_response.status_code == 204:
                        print(f"Deleted {resource_type[:-1]} ID {resource_id} with tag 'gitops'")
                        deleted_count += 1
                    else:
                        print(f"Failed to delete {resource_type[:-1]} ID {resource_id}: {delete_response.text}")

            return deleted_count
    except Exception as e:
        print(f"Error during {resource_type} deletion: {e}")
        return 0

def main():
    """
    Main function to delete only resources with the 'gitops' tag.
    """
    if not API_BASE_URL or not CONTROL_PLANE_ID or not AUTH_TOKEN:
        print("Error: Missing API_BASE_URL, CONTROL_PLANE_ID, or AUTH_TOKEN in the environment.")
        return

    print("Starting cleanup process for 'gitops' tagged resources...")

    # Delete only routes with 'gitops' tag
    routes_deleted = delete_gitops_resources("routes")
    print(f"Deleted {routes_deleted} 'gitops' tagged routes.")

    # Delete only services with 'gitops' tag
    services_deleted = delete_gitops_resources("services")
    print(f"Deleted {services_deleted} 'gitops' tagged services.")

    print("Cleanup process for 'gitops' tagged resources completed.")

if __name__ == "__main__":
    main()
