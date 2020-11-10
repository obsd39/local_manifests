#!/usr/bin/python3

import os
import sys
try:
    from github import Github
    from github import GithubException
except ImportError:
    print("Please install the pygithub package via pip3")
    exit(1)
e = os.environ.copy()
# Environment variables for github username and api token
try:
    u = e["GHUSER"]
    p = e["GHTOKEN"]
except KeyError:
    print("Please set the GHUSER and GHTOKEN environment variables")
    exit(1)

orgName = "obsd39"
org = Github(u, p).get_user(orgName)
cr_branch = "cr-11.0"

file = open("vendor.xml", "w")
file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
file.write("<manifest>\n")

file.write("  <remote  name=\"vendor\"\n")
file.write("           fetch=\"https://github.com/\"\n")
file.write("           revision=\"refs/heads/" + cr_branch + "\"\n")
file.write("           sync-c=\"true\"\n")
file.write("           sync-j=\"8\" />\n")

repos = []

for repo in org.get_repos():
    if repo.full_name.find("proprietary_vendor") != -1:
        # Only add repos with the correct branch present
        try:
            repo.get_branch(branch=cr_branch)
            repos.append(repo.full_name)
        except GithubException:
            # Skip the repo, we don't have the branch we want
            continue

for repo in sorted(repos):
    # Repo name is obsd39/proprietary_vendor_$vendor
    # split on "_" and grab the last one
    vendor = repo.split('proprietary_vendor_')[-1].replace('_','/')
    file.write("  <project name=\"" + repo + "\" path=\"vendor/" + vendor +
            "\" remote=\"vendor\" />\n")

file.write("</manifest>\n")
file.close()
