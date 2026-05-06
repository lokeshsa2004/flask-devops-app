# GitHub Actions Docker Build Fix

## ❌ Problem

The Docker build was failing with:
```
ERROR: failed to build: invalid tag "ghcr.io/lokeshsa2004/flask-devops-app:-f268285": invalid reference format
```

## 🔍 Root Cause

The metadata action was generating invalid tag formats with:
```
type=sha,prefix={{branch}}-
```

This created tags like `-f268285` (with leading dash) which is invalid Docker tag format.

## ✅ Solution Applied

### Changed Tag Format

**BEFORE:**
```yaml
tags: |
  type=ref,event=branch
  type=semver,pattern={{version}}
  type=semver,pattern={{major}}.{{minor}}
  type=sha,prefix={{branch}}-
```

**AFTER:**
```yaml
tags: |
  type=ref,event=branch
  type=semver,pattern={{version}}
  type=semver,pattern={{major}}.{{minor}}
  type=sha
  type=raw,value=latest,enable={{is_default_branch}}
```

### Fixed Push Condition

**BEFORE:**
```yaml
push: ${{ github.event_name != 'pull_request' }}
```

**AFTER:**
```yaml
push: ${{ github.event_name != 'pull_request' && github.ref == 'refs/heads/master' }}
```

This ensures images are only pushed on master branch, not on all branches.

### Removed Hard Dependency

**BEFORE:**
```yaml
test-image:
  needs: build
  if: github.event_name == 'pull_request'
```

**AFTER:**
```yaml
test-image:
  if: github.event_name == 'pull_request'
```

Test image job now builds independently for PRs.

## 📋 Valid Tags Generated

Now the workflow will generate valid tags like:
- `ghcr.io/lokeshsa2004/flask-devops-app:master` (branch)
- `ghcr.io/lokeshsa2004/flask-devops-app:sha-f268285f9da7` (commit SHA)
- `ghcr.io/lokeshsa2004/flask-devops-app:latest` (on master branch)
- `ghcr.io/lokeshsa2004/flask-devops-app:v1.0.0` (on version tags)

## ✨ Next Steps

1. Push the fixed workflow:
```bash
git add .github/workflows/docker-build-push.yml
git commit -m "fix: Fix Docker build tag format in GitHub Actions workflow"
git push origin master
```

2. The workflow should now work correctly on next push!

