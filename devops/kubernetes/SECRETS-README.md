# Kubernetes Secrets Management

## ⚠️ Important: API Keys Are Not In Git

For security, the real API keys are **NOT** committed to GitHub. They are stored in `secrets-production.yaml` which is gitignored.

## How to Deploy Secrets

### Option 1: Apply secrets-production.yaml directly (Recommended for Production)

```bash
# From Jenkins or your local machine with kubectl configured:
kubectl apply -f devops/kubernetes/secrets-production.yaml
```

### Option 2: Create secret from command line

```bash
kubectl create secret generic backend-secrets \
  --namespace=cinereads \
  --from-literal=OPENAI_API_KEY="your-groq-api-key" \
  --from-literal=HARDCOVER_API_KEY="your-hardcover-api-key" \
  --from-literal=OPENAI_BASE_URL="https://api.groq.com/openai/v1" \
  --from-literal=GPT_MODEL="llama-3.3-70b-versatile"
```

### Option 3: Use Jenkins credentials (CI/CD Pipeline)

The Jenkinsfile will automatically create the secret from Jenkins credentials during deployment.

## File Structure

- `configmap.yaml` - Configuration with **placeholder** API keys (safe to commit to Git)
- `secrets-production.yaml` - Real API keys (gitignored, **never commit**)
- `backend-deployment.yaml` - References the secret created by one of the above methods

## Verification

Check if secrets are properly deployed:

```bash
kubectl get secrets -n cinereads
kubectl describe secret backend-secrets -n cinereads
```

## Security Best Practices

1. ✅ Never commit `secrets-production.yaml` to Git
2. ✅ Store production secrets in Jenkins credentials or external secret management
3. ✅ Use different API keys for development/staging/production
4. ✅ Rotate API keys regularly
5. ✅ Use RBAC to restrict access to secrets in Kubernetes
