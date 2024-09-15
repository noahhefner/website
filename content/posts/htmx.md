---
title: "Htmx"
date: 2024-09-03T12:45:58-04:00
draft: true
---

Earlier this year, I started side project called Papernote. It is a simple note-taking applicaiton that runs in the browser. Like most of my side-projects, the actual product was more of a side-quest--I just wanted an excuse to learn some new tools. Since this was a web-app, I had to decide on what "frontend framework" to use. I had used React and Vue in the past for other things, so those were no-go's. I had been hearing a lot about a Javascript library called HTMX, so having no idea what I was getting myself into, I decided to give it a shot.

At this point in my career, I knew basically nothing about web development. My experience with Javascript frameworks was limited to college assignments and half-baked side projects. Everything I knew about frontend web developement was learned from YouTube tutorials, Stack Overflow posts, and Udemy courses. Take my college capstone project for example. It was an application for managing band equipment inventory for a local high school. We built the frontend in React and used Express on the server. We used MongoDB Atlas as our database and deployed it with Heroku. It was actually a pretty solid application, yet *I had no idea how it worked under the hood*. 

I started learning HTMX with the official HTMX textbook, Hypermedia Systems. I was immediately taken aback by the authors straigtforward explanation of the pros and cons of modern Javascript frameworks. In particular, I was fascinated by this idea that the modern "REST API" is actully not RESTful at all. As the authors explain:

> Today, in a strange turn of events, the term “REST” is mainly associated with JSON Data APIs, rather than with HTML and hypermedia. This is extremely funny once you realize that the vast majority of JSON Data APIs aren’t RESTful, in the original sense, and, in fact, can’t be RESTful, since they aren’t using a natural hypermedia format.
>
> To re-emphasize: REST, as coined by Fielding, describes the pre-API web, and letting go of the current, common usage of the term REST to simply mean “a JSON API” is necessary to develop a proper understanding of the idea.

Until reading that paragraph, I had assumed (and was taught in higher education) that a REST API was simply a mechanism of exchanging information in JSON format between a client and a server. In other words, the JSON API wasm in my mind, the definition of a REST API. I had no idea how uninformed I was as to how "REST" came about and what it originally meant. 

When it came to Javascript frameworks, I *really* had no clue where the code I was writing was running. All I knew was "create-react-app", follow some online tutorials, and somehow my database data magically shows up in the web browser. When it came to hosting, all I needed to do was point the hosting service to my GitHub repository, setup a domain, and my website is now magically online.


