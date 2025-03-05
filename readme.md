# Setup
1. Create a project on Insomnia and git clone this project in Insomnia

    - navigate to the collection tab and change the env vars (cmd-e) to use the `OpenAPI env localhost:3000` env

# Execution:

1. To showcase API-Ops, make an empty commit and push to dev branch to run the github action
    - Show the `.github/workflows/inso-deck.yaml` that it runs on push to dev branch and PR to master
    - Show the steps in the github action: <br/> 
          - Running the insomnia unit tests defined <br/>
          - Converting my openapi specs to kong gateway config via decK <br/>
          - Validating the decK file <br/>
          - Pushing it as gateway config to my control plane <br/>
    - Verify by going to your control plane to see the APIs in the spec onboarded to the gateway
    - Run below commands to trigger

        ```bash
        git commit --allow-empty -m "Trigger CI/CD pipeline"
        git push origin dev
        ```
# Cleanup

1. Navigate to `./cleanup/konnect` folder and create a venv for the python project

    ```python
    python3 -m venv myenv
    source myenv/bin/activate
    ```

2. Install the requirements.txt for the venv

    `pip3 install -r requirements.txt`

3. Create a .env file with the following vars:

    ```python
    KONNECT_API_BASE_URL="https://global.api.konghq.com"
    KONNECT_AUTH_TOKEN="<your-konnect-PAT>"
    CONTROL_PLANE_ID="<your-control-plane-id>"
    ```

4. Run the `python3 cleanup-konnect.py` to remove the gateway services and routes

# References:

1. See the `./demo-scenes/resources/insomnia-env-var.json` for env vars if needed

2. See the `./demo-scenes/wrong-format-spec.yaml` file for a spec that violates spectral linting errors
