# Branch Protection

The workflows define two required checks for `main`:

- `critical-backend-tests`
- `full-regression`

Apply the checked-in branch protection payload with:

```bash
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  /repos/loobo07/job_hunt/branches/main/protection \
  --input .github/branch-protection/main.json
```

The same settings can be applied through GitHub's UI under:

`Settings -> Branches -> Branch protection rules -> main`

Require pull requests before merging, require the two status checks above, require branches to be up to date before merging, require conversation resolution, require linear history, disallow force pushes, and disallow deletions.

## Current Hosting Constraint

GitHub returned HTTP 403 when applying this rule while the repository was private:

```text
Upgrade to GitHub Pro or make this repository public to enable this feature.
```

To enforce `main` protection, either upgrade the repository owner/account to a plan that supports branch protection for private repositories, make the repository public, or apply equivalent protection after moving the code to a repository where branch protection is available.
