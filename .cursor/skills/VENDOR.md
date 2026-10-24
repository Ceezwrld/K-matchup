# Vendored Superpowers skills

Source: [obra/superpowers](https://github.com/obra/superpowers)  
Upstream commit: `44c9b2d6e889982ac18c27d05a19fefe335194e1`  
Plugin version: 6.2.0  
License: MIT (see `LICENSE-superpowers`)

These skills are vendored so Cursor Cloud Agents (and other agents that load
project skills from `.cursor/skills/`) can use Superpowers without a
Marketplace plugin install.

## Skills included

- brainstorming
- dispatching-parallel-agents
- executing-plans
- finishing-a-development-branch
- receiving-code-review
- requesting-code-review
- subagent-driven-development
- systematic-debugging
- test-driven-development
- using-git-worktrees
- using-superpowers
- verification-before-completion
- writing-plans
- writing-skills

## Usage

In Agent chat, type `/` and select a skill (for example `/brainstorming` or
`/systematic-debugging`), or ask the agent to use a named Superpowers skill.

To refresh from upstream:

```bash
git clone --depth 1 https://github.com/obra/superpowers.git /tmp/superpowers
rm -rf .cursor/skills/*
cp -a /tmp/superpowers/skills/. .cursor/skills/
cp /tmp/superpowers/LICENSE .cursor/skills/LICENSE-superpowers
# then update this VENDOR.md commit SHA / version
```
