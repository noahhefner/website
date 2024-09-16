---
title: "Htmx"
date: 2024-09-03T12:45:58-04:00
draft: true
---

Earlier this year, I started a side project called Papernote. It is a simple note-taking application that runs in the browser. Like most of my side projects, the actual product was more of a side quest—I just wanted an excuse to learn some new tools. Since this was a web app, I had to decide on a frontend framework to use. I had used React and Vue in the past for other things, so those were no-goes. I had been hearing a lot about a JavaScript library called HTMX, so, having no idea what I was getting myself into, I decided to give it a shot.

At this point in my career, I knew basically nothing about web development. My experience with JavaScript frameworks was limited to college assignments and half-baked side projects. Everything I knew about frontend web development was learned from YouTube tutorials, Stack Overflow posts, and Udemy courses. At that time, I didn't even know what code was running on the client and what code was running on the server. All I knew was to run create-react-app, follow some online tutorials, and somehow my database data magically showed up in the web browser. For hosting, I simply pointed Heroku to my GitHub repository, set up a domain, and my website was now magically online. How this all worked was a complete mystery to me.

Which is sort of crazy to think about isn't it? The bearier to entry for getting a basic web app up and running is essentially zero. The modern developer needs no knowledge of server infrastructure, deployment pipelines, or even the underlying principals of HTTP to create a functional product. When the foundational technologies are abstracted away by hosting platforms, developers are robbed of a deeper understanding of how their applications are put together.

What drew my attention to HTMX at the start was how it was framed as the antithesis to modern JS frameworks. Where frameworks were bloated and complex, HTMX was lean and simple. Being the Grug-brained developer that I am, I thought this would be a good choice for me. The creators even wrote a free online textbook! As I read through Hypermedia Systems (a real page-turner if you ask me), everything started to click. I understood why the term "Single Page Application" applies to websites that seemingly have dozens of different pages. I gained a much deeper understanding of the HTTP protocol and the role of things like headers, HTTP verbs, URL queries, response codes, and so much more. All terms and concepts I was familiar with, but lacked in practical experience. The web platform as a whole became clear to me.

I cannot understate the impact that HTMX and Hypermedia Systems have had on my development as an engineer. My mindset around building web applications has completely shifted. I find that I think less in terms of "frontend and backend" and instead in terms of "client and server." (This is perhaps due to the fact that the separation between the frontend and backend code for an HTMX-driven application is less clean-cut than in traditional JSON-API-driven projects, but I find it a valuable perspective nonetheless.) I can now draw clear connections between the architecture of my application and its performance and security. I can accurately assess what user interactions necessitate a request to the server and what can be done client-side.

I think the biggest driver behind this personal renaisance is the fact that understanding HTMX neccessitates an understanding of basic web concepts. It is impossible to understand why client-side JavaScript frameworks are bloated without understanding how a framework functions to begin with. It forces the developer to carefully consider each client-server interaction and to properly update the application state (which is hypermedia, btw).

The authors of Hypermedia Systems argue that the vast majority of web applications can be built using simple tools like HTMX, without the need for large amounts of client side JavaScript. Having a few HTMX projects under my belt now, I wholeheartedly agree with them. This is not to say that JS frameworks have no place in a developers toolbox. HTMX is likely a poor choice for implementing experiences that rely heavily on complex client-side interractions and animations. But what HTMX lacks in chrome, it makes up for in simplicity 


# Scratch




They authors of Hypermedia Systems lay this out beautifully, offering a brief history of how we arrived at where we are now in web dev and how HTMX aims to bring the industry back in line with the original vision for how the web should work. 








Which is kind of crazy to think about isn't it? It's completely possible for someone who knows little to nothing about web technologies to build a fully functional application--with a database and authentication--and have no idea how it's actually put together. **In hindsight, that's a very dangerous position to be in as a developer.** If you were a user or company paying for access to my software, would you want me on the development team? Absolutely not! (To be clear, I am not saying that development teams should not hire inexperienced developers. We were all inexperienced at the get-go.)







I was immediately taken aback by the authors straigtforward explanation of the pros and cons of modern Javascript frameworks. In particular, I was fascinated by this idea that the modern "REST API" is actully not RESTful at all. As the authors explain:

> Today, in a strange turn of events, the term “REST” is mainly associated with JSON Data APIs, rather than with HTML and hypermedia. This is extremely funny once you realize that the vast majority of JSON Data APIs aren’t RESTful, in the original sense, and, in fact, can’t be RESTful, since they aren’t using a natural hypermedia format.
>
> To re-emphasize: REST, as coined by Fielding, describes the pre-API web, and letting go of the current, common usage of the term REST to simply mean “a JSON API” is necessary to develop a proper understanding of the idea.

Until reading that paragraph, I had assumed (and was taught in higher education) that a REST API was simply a mechanism of exchanging information in JSON format between a client and a server. In other words, the JSON API wasm in my mind, the definition of a REST API. I had no idea how uninformed I was as to how "REST" came about and what it originally meant.





