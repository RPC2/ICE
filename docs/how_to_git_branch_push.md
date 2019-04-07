Taking the branch `zhijing` as an example.

## (Step 1) Create a branch
```bash
git checkout -b zhijing develop

# update all remote tracking branches, and the currently checked out branch
git pull

# switch to that branch (line of development)
git checkout zhijing

# push changes to github
git push --set-upstream origin zhijing

```
## (Step 2) Make changes in the branch

```bash
# make changes, for example, edit `file1.md` and `file2.md` using the text editor

# stage the changed files
git add file1.md file2.md

# take a snapshot of the staging area (anything that's been added)
git commit -m "my snapshot"

# push changes to github
git push origin zhijing
```
## (Step 3) Merge in 2 directions

#### Merge_Direction_1: update zhijing with the `new changes in master`
```bash
git checkout zhijing
git pull
git merge master
git push origin zhijing
```

#### Merge_Direction_2: merge the `new changes in zhijing` to master
```bash
git checkout master
git merge --no-ff zhijing
git push origin master
```