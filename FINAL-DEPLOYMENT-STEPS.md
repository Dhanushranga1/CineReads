# 🚀 Final Deployment Steps - CineReads

## 📋 What's Ready

✅ **Infrastructure (100% Complete)**
- AWS Jenkins EC2: http://15.207.32.48:8080
- k3s Cluster: 2 nodes (control + worker) in DigitalOcean
- Cloudflare DNS: cinereads.dhanushranga1.dev → k3s cluster
- All services operational and tested

✅ **Code (100% Complete)**  
- Backend Dockerfile with Python 3.13 and health checks
- Frontend Dockerfile with Node 20 multi-stage build
- Kubernetes manifests (namespace, configmap, deployments, ingress)
- Jenkinsfile with complete CI/CD pipeline (8 stages)
- All code pushed to GitHub

✅ **Files You Have**
- k3s kubeconfig: `~/Downloads/k3s-kubeconfig.yaml` (ready to upload)
- Production secrets: `devops/kubernetes/secrets-production.yaml` (gitignored)

---

## 🎯 Next Steps (30 minutes to live deployment)

### Step 1: Upload k3s Kubeconfig to Jenkins (2 minutes)

1. Open Jenkins: http://15.207.32.48:8080
2. Navigate: **Manage Jenkins** → **Credentials** → **System** → **Global credentials (unrestricted)**
3. Click **Add Credentials**
4. Fill in:
   - **Kind**: `Secret file`
   - **File**: Choose `~/Downloads/k3s-kubeconfig.yaml`
   - **ID**: `k3s-kubeconfig` (MUST BE EXACT - Jenkins pipeline uses this ID)
   - **Description**: `k3s Cluster Configuration`
5. Click **Create**

**Verify**: You should see the credential in the list with Kind = "Secret file"

---

### Step 2: Add API Keys as Jenkins Credentials (3 minutes)

#### 2a. Add Groq API Key

1. In Jenkins Credentials page, click **Add Credentials**
2. Fill in:
   - **Kind**: `Secret text`
   - **Secret**: `<your-groq-api-key-from-backend-.env>`
   - **ID**: `groq-api-key` (MUST BE EXACT)
   - **Description**: `Groq API Key for LLM`
3. Click **Create**

#### 2b. Add Hardcover API Key

1. Click **Add Credentials** again
2. Fill in:
   - **Kind**: `Secret text`
   - **Secret**: `<your-hardcover-bearer-token-from-backend-.env>`
   - **ID**: `hardcover-api-key` (MUST BE EXACT)
   - **Description**: `Hardcover API Key for Book Data`
3. Click **Create**

**Verify**: You should now have 4 credentials:
- `github-registry` (Username with password) ✅ Already exists
- `k3s-kubeconfig` (Secret file) ✅ Just added
- `groq-api-key` (Secret text) ✅ Just added
- `hardcover-api-key` (Secret text) ✅ Just added

---

### Step 3: Create Jenkins Pipeline Job (3 minutes)

1. Go to Jenkins home: http://15.207.32.48:8080
2. Click **New Item**
3. Fill in:
   - **Name**: `cinereads-pipeline`
   - **Type**: Select **Pipeline**
4. Click **OK**

5. In the configuration page:

   **General Section:**
   - ✅ Check **GitHub project**
   - Project url: `https://github.com/Dhanushranga1/CineReads`

   **Build Triggers Section:** (Optional - for auto-deploy on push)
   - ✅ Check **GitHub hook trigger for GITScm polling**

   **Pipeline Section:**
   - Definition: **Pipeline script from SCM**
   - SCM: **Git**
   - Repository URL: `https://github.com/Dhanushranga1/CineReads.git`
   - Branch Specifier: `*/main`
   - Script Path: `Jenkinsfile`

6. Click **Save**

**Verify**: You should see "cinereads-pipeline" in the Jenkins dashboard

---

### Step 4: Run First Deployment (10-15 minutes - AUTOMATED)

1. Click on **cinereads-pipeline** in Jenkins dashboard
2. Click **Build Now** (left sidebar)
3. Click on build **#1** in Build History
4. Click **Console Output** to watch logs

**What will happen automatically:**

1. 🔍 **Checkout** - Clone repo from GitHub
2. 🔨 **Build Backend** - Create Docker image for FastAPI
3. 🔨 **Build Frontend** - Create Docker image for Next.js
4. 🧪 **Test Backend** - Run pytest in container
5. 🧪 **Test Frontend** - Run npm lint
6. 📦 **Push Images** - Upload to ghcr.io/dhanushranga1/
7. 🚀 **Deploy to k3s** - Apply Kubernetes manifests
8. ✅ **Verify** - Check health endpoints

**Expected Duration**: 10-15 minutes (first build downloads dependencies)

**Success Message**: `✅ PIPELINE COMPLETED SUCCESSFULLY! 🎉`

---

### Step 5: Verify Deployment (2 minutes)

#### Check Kubernetes Pods

```bash
# SSH to Jenkins server
ssh -i ~/.ssh/id_ed25519_do ubuntu@15.207.32.48

# Check all resources
kubectl get all -n cinereads

# Expected output:
# NAME                           READY   STATUS    RESTARTS   AGE
# pod/backend-xxxxx-xxxxx       1/1     Running   0          2m
# pod/backend-xxxxx-xxxxx       1/1     Running   0          2m
# pod/frontend-xxxxx-xxxxx      1/1     Running   0          2m
# pod/frontend-xxxxx-xxxxx      1/1     Running   0          2m

# Check logs if needed
kubectl logs -f deployment/backend -n cinereads
kubectl logs -f deployment/frontend -n cinereads
```

#### Test the Application

