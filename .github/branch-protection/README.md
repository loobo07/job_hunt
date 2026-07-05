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
