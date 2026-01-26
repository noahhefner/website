---
title: "Librebooting a Dell OptiPlex 3050 Micro"
date: 2026-01-25T08:51:17-05:00
draft: true
---

- what is libreboot

- dell optiplex 3050 micro
- needs proprietary blobs. can either inject them into prebuilt rom or build from source and have the build pipeline do it for you. i opted to build from source

- installation
  - clone git repo
  - install deps w/ m
  - first build failed
    - missed some aur packages
  - couldnt get flashprog to build, so I used flashrom instead

- massive improvement in boot times

- docker image for build process?