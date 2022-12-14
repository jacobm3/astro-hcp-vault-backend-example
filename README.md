# Overview

This repo contains working example files to help connect Astro to HCP Vault and Vault Enterprise, including supporting Vault namespaces and a helper script to generate the required `.env` file for local development. This is supplementary to Astronomer guide is available here:

https://docs.astronomer.io/astro/secrets-backend?tab=hashicorp#setup


# Steps

After you create a publicly-accessible HCP dev cluster and obtain an admin token, follow these steps:

## Setup

```
export VAULT_NAMESPACE=admin
export VAULT_ADDR=https://YOUR-CLUSTER.hashicorp.cloud:8200/

vault login  # provide the admin token from the HCP portal

vault auth enable approle
vault write auth/approle/role/astro_role \
  secret_id_ttl=0 \
  secret_id_num_uses=0 \
  token_num_uses=0 \
  token_ttl=24h \
  token_max_ttl=24h

# output needed in .env file
vault read auth/approle/role/astro_role/role-id 

# output needed in .env file
vault write -f auth/approle/role/astro_role/secret-id  

vault policy write astro_policy - <<EOF
path "secret/*" {
  capabilities = ["create", "read", "update", "patch", "delete", "list"]
}
EOF
```

## Create Secrets

```
vault secrets disable secret
vault secrets enable -path=secret -version=2 kv
vault kv put secret/variables/example-variable value="success"
vault kv put secret/variables/other-variable value="some-secret"

vault kv put secret/connections/<your-connection-id> \   conn_uri=<connection-type>://<connection-login>:<connection-password>@<connection-host>:5432
```

## Setup .env file

```
AIRFLOW__SECRETS__BACKEND=airflow.providers.hashicorp.secrets.vault.VaultBackend
AIRFLOW__SECRETS__BACKEND_KWARGS={"mount_point": "secret", "connections_path": "connections", "variables_path":"variables", "config_path": null, "url": "https://YOUR-CLUSTER.hashicorp.cloud:8200", "namespace": "admin", "auth_type": "approle", "role_id":"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxx", "secret_id":"yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyy"}
```

## Python module requirements

Ensure you include this Python module in requirements.txt:

```
apache-airflow-providers-hashicorp
```

## DAG
Enable the `variable_demo_dag.py` in the Astro UI to see this in action.