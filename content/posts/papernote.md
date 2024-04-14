---
title: "Papernote"
date: 2024-04-13T18:46:40-05:00
draft: true
---

I've tried a lot of note taking applications. Ive used Google Keep, [Standard Notes](https://standardnotes.com/), [Joplin](https://joplinapp.org/), and more recently, [Flatnotes](https://github.com/Dullage/flatnotes). All of these options (minus Google Keep) have a few common traits. They are all **self-hostable**, **open-source**, and **support markdown**. Going forward, any note taking application I use must support these three key features.

I've really enjoyed Flatnotes. It has one key feature that made me move away from Joplin: **plain markdown file storage**. Unlike Joplin which stores note data in an SQL database, Flatnotes reads and writes data directly to markdown files stored on the server. This makes it incredibly easy to move notes in and out of the server and very easy to backup notes by keeping them in a Docker volume. There is nothing locking your notes into the application.

Flatnotes is not without its flaws though. I'm not a fan of the list view as it does not make efficient use of the users vertical screen real estate. The home screen - it's just a search bar, no list view of your notes. I tend to use my notes more for long term storage / archival purposes, so while the search function is nice, it's not a super valuable feature for my use case.

![flatnotes](/images/papernote/flatnotes-screenshots.png)

So I decided to build my own note taking application, taking into consideration my use case and building on the features that I loved about Flatnotes. I could have just forked it and built a new frontend, but where's the fun in that? I decided to build my app from the ground up using Golang on the backend and HTMX on the frontend. This turned out to be a fantastic choice, not just because the tools are cool and powerful, but also as a learning opportunity.

I have very little web development experience. I've built a few apps in React and Vue.js, but that's about it. What I did not know before starting this project was how little I actually knew about web development. Until I began to learn how to use HTMX, I essentially thought everything on the web was built using enormous Javascript frameworks like React, Angular, or something else of the like. "Single Page Applications" (SPA's) was all I knew.

Learning HTMX required that I also learn about the history of web development and how far modern web apps have strayed from the original vision of REST. I won't dive too deep into mission of HTMX in this article, but I highly reccommend reading Chapter 1 from [Hypermedia Systems](https://hypermedia.systems/hypermedia-reintroduction/), the free user manual for HTMX, for a deeper explanation. In a nutshell: Most modern web apps make heavy use of enormous client-side Javascript frameworks such as React, Angular, or Vue. In this model, the client-server interraction is reduced merely to exchanging JSON information. The server manages all the data while the client does all the front-end legwork. HTMX harkens back to simpler days of web development by leaning into server-side rendering for dynamic application behavior. The server is responsible both for data management and controlling the front-end state. Some may argue that this approach is less flexible, but it has the benefit of reduced client-side complexity and an overall simpler application architecture.

For my backend, I chose Golang because it supports all the tooling I need and seems to pair well with HTMX. (Also I just wanted to learn Go.) A cool side effect of using HTMX is that you can pretty much use whatever language you want in the backend, as long as it has support for building an HTTP server and HTML templating. 

So without further ado, I would like to introduce Papernote - a self-hostable, markdown-driven, (almost) database-less note taking web application, built on HTMX and Golang. It is very basic, but I think it's at a good MVP state at this point. The markdown editor especially lacks a lot of features that other note apps have, such as a "ribbon" for inserting things like tables, bold text, itallic, images, etc. But this was an intentional choice as I wanted to have a few dependencies as possible. I skipped using any CSS libraries as well. The only dependency is HTMX.






















