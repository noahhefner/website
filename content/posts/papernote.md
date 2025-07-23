---
title: "Papernote"
date: 2024-04-13T18:46:40-05:00
draft: true
---

I've tried a lot of note-taking applications. Ive used Google Keep, [Standard Notes](https://standardnotes.com/), [Joplin](https://joplinapp.org/), and more recently, [Flatnotes](https://github.com/Dullage/flatnotes). All of these options (minus Google Keep) have a few common traits. They are all self-hostable, open-source, and support markdown. Going forward, any note-taking application I use must have these three key features.

I've really enjoyed Flatnotes. It has one key feature that made me move away from Joplin which is plain markdown file storage. Unlike Joplin which stores note data in an SQL database, Flatnotes reads and writes data directly to markdown files stored on the server. This makes it incredibly easy to move notes in and out of the server and very easy to back up notes by keeping them in a Docker volume. Nothing is locking your notes into the application.

Flatnotes is not without its flaws though. I'm not a fan of the list view as it does not make efficient use of the users' vertical screen real estate. The home screen - it's just a search bar, with no list view of your notes. I tend to use my notes more for long-term storage / archival purposes, so while the search function is nice, it's not a super valuable feature for my use case.

![flatnotes](/images/papernote/flatnotes-screenshots.png)

So I decided to build my own note-taking application, taking into consideration how I write my notes and building on the features that I loved about Flatnotes. I could have just forked it and built a new front end, but where's the fun in that? I decided to build my app from the ground up using Golang on the backend and HTMX on the front end. This turned out to be a fantastic choice, not just because the tools are cool and powerful, but also as a learning opportunity.

## Learning Web Development History

I have very little web development experience. I've built a few apps in React and Vue.js, but that's about it. What I did not know before starting this project was how little I knew about web development. Until I began to learn how to use HTMX, I essentially thought everything on the web was built using enormous Javascript frameworks like React, Angular, or something else of the like. "Single Page Applications" (SPA's) was all I knew.

Learning HTMX required that I also learn about the history of web development and how far modern web apps have strayed from the original vision of REST. I won't dive too deep into the mission of HTMX in this article, but I highly recommend reading Chapter 1 from [Hypermedia Systems](https://hypermedia.systems/hypermedia-reintroduction/), the free user manual for HTMX, for a deeper explanation. In a nutshell: Most modern web apps make heavy use of enormous client-side Javascript frameworks such as React, Angular, or Vue. In this model, the client-server interaction is reduced merely to exchanging JSON information. The server manages all the data while the client does all the front-end legwork. HTMX harkens back to simpler days of web development by leaning into server-side rendering for dynamic application behavior. The server is responsible both for data management and controlling the front-end state. Some may argue that this approach is less flexible, but it has the benefit of reduced client-side complexity and an overall simpler application architecture.

I chose Golang for the backend because it supports all the tooling I need and seems to pair well with HTMX. (Also I just wanted to learn Go.) A cool side effect of using HTMX is that you can pretty much use whatever language you want in the backend, as long as it has support for building an HTTP server and HTML templating. Flatnotes, for example, is built in Python.

## Papernote

With that, I would like to introduce [Papernote](https://github.com/noahhefner/papernote) - a self-hostable, markdown-driven, (almost) database-less note-taking web application, built on HTMX and Golang. It is very basic, but I think it's at a good MVP state at this point. The markdown editor especially lacks a lot of features that other note apps have, such as a "ribbon" for inserting things like tables, bold text, italics, images, etc. But this was an intentional choice as I wanted to have as few dependencies as possible. There are libraries out there for editing markdown, but I wasn't stoked about any existing options. I skipped using any CSS libraries as well. The only dependencies are HTMX and a markdown rendering library called [Marked](https://github.com/markedjs/marked).

![notes-view](/images/papernote/notes-view.png)

![editor-view](/images/papernote/editor-view.png)

![fullscreen-view](/images/papernote/fullscreen-view.png)

## Features and Architecture

One feature that I'm very excited about is note previews. On the main notes page, you're presented with a list of your notes on the left and a preview pane on the right. Hovering over a note title will trigger a request to the server to fetch the contents of that note. The note contents are returned to the client where HTMX will swap them into the preview pane. Marked will then pick up those contents and perform the markdown to HTML rendering client-side. Additionally, quick-action buttons will be added next to the note being previewed. You can choose to delete, open in fullscreen view, or edit the note, right there next to the note name. (These options are visible in the first screenshot above.)

The editor view is very simple - markdown on the left, HTML on the right. I hope to build more functionality into the editor in the future (like image support). But this will do for now. The rendering is again handled here on the client side. I wanted the rendering to be real-time and to update on every keystroke from the user, so client-side rendering was the appropriate choice here. Otherwise, the client would need to send a request to the server on every keystroke and get back a rendered page, which is for obvious reasons, ridiculous.

There is also a full-page note view. This is great if you only need to see one of your notes as a reference for something else you are working on.

Multiple users are also supported. User management is handled by an SQLite database file (thus the "almost" in my earlier statement, "(almost) database-less"). It's dead simple, storing usernames and hashed passwords. Authentication is implemented as a standard middleware, utilizing JSON web tokens. Each user gets their own directory on the server and their notes are stored in that folder as plain markdown files. (This was the killer feature of Flatnotes that I stole for this project).

```
user
├── cron-notes.md
├── lorum-ipsum.md
└── yellowstone.md
```

## Wrap Up

And that's it! That's my new notes app. The project can be found on my Github page. I'm open to taking pull requests from anyone who wants to contribute. I'm thrilled at the state of it now and I am planning to fully swap over from Flatnotes sometime in the near future (need to iron out a few more UI things first). I have learned so much about web development in building this project and HTMX has been a huge reason why. I am already applying principals learned from this project in my professional work too, which is always great.

Thanks for reading!

## Notes / Additional Reading / Resources

- [Papernote Repository](https://github.com/noahhefner/papernote)
- [Hypermedia Systems Book](https://hypermedia.systems/hypermedia-reintroduction/)
- [FULL Introduction To HTMX Using Golang](https://www.youtube.com/watch?v=x7v6SNIgJpE)
- [The Most Important Lesson From HTMX](https://www.youtube.com/watch?v=f2wYvIVWR6M)
- [HTMX X/Twitter Page](https://twitter.com/htmx_org)