Open in browser:
- **Frontend**: http://cinereads.dhanushranga1.dev
- **API Docs**: http://cinereads.dhanushranga1.dev/docs
- **Health Check**: http://cinereads.dhanushranga1.dev/api/health

Or use curl:
```bash
curl http://cinereads.dhanushranga1.dev/api/health
# Expected: {"status":"healthy","timestamp":"..."}

curl http://cinereads.dhanushranga1.dev
# Expected: HTML page with Next.js content
```

---

## 🎉 Success Criteria

Your deployment is successful when:
- ✅ All 4 pods show `Running` status (2 backend + 2 frontend)
- ✅ Health endpoint returns `{"status":"healthy"}`
- ✅ Frontend loads at http://cinereads.dhanushranga1.dev
- ✅ You can search for a movie and get book recommendations

---

## 🔧 Troubleshooting

### If Jenkins build fails:

**Check credentials:**
```bash
# In Jenkins Console Output, look for:
# "ERROR: Could not find credentials with ID 'xxx'"
```
Solution: Verify credential IDs are EXACTLY:
- `k3s-kubeconfig` (Secret file)
- `groq-api-key` (Secret text)
- `hardcover-api-key` (Secret text)
- `github-registry` (Username with password)

**Check Docker login:**
```bash
# In Console Output, look for:
# "Error response from daemon: Get https://ghcr.io/..."
```
Solution: Verify `github-registry` credential has your GitHub PAT with `write:packages` permission

**Check kubectl access:**
```bash
# In Console Output, look for:
# "The connection to the server ... was refused"
```
Solution: Verify k3s-kubeconfig file is correct and cluster is running:
```bash
ssh ubuntu@15.207.32.48
kubectl get nodes  # Should show 2 nodes Ready
```

### If pods won't start:

**Check pod status:**
```bash
kubectl get pods -n cinereads
kubectl describe pod <pod-name> -n cinereads
```

**Common issues:**
- `ImagePullBackOff`: Docker image not pushed or wrong image name
  - Check: `docker images | grep cinereads` on Jenkins
  - Check: Jenkins Console Output for push errors
  
- `CrashLoopBackOff`: Container starting but crashing
  - Check logs: `kubectl logs <pod-name> -n cinereads`
  - Common cause: Missing environment variables or wrong API keys

- `Pending`: Not enough resources
  - Check: `kubectl describe node` for resource usage
  - Solution: Reduce replicas from 2 to 1 in deployments

### If application doesn't respond:

**Check ingress:**
```bash
kubectl get ingress -n cinereads
kubectl describe ingress cinereads -n cinereads
```

**Check service endpoints:**
```bash
kubectl get svc -n cinereads
kubectl get endpoints -n cinereads
```

**Test directly from cluster:**
```bash
# SSH to control plane
ssh ubuntu@206.189.140.246

# Test backend directly
curl http://<backend-pod-ip>:8000/health

# Test frontend directly
curl http://<frontend-pod-ip>:3000
```

---

## 📊 Monitoring Commands

```bash
# Watch pods in real-time
kubectl get pods -n cinereads --watch

# Check resource usage
kubectl top nodes
kubectl top pods -n cinereads

# View logs (follow)
kubectl logs -f deployment/backend -n cinereads
kubectl logs -f deployment/frontend -n cinereads

# Check recent events
kubectl get events -n cinereads --sort-by='.lastTimestamp'

# Check ingress status
kubectl get ingress -n cinereads -o wide
```

---

## 🔄 Making Changes (Future Deployments)

After initial deployment, any push to `main` branch will:
1. Trigger Jenkins build automatically (if webhook configured)
2. Run full pipeline (build → test → push → deploy)
3. Update pods with zero-downtime rolling update

**Manual trigger:**
- Go to Jenkins → cinereads-pipeline → Build Now

**Rollback if needed:**
```bash
kubectl rollout undo deployment/backend -n cinereads
kubectl rollout undo deployment/frontend -n cinereads
```

---

## 🎯 What You've Built

**Hybrid Multi-Cloud Infrastructure:**
- AWS EC2 (Jenkins CI/CD)
- DigitalOcean (k3s Kubernetes cluster)
- Cloudflare (DNS + CDN)

**Full Production Stack:**
- FastAPI backend with Groq LLM (Llama 3.3 70B)
- Next.js 15 frontend with React 19
- Kubernetes with Traefik ingress
- Docker containerization
- Automated CI/CD pipeline

**Cost**: ~$20/month (Jenkins $5, k3s control $6, worker $6, minimal data transfer)

**Scalability**: Can handle 100s of requests/second with current setup. Scale by:
- Increasing replicas: `kubectl scale deployment/backend --replicas=5 -n cinereads`
- Adding worker nodes to k3s cluster
- Upgrading droplet sizes

---

## 📝 Summary Checklist

Before clicking "Build Now":
- [ ] k3s-kubeconfig uploaded to Jenkins ✅
- [ ] groq-api-key added to Jenkins credentials ✅
- [ ] hardcover-api-key added to Jenkins credentials ✅
- [ ] github-registry credential exists (from earlier) ✅
- [ ] Pipeline job created (cinereads-pipeline) ✅
- [ ] All code pushed to GitHub ✅

**You are now ready to deploy! Click "Build Now" and watch the magic happen! 🚀**

---

## 🎊 Post-Deployment Next Steps (Optional)

1. **Enable HTTPS** - Add cert-manager for Let's Encrypt SSL
2. **Add Monitoring** - Install Prometheus + Grafana
3. **Setup GitHub Webhook** - Auto-deploy on every push
4. **Configure Backups** - Backup k3s etcd and application data
5. **Add Staging Environment** - Create `staging` namespace
6. **Performance Tuning** - Adjust resource limits based on usage

**Congratulations! You've built a production-grade AI application infrastructure! 🎉**
