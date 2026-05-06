# GitHub Actions Setup Guide

## Overview

This project includes 3 GitHub Actions workflows:

1. **ci.yml** - Tests, Linting, and EC2 Deployment
2. **docker-build-push.yml** - Docker image building and GHCR publishing
3. **notify.yml** - Status notifications (part of ci.yml)

---

## Required GitHub Secrets

### Step 1: Access GitHub Secrets Settings

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"**

### Step 2: Add Required Secrets

| Secret Name | What It Is | How to Get It |
|-------------|-----------|---------------|
| `EC2_HOST` | Public IP or domain of EC2 instance | From AWS Console or `ec2-xx-xx-xx-xx.compute-1.amazonaws.com` |
| `EC2_USER` | SSH username to connect to EC2 | Usually `ubuntu` for Ubuntu AMI |
| `EC2_KEY` | Private SSH key (.pem file) content | From AWS Console when launching instance |
| `GHCR_TOKEN` | GitHub Personal Access Token | Generate from GitHub Settings |

### Step 3: Getting Your EC2_KEY

#### If you already have the .pem file:

**On Windows (PowerShell):**
```powershell
# Read the PEM file content
$keyContent = Get-Content -Path "C:\path\to\your-key.pem" -Raw
$keyContent | Set-Clipboard

# Now paste in GitHub secret
```

**On Mac/Linux:**
```bash
cat /path/to/your-key.pem | pbcopy
# Now paste in GitHub secret
```

#### If you don't have the .pem file:

1. Go to AWS Console → EC2 → Key pairs
2. Download your key pair (if available)
3. Or create a new key pair and re-launch instance

### Step 4: Getting Your GHCR_TOKEN

1. Go to https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Give it a name: `GHCR_TOKEN`
4. Set expiration: 90 days (or custom)
5. Select scopes:
   - ✅ `write:packages`
   - ✅ `read:packages`
   - ✅ `delete:packages`
6. Click **"Generate token"**
7. Copy and save immediately (won't show again)
8. Add as `GHCR_TOKEN` secret in repository

---

## Workflow Triggers

### CI Workflow (ci.yml)
- Triggers on: Push to `master` branch or Pull Requests
- Runs: Test → Lint → Deploy → Notify

### Docker Build Workflow (docker-build-push.yml)
- Triggers on: Push to `master` or PR
- Automatically tags with: `branch-name`, `version` tags, `commit-sha`
- Pushes to GHCR if: Not a PR

---

## Secrets Configuration Examples

### Example EC2_HOST
```
203.0.113.42
# or
ec2-203-0-113-42.compute-1.amazonaws.com
```

### Example EC2_USER
```
ubuntu
```

### Example EC2_KEY
```
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA2x8N5h...
(full key content)
-----END RSA PRIVATE KEY-----
```

### Example GHCR_TOKEN
```
ghp_abc123defghi456jklmno789pqrst012uvwxyz
```

---

## Workflow Files Location

All workflow files are in: `.github/workflows/`

```
.github/
└── workflows/
    ├── ci.yml                   # Main CI/CD pipeline
    └── docker-build-push.yml    # Docker build and push
```

---

## Manual Workflow Triggers (if needed)

If you need to manually trigger a workflow:

1. Go to **Actions** tab in repository
2. Select the workflow from left sidebar
3. Click **"Run workflow"** button
4. Choose branch and click **"Run workflow"**

---

## Troubleshooting

### Deploy Job Fails with "Permission denied (publickey)"

**Solution:**
- Verify `EC2_KEY` secret contains complete PEM key
- Ensure `EC2_USER` is correct (usually `ubuntu`)
- Check EC2 security group allows SSH (port 22)

### Docker Build Fails

**Solution:**
- Check logs in Actions tab
- Verify Dockerfile has no syntax errors
- Ensure all files referenced in COPY exist

### GHCR Push Fails with "denied"

**Solution:**
- Generate new GHCR_TOKEN with correct scopes
- Verify token has `write:packages` scope
- Token may have expired (regenerate)

### EC2 Deployment Timeout

**Solution:**
- Verify EC2 instance is running
- Check EC2 security group (SSH port 22 must be open)
- Test SSH connection manually first

---

## Monitoring Workflow Runs

1. Go to **Actions** tab in repository
2. See all workflow runs with status (✅ success, ❌ failed, ⏳ running)
3. Click on a run to see detailed logs
4. Scroll through individual job logs for troubleshooting

---

## Next Steps

1. ✅ Add all 4 secrets to repository
2. ✅ Test CI workflow with a git push
3. ✅ Verify Docker image builds and pushes to GHCR
4. ✅ Test deployment to EC2
5. ✅ Monitor workflow runs in Actions tab

---

## Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| "Workflow not triggered" | Event not matched | Ensure you're pushing to `master` branch |
| "Deploy job skipped" | Test/lint failed | Fix failing tests first |
| "SSH connection failed" | Invalid credentials | Verify all 3 EC2 secrets are correct |
| "Docker image not pushed" | PR workflow | Secrets only available on `master` branch pushes |
| "Curl command not found" | Container issue | Ensure Ubuntu image includes curl or use different health check |

---

## Health Checks

After successful deployment, verify:

```bash
# SSH into EC2
ssh -i your-key.pem ubuntu@<EC2_HOST>

# Check Gunicorn
sudo systemctl status flask_app

# Check Nginx
sudo systemctl status nginx

# Test Flask app
curl http://127.0.0.1:8000/

# Test through Nginx
curl http://localhost/
```

