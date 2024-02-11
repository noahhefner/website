---
title: My Homelab Journey
date: 2024-01-10T00:40:04-07:00
draft: true
---

## Humble Beginnings

My homelab journey started about 3 years ago while I was in undergrad studying computer science at Virginia Tech. I had gotten fed up with the big cloud service providers and I wanted a solution to store all my files and photos locally. As a student, I had no money at the time, so I purchased a Raspberry Pi 4 and started tinkering around. The first thing I wanted to host was Nextcloud. I could store all my photos, documents, media, contacts, and calendar events all in one place on my local network. No more paying for Google Drive storage every month! I even had a fancy Raspberry Pi enclosure from Argon that allowed me to boot the Pi from an M.2 SSD over USB, which was pretty slick. I used Google’s takeout feature to mass download all my photos and exported my contacts and calendars. After importing all my data to Nextcloud, I had accomplished what I set out to do: get my data under my own roof.
 
At this point, I was pretty happy with my creation. I had a tiny, power efficient server that housed all my digital assets. Setting up Nextcloud had taught me a lot about the linux servers and basic networking concepts. It also opened me up to the world of self-hosting and introduced me to the vibrant homelab community. I had originally only planned to run Nextcloud, but why stop there? I soon discovered the vast landscape of self-hostable services I wanted to add more stuff to my server.

## Docker

Now, I had setup Nextcloud on my Pi to run on "bare metal" following an excellent guide from Learn Linux TV. It's not too difficult to setup, but I wanted a little more portability in my own lab. For that reason, I made the decision to switch my Nextcloud instance to Docker. What I liked about Docker (really Docker compose) was that it gave me the ability to quickly destroy and re-deploy services while persisting my data through Docker volumes. I developed a set of docker compose files for my services so that any time I needed to re-deploy a service, I just killed the existing container and reran the compose file. This was especially useful in the early days when I was still learning about Docker/Linux and I needed to repeatedly re-deploy my containers because I had mis-configured something in the compose.

My first additional service containers were FreshRSS, an RSS feed aggregator, and Linkding, a bookmark manager. I put everything behind a reverse proxy called Traefik (also running in a Docker container) which allowed me to access my services via my own domain (with SSL!) instead of by IP address.

It was around this time that I made a crucial decision about my homelab: Docker or die. That is to say, I only want to run services that can be run in a Docker container on my homelab. I made this choice for one main reason: ease of maintenance. I love how easy it is to deploy Docker containers on my server. To make backups, I can simply backup all my docker volumes, which are stored under a single directory. Add some tags to the docker compose and Traefik will handle all the certificate stuff automatically. If something isn't working, I go read the docker logs for that service and see whats happening. I know there is some really cool things that can be done with hypervisors like ProxMox, but for me, I don't think the additional system complexity is worth the potential upsides. (At least for the time being.) Not using a hypervisor reduces the number of failure points that I have to check when something goes wrong. As much as I love my homelab, I want it to "just work". If I have to spend more time maintaining my server than I do actually using my services, then I have missed the point of homelab entirely.

## Ansible

I also decided to take my docker compose files a step further by converting them to Ansible playbooks. This gave me another level of automation and made my deployment process even faster. I would highly recommend Jeff Geerlings Ansible for DevOps as it was a great resource for me when I was just getting started.

A few things I really love about Ansible:

1. Ansible Vault: Ansible Vault is a mechanism for storing sensitive playbook information (API keys, username/passwords, etc.) in an encrypted text file. I also use the vault as a central location for all my playbook variables. I just like having one file to go to when I want to change something (which really isn't the intended use case for vault, but it works for me because I'm the only one who uses these playbooks.)

2. Templates: A lot of my services have some sort of JSON/YAML/TOML configuration file to set some options within the service. With Ansible templates, I can use my vault variables within the configuration file and Ansible will automatically replace the variable with the value in my vault before copying the template file to the target machine. This is especially useful for services like Homepage that have a large number of configuration options.

## More Power

The Raspberry Pi is an amazing little computer, but it was beginning to struggle a bit (especially in Nextcloud) running all my containers. In the first of what would be a series of hardware transitions, I transformed my desktop gaming PC into an Ubuntu server and moved all my containers over. Speaking again to the portability of docker volumes, this process was completely painless. Just move my docker volumes directory to the new drive, run my Ansible playbooks, and I was up and running again in no time. I had purchased a mid-range NVIDIA GPU a few years back, which I utilized for hardware acceleration in Jellyfin, a recent addition to my container fleet.

This worked well for a time, but I started to miss my desktop and my gaming monitor was collecting dust in the corner of my room. Inspired by an LTT video on up-cycling old hardware as a home server, I purchased a Dell Optiplex Desktop on Facebook Marketplace for $80. It has a 7th gen Intel i5 and 8GB of DDR3, a solid base on which I could build. I cleaned it up a bit, swapped the spinning disk drive for an SSD, migrated all my containers (again) and I was good to go. As a bonus, it came with a CD drive which I could use for ripping DVDs and CDs. (This actually kick-started my CD collection, which I digitized and stored in a music-streaming service called Navidrome.)

This brings me to the current day where I am still running all my containers on the Optiplex. However, I have made a few upgrades, particularly in networking department. I got a major case of FOMO after listening to an episode of The Homelab Show (hosted by Jay LaCroix and Tom Lawrence) on open source firewalls and I decided I wanted an OPNsense box for my setup. I chose OPNsense over Pfsense for the more consistent updates and arguably better user interface. In addition to performing the usual routing/firewall duties, it also runs a Wireguard instance, giving me access to my server from outside my local network. I also purchased a rack, a basic unmanaged network switch, and a cheap PDU off Amazon to round it out.

The Raspberry Pi I started with has now been repurposed as a Pihole. I setup my OPNsense box to forward all DNS requests to the Pi, which blocks advertisement and tracking requests. My TP-Link router/wireless access point had its router duties revoked, now handling just the latter. I'm still using the Optiplex for my docker containers, but I have a 4U chasis from Sliger ready to accept some new server hardware. (I had originally planned to put the Optiplex internals in the 4U chassis, but it has a proprietary Dell motherboard and power supply, neither of which will install correctly into the chassis.) My future plan is to purchase some new hardware for the Sliger chassis and turn the Optiplex into an HTPC.

![rack](/images/rack.jpg)

## Lessons Learned

I've really enjoyed setting up all this equipment for my own personal use. But the cool thing about homelab is that these skills are also marketable in a professional environment. I've learned about a wide array of topics such as:

- Setting up a Linux server and performing basic management tasks
- Configuring and spinning up containers with Docker
- Automating server tasks with Ansible
- Networking concepts like sub-netting, port forwarding, and firewall rules

In conclusion, here are some lessions I have learned during my homelab journey that I would like to share:

- **Start small**: You don't need to run out and buy a ton of expensive equipment if you are starting from scratch with no prior experience. My Raspberry Pi was a great introduction to self-hosting and it allowed me to gain a lot of experience for a low price. 
- **One thing at a time**: Focus on one task at a time. It's easy to have multiple sub-projects in progress at once, like converting docker compose files to Ansible playbooks, or writing new playbooks for new services, or setting up PiHole. Taking on too many tasks at once causes me to lose track of what I'm actually trying to accomplish and I would fail to *complete* anything at all. Setting small goals and focusing on implementing a singular feature helped me progress faster in my homelab journey.
- **Document everything**: Take notes on your system configuration. It is helpful to have a reference guide to refresh your memory when you are troubleshooting a service that suddenly stopped working. And this doesn't just mean taking notes
