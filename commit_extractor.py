#!/usr/bin/python

import sys;
import subprocess;

############# Get Args
cmds = ["hg", "log"];
if len(sys.argv) > 1 :
    cmds += ["-l", sys.argv[1]];

############# Get Logs
p = subprocess.Popen(cmds, stdout=subprocess.PIPE);
str_commits = p.communicate()[0].split("\n");

############# Init
commits = [];
empty = {"user": None, "changeset": None, "description": ""};
description = False;
commit = empty.copy();

############# Parse
for line in str_commits :
    if line.startswith("user:        ") :
        commit["user"] = line[13:];
    elif line.startswith("changeset:   ") :
        commit["changeset"] = line[13:].split(":")[1];
    elif line.startswith("description:") :
        description = True;
    elif description == True and line == "" :
        description = False;
        commits.append(commit);
        commit = empty.copy();
    elif description == True :
        commit["description"] += line;

############# Print
def pretty_print(changeset, user, description):
    print "[\033[93mCOMMIT\033[0m]  \033[93m#"+ changeset +"\t"+ user + "\033[0m";
    print "          "+ description;

for commit in commits :
    pretty_print(commit["changeset"], commit["user"], commit["description"]);
