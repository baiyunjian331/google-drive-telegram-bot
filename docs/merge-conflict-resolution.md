# "Switch user prompts to Chinese #2" Merge Conflict Resolution Guide

This guide walks maintainers through clearing the remaining merge conflicts in the
`Switch user prompts to Chinese #2` branch. The conflicts appear in files that
touch user-facing copy, so make sure the final text keeps the Chinese prompts while
retaining any upstream fixes.

## 1. Prepare the branch

```sh
git checkout "Switch user prompts to Chinese"
git pull --rebase
```

If a dedicated follow-up branch (for example `Switch user prompts to Chinese #2`)
exists, substitute that branch name in the commands above. Once checked out, run:

```sh
git status
```

Confirm that Git reports conflicts in the following files:

- `README.md`
- `bot/config.py`
- `bot/plugins/authorize.py`
- `bot/plugins/download.py`

## 2. Resolve each conflicted file

Open every conflicted file and search for the conflict markers (`<<<<<<<`, `=======`,
`>>>>>>>`). Decide which portions to keep so that:

- The Chinese translations from the localization change remain intact.
- Any new instructions or fixes from the upstream branch are preserved.
- Duplicate guidance or outdated English text is removed.

For quick reference, here is what each file should look like once the markers are
gone:

- **`README.md`** – keep the feature checklist item `中文界面提示与指引。` and retain
  the Replit deployment section introduced upstream. If the README pulled in
  updates from `main`, make sure both the English content and the localized bullet
  coexist cleanly without duplicated headings.
- **`bot/config.py`** – ensure the `Messages` class contains the full set of
  Chinese prompts (欢迎语、帮助文本、报错提示等). No raw conflict markers or leftover
  English fallbacks should remain.
- **`bot/plugins/authorize.py`** – keep the localized replies for `/auth` and the
  `_token` handler, including the friendly messages for missing codes or flows.
- **`bot/plugins/download.py`** – keep the Chinese guidance messages for missing
  URLs and download status updates, along with the helper that parses custom file
  names.

Edit the files to remove the conflict markers and polish the final Chinese wording
if needed. The `download.py` and `authorize.py` handlers should continue to use the
localized prompts you recently introduced.

### Handling competing line changes

When Git reports *"both modified"* or *"Merge conflict in … (content):
Merge conflict in … (content): Merge conflict (content): merge conflict in …"* it
means both branches edited the same lines. Use the three-way diff views to inspect
each version before choosing what to keep:

```sh
git diff --base bot/plugins/authorize.py    # original file before either change
git diff --ours bot/plugins/authorize.py    # your branch (localized Chinese prompts)
git diff --theirs bot/plugins/authorize.py  # upstream branch you merged in
```

For a quick look at just the conflicting hunks inside your editor, you can also run
`git mergetool` or rely on IDE merge tools such as VS Code's *Accept Current/Accept
Incoming* buttons. Keep the localized Chinese copy from your branch, fold in any
upstream wording or fixes, and delete the conflict markers.

If you determine that an entire file should prefer one side, you can accept it all at
once using:

```sh
# Keep your localized version and discard upstream changes for this file
git checkout --ours bot/plugins/download.py

# Or keep the upstream version and discard your edits
git checkout --theirs bot/plugins/download.py
```

Afterwards reapply the necessary Chinese translations (if any were overwritten), save
the file, and stage it again with `git add`.

## 3. Stage and commit the resolution

After every marker has been removed, stage and commit the files:

```sh
git add README.md bot/config.py bot/plugins/authorize.py bot/plugins/download.py
git commit -m "Resolve merge conflicts for Switch user prompts to Chinese"
```

If you are in the middle of a merge, Git may instead prompt you to run
`git commit` without arguments to complete the merge commit.

## 4. Verify the bot still works

Run quick checks before pushing:

```sh
python -m compileall bot
```

Optionally run any other linters or functional tests you rely on. Once the commands
finish successfully, push the branch to update the pull request.

```sh
git push
```

The pull request should now show as conflict-free with the fully localized Chinese
prompts intact.
