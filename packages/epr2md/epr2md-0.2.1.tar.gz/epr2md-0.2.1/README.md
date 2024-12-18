
[![CircleCI](https://dl.circleci.com/status-badge/img/gh/hasii2011/epr2md/tree/master.svg?style=shield)](https://dl.circleci.com/status-badge/redirect/gh/hasii2011/epr2md/tree/master)
[![PyPI version](https://badge.fury.io/py/epr2md.svg)](https://badge.fury.io/py/epr2md)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

# Introduction

A simple python console script to let me convert [epr](https://github.com/sshaw/export-pull-requests) files to [Markdown](https://www.howtogeek.com/448323/what-is-markdown-and-how-do-you-use-it/).

Typical export-pull-requests file that I generate use the following CLI invocation:

```
epr hasii2011/gittodoistclone --milestone=5 --export=issues --token=myToken --state=closed > release-0.98.0.csv 
```
The various columns are in this format:

```
Repository,Type,#,User,Title,State,Created,Updated,URL
```

A [CSV](https://file.org/extension/csv) line like this:

```
hasii2011/PyUt,Issue,359,hasii2011,Fix warning in PyutLink.setType,closed,03/23/22 09:50:04,03/23/22 13:56:09,https://github.com/hasii2011/PyUt/issues/359
```

Gets converted to a Markdown line like this:

```Markdown
* [359](https://github.com/hasii2011/PyUt/issues/359) Fix warning in PyutLink.setType
```
# Overview

The basic command structure is:

```
Usage: epr2md [OPTIONS]

Options:
  --version               Show the version and exit.
  -i, --input-file TEXT   The input .csv file to convert.  [required]
  -o, --output-file TEXT  The output .md file.
  --help                  Show this message and exit.
```

By default, epr2md assumes that the input file has a `.csv` suffix and the output file has a `.md` suffix. 

However, epr2md is flexible and can deduce file names and suffixes.  The best option is if you do not specify the output file.  Then epr2md deduces that the output file is the same as the input file name with the .md suffix.  For example:

```epr2md -i release-6.5.4.csv```

causes pyut2xml to write to a file named TestFileV10.xml

The command line:

```epr2md -i release-6.5.4 -o release-6.5.4```

reads from release-6.5.4.csv and writes to release-6.5.4.md


Another simple example:

```epr2md -i release-6.5.4```

causes pyut2xml to reads from a file named TestFileV10.csv and write to a file named release-6.5.4.md

# Installation

```pip install epr2md```


___

Written by Humberto A. Sanchez II <mailto@humberto.a.sanchez.ii@gmail.com>, (C) 2024

 

 
## Note
For all kind of problems, requests, enhancements, bug reports, etc.,
please drop me an e-mail.


------


![Humberto's Modified Logo](https://raw.githubusercontent.com/wiki/hasii2011/gittodoistclone/images/SillyGitHub.png)

I am concerned about GitHub's Copilot project


I urge you to read about the
[Give up GitHub](https://GiveUpGitHub.org) campaign from
[the Software Freedom Conservancy](https://sfconservancy.org).

While I do not advocate for all the issues listed there I do not like that
a company like Microsoft may profit from open source projects.

I continue to use GitHub because it offers the services I need for free.  But, I continue
to monitor their terms of service.

Any use of this project's code by GitHub Copilot, past or present, is done
without my permission.  I do not consent to GitHub's use of this project's
code in Copilot.
