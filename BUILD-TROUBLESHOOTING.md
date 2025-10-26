# 🔧 Deployment Troubleshooting - First Build Failed

## What Happened

Your first Jenkins build failed with these issues:

### 1. ❌ Docker Build Timeout (FIXED)
**Error**: `Timeout has been exceeded` during backend Docker build
**Cause**: Jenkins t2.micro instance (1GB RAM) took too long downloading Python dependencies
**Fix Applied**:
- ✅ Increased Jenkins timeout from 30 to 60 minutes
- ✅ Added pip install timeout and retry flags: `--timeout=1000 --retries=5`
- ✅ Committed to GitHub: `a4c426a`

### 2. ⚠️ Cloudflare 521 Error (EXPECTED)
**Error**: "Web server is down Error code 521" at cinereads.dhanushranga1.dev
**Cause**: No application deployed yet (build failed before deployment stage)
**Status**: This is NORMAL - will be fixed after successful build

### 3. ✅ k3s Cluster Health (VERIFIED)
```
NAME                     STATUS   ROLES                  AGE
cinereads-k3s-worker-1   Ready    <none>                 18h
cinereads-k3s-control    Ready    control-plane,master   18h
```
**Status**: Both nodes Running, cluster operational

---

## ✅ Next Steps - Retry Build (5 minutes)

### Option 1: Jenkins UI (Recommended)
1. Go to Jenkins: http://15.207.32.48:8080
2. Click **cinereads-pipeline**
3. Click **Build Now** (left sidebar)
4. Click on build **#2** in Build History
5. Click **Console Output** to watch progress

**Expected Duration**: 15-20 minutes (first successful build downloads all dependencies)

### Option 2: Alternative - Build Locally Then Deploy

If Jenkins keeps timing out on t2.micro, you can build images locally and push them:

```bash
# Build backend locally
cd backend
docker build -t ghcr.io/dhanushranga1/cinereads-backend:latest .
docker login ghcr.io -u Dhanushranga1 -p <your-github-pat>
docker push ghcr.io/dhanushranga1/cinereads-backend:latest

# Build frontend locally
cd ../frontend
docker build -t ghcr.io/dhanushranga1/cinereads-frontend:latest .
docker push ghcr.io/dhanushranga1/cinereads-frontend:latest

# Deploy to k3s from Jenkins server
ssh ubuntu@15.207.32.48
cd /tmp
git clone https://github.com/Dhanushranga1/CineReads.git
cd CineReads/devops/kubernetes

# Create secrets manually
kubectl create namespace cinereads
kubectl create secret generic backend-secrets \
  --namespace=cinereads \
  --from-literal=OPENAI_API_KEY="<your-groq-key>" \
  --from-literal=HARDCOVER_API_KEY="<your-hardcover-key>" \
  --from-literal=OPENAI_BASE_URL="https://api.groq.com/openai/v1" \
  --from-literal=GPT_MODEL="llama-3.3-70b-versatile"

# Deploy
kubectl apply -f namespace.yaml
kubectl apply -f configmap.yaml
kubectl apply -f backend-deployment.yaml
kubectl apply -f frontend-deployment.yaml
kubectl apply -f ingress.yaml

# Check status
kubectl get pods -n cinereads --watch
```

---

## 🔍 Monitoring Build #2

Watch for these stages in Console Output:

1. ✅ **Checkout** - Should complete in 10s
2. ⏳ **Build Backend** - Will take 10-15 minutes (downloading Python packages)
3. ⏳ **Build Frontend** - Will take 5-10 minutes (npm install + build)
4. ✅ **Test Backend** - Should complete in 30s
5. ✅ **Test Frontend** - Should complete in 20s
6. ✅ **Push Images** - Will take 2-3 minutes (uploading to ghcr.io)
7. ✅ **Deploy to k3s** - Will take 2-3 minutes (kubectl apply + rollout)
8. ✅ **Verify** - Should complete in 30s

**Total Expected Time**: ~20 minutes

---

## 🎯 Success Indicators

When build #2 succeeds, you'll see:

### Jenkins Console Output:
```
✅ PIPELINE COMPLETED SUCCESSFULLY! 🎉
Application deployed to: http://cinereads.dhanushranga1.dev
```

### Browser Test:
- Visit: http://cinereads.dhanushranga1.dev
- Should see: CineReads landing page (NOT Cloudflare 521 error)

### Kubernetes Check:
```bash
ssh ubuntu@15.207.32.48
kubectl get pods -n cinereads

# Expected output:
NAME                        READY   STATUS    RESTARTS   AGE
backend-xxxxx-xxxxx        1/1     Running   0          2m
backend-xxxxx-xxxxx        1/1     Running   0          2m
frontend-xxxxx-xxxxx       1/1     Running   0          2m
frontend-xxxxx-xxxxx       1/1     Running   0          2m
```

---

## ⚠️ If Build #2 Also Times Out

The t2.micro instance might be too small for Docker builds. Consider:

### Option A: Upgrade Jenkins EC2 (Cost: +$5/month)
```bash
# Stop instance, change to t3.small (2GB RAM), start again
aws ec2 stop-instances --instance-ids <instance-id>
aws ec2 modify-instance-attribute --instance-id <instance-id> --instance-type t3.small
aws ec2 start-instances --instance-ids <instance-id>
```

### Option B: Build Locally (Free)
Use "Option 2" above to build on your laptop and push to registry

### Option C: Use GitHub Actions (Free)
Move CI/CD to GitHub Actions (included in free tier, faster builders)

---

## 📊 Current Status

- ✅ Infrastructure: 100% operational (Jenkins + k3s cluster)
- ✅ Code: 100% ready (Dockerfiles, manifests, Jenkinsfile)
- ✅ Fixes: Committed to GitHub
- ⏳ Deployment: Waiting for successful Jenkins build

**Next Action**: Click "Build Now" in Jenkins and wait ~20 minutes for first successful build! 🚀
