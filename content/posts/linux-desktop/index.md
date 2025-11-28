---
title: "On Customizing Linux"
date: 2025-11-09T18:50:40Z
draft: true
cover: "tux.jpg"
---

## Introduction

“The year of the Linux desktop” is somewhat of a running joke in the Linux community. It refers to the idea that one day, Linux will finally establish itself as a mainstream desktop operating system alongside Windows and macOS for everyday computer users. But the prophecy has not yet been fulfilled—thanks to limited support for popular software, a fragmented landscape of desktop environments, and minimal adoption from computer manufacturuers. All of this has kept Linux just out of reach for the average computer user.

But it feels like the tide is turning. Valve proved—through the [massive success of the Steam Deck](https://www.theverge.com/pc-gaming/618709/steam-deck-3-year-anniversary-handheld-gaming-shipments-idc?ref=birchtree.me)—that Linux doesn’t have to be intimidating; they put a full-fledged Linux desktop in the hands of millions of gamers, many of whom probably didn’t even realize it. More recently, [DHH](https://dhh.dk/) has helped generate enthusiasm for Linux through the release of [Omarchy](https://omarchy.org/), a beautiful, easy-to-install Arch Linux configuration gearned towards developers.

Simultaneously, Windows 11 seems to be getting worse by the day as Microsoft pushes out one anti-consumer update after another. Just this year, Microsoft has [patched multiple loopholes](https://www.pcguide.com/news/windows-11-update-removes-known-local-account-workarounds-so-now-you-definitely-need-to-sign-in-with-microsoft/) which allowed Windows 11 to be installed without a Microsoft account under the guise of "security improvements". Additionally, Microsoft is inregrating their AI spyware into every aspect of their operating system with the introduction of Copilot and "Copilot+ PC's". And lets not forget how Microsoft pushed millions of otherwise perfectly fine computers into obsolecense with completely unreasonable and seemingly arbitrary Windows 11 [minimum system requirements](https://www.ghacks.net/2024/12/05/windows-11-microsoft-sticks-to-system-requirements-despite-sluggish-conversion/). Even non-tech-savy computer users are feeling pushed away by these increasingly restrictive, bloated, and intrusive design choices. Is Linux the way out?

## First Contact with Linux Desktops

I was in high school the first time I installed Linux on a computer. I had just built my second desktop computer and I needed an operating system for it. While I don't remember why highschool me felt the need to own two desktops, I do recall that my primary motivation for installing Linux on that machine was simply because I did not want to buy a second Windows 10 license. I had worked hard all summer to save up for that machine and the last thing I wanted to do was fork over another $100 to Microsoft just to make it usable. I installed Ubuntu 16.04 LTS because that was the only Linux distribution I knew. As I booted into the GNOME desktop environment for the first time, I was both in awe and disbelief. Compared to my Windows machine, this OS booted faster, was more customizable, and completely free to use?! My mind was blown. There had to be a catch. Why isn't everybody using Linux?

After tinkering with my Linux box for a while, I quickly figured out the answer to that question: software compatibility; or more accurately, the lack thereof. I was a bit dissapointed to discover that I could not run the Microsoft Office suite (which I needed for school work) or play any of my Steam games. It was practically a paperweight since those apps made up 90% of my computer usage. Despite these challenges, I could not get over the fact that this operating system was completely free. I was enamoured by the idea of software being freely distributed for anyone to use.

After discovering that there were other Linux flavors outside Ubuntu, I quickly developed a habit of [distro hopping](https://informatecdigital.com/en/What-is-distro-hopping-in-Linux--why-and-when-to-do-it/). Distro hopping is Linux slang for constantly installing different different Linux distributions on  your computer. Many people who are new to Linux become distro-hoppers. But how could one not

, searching for that "perfect Linux desktop". But alas, the grass was always greener on the other side. I never quite found one desktop that I truly loved using. Each one seemed to have some quirk that wasn't quite right for me.

After tinkering for some time with various distributions, I eventually made my way down the [Linux ricing](https://dev.to/nucleofusion/complete-beginners-guide-to-linux-ricing-4i0e) rabbit-hole. And let me tell you, it is a very, very deep rabbit hole. In a nutshell, Linux “ricing” is the practice of heavily customizing the look and feel of your Linux desktop to make it uniquely stylish or visually impressive. To use an analogy that predates my existence, it's sort of like customizing your MySpace profile page, except instead of a social media site, you’re customizing an entire operating system. Below is a screenshot (not mine) of a typical tiling window manager setup:

![Tiling Window Manager](/tiling-wm.jpg)

For my “rice” (I still don’t know why it’s called that), I used Debian 12 as the base distribution and installed [Sway](https://swaywm.org/) as the foundation for the graphical functions. Sway is what’s known as a “tiling window manager”. Unlike Windows or macOS, where application windows “float” around the screen, tiling window managers automatically “tile” or organize application windows for you. The advantage of using a tiling window manager is that, with a little bit of practice, you can open and navigate between applications much faster than on a floating window system.

Tiling window managers like Sway are extremely minimal by design. They are geared towards power users who want to hand-select every piece of software that gets installed on their machine. Everything, and I mean everything, that makes up your system needs to be installed and configured manually. I spent hours upon hours picking packages and crafting config files until the system was aesthetically pleasing, performant, and taylored exactly to my neads.

While setting up Sway was a fantastic learning experience, it was also a pain in the neck sometimes. There were several occasions where I would take my laptop to a coffee shop to get some work done, only to spend the first 30 minutes troubleshooting my WiFi connection or figuring out why my system wouldn’t boot. And it wasn’t just a few times; these little hiccups kept happening over and over again. I decided that this configuration was simply too much effort to maintain. It seemed wrong to force myself to use a system that, despite its beauty, was so fragile and frustrating. Feeling defeated, I wiped my system and installed bone-stock Fedora with the GNOME desktop environment. Say what you want about GNOME, but dang it, it just works, no strings attached. For over the better part of two years, Fedora and GNOME provided me with a stable desktop experience for my everyday computer tasks.

## A New Hope

![Omarchy Logo](/omarchy-logo.png)

And then, earlier this year, DHH released Omarchy. Unlike established Linux distributions such as Ubuntu or Fedora, Omarchy isn’t a “distro” in the traditional sense. Instead, it’s essentially an Arch Linux install bundled with DHH’s favorite applications and configuration files-and an absolute boat-load of bash scripts.

Omarchy made an immediate splash in the Linux community. A longtime macOS user, DHH only made the switch to Linux earlier this year, and his enthusiasm for the platform has been infectious. Through interviews, podcasts, and blog posts, he has been documenting his Linux experience and delight in building Omarchy, even going so far as to make it the default system configuration for all employees at his company, 37Signals.

What struck me about Omarchy is how complete and cohesive it feels—especially for a tiling window manager setup. The theming system alone is remarkably thorough: cycling through the theme options automatically updates everything from the wallpaper to Neovim to even a [micro-forked version of Chromium](https://world.hey.com/dhh/omarchy-micro-forks-chromium-1287486d). Omarchy’s update utility is just as polished. It’s essentially a bash script that not only updates your system packages, but also pulls and installs the latest configuration files from the Omarchy GitHub repository. There’s even a mechanism for running migration scripts to help users set up new features, if any were included in the updates.

![Omarchy Screenshot](/omarchy.png)

At launch, the installation process for Omarchy was a bit unique. First, you would need to install Arch Linux manually using the `archinstall` utility. Then, you would boot into the system, download the Omarchy install script, and execute it. The script would download all the Omarchy assets, install all the Omarchy applications, and get everything ready to go. After the script is finished, simply reboot the machine to a fully configured system. This process has since been replaced by an ISO file, but the scripted setup workflow was intriguing.

Although I eventually decided Omarchy wasn’t the right daily driver for me, it reignited my interest in Linux ricing and inspired me to give tiling window managers another go. Omarchy demonstrates that a highly customized Linux setup doesn’t have to be delicate. With enough care, it is possible to build a desktop that’s both beautiful and reliable. I loved the clarity and reproducibility that came from Omarchy’s bash-script centric approach, and I began work building a new rice of my own.

## Return of the Rice

For my new rice, I wanted to start totally from scratch. The first step was to select a base Linux distribution. I considered several options, including Fedora, Ubuntu, and Debian, but I landed on Arch Linux for two key reasons:

1. [The Arch Wiki](https://wiki.archlinux.org/title/Main_page) - The Arch Wiki is an invaluable resource for learning about Linux. If it runs on Arch, there's a good chance the Wiki has a page for it. I used the Wiki heavily while setting up my system, and I continue to use it for troubleshooting and learning.
2. [The Arch Linux User Repository (AUR)](https://aur.archlinux.org/) - Generally speaking, installing software on your computer from random people on the internet is ill-advised. However, there are a handful of packages I wanted to install that are only available through the AUR. I use the AUR sparingly, but it is nice to have it in the toolbox.

### Hyprland

![hyprland](hyprland.jpg)

Next, I needed to choose a tiling window manager. The decision was between Sway and [Hyprland](https://hypr.land/), the two most widely used options that support Wayland. While both are great, I chose Hyprland for its excellent documentation. The Hyprland Wiki is a fantastic guide, not just for configuring Hyprland, but for assembling a complete desktop environment [The "Useful Utilities" pages](https://wiki.hypr.land/Useful-Utilities/) are a great example of this. These pages cover all the additional bits that most users will *probably* want to configure, such as a notification daemon, a status bar, or a desktop wallpaper. For the tiling window manager veterans, this all seems obvious, but for newcomers like myself, these notes are incredibly useful.

### Packages and Applications

The next thing I did was to create text files listing all the packages I wanted to install on my system. Above each package (or group of packages), I added comments to remind myself what that package is for. With these comments, I won’t accidentally remove something important and break my install. I have separate files for Arch repository packages, AUR packages, and Flatpaks. With a bash script (which I stole directly from the Omarchy repository), I can install all the packages in a single command. Here’s a sample:

```plaintext
# Printing
cups
cups-browsed
cups-filters
cups-pdf

...

# Login manager
greetd
greetd-regreet

# Dependency for Flameshot
grim

# Static site generator
hugo

...

# GUI for managing displays
nwg-displays

```

### Templating Script

I also wrote a small templating script that reads values from a .env file and inserts them into configuration files using Jinja2 syntax. This lets me share fonts, colors, and other system-wide settings across multiple apps.

In the example below, I have two configuration files: one for Fuzzel, my app launcher, and one for Waybar, my status bar. I wanted to use the same font for both Waybar and Fuzzel, so instead of hardcoding `CaskaydiaCove Nerd Font` in both files, I use the Jinja syntax to programmatically insert the font name into both files.

```
# .env
FONT='CaskaydiaCove Nerd Font'
```

```
# fuzzel.jijna.ini
font={{ FONT }}:size=16
```

```css
/* (Waybar) style.jinja.css */
* {
font-family: "{{ FONT }}", Roboto, Helvetica;
font-size: 14px;
font-weight: 600;
min-height: 0;
}
```

After executing the script, the files look like this:

```
# fuzzel.jijna.ini
font=CaskaydiaCove Nerd Font:size=16
```

```css
/* (Waybar) style.jinja.css */
* {
font-family: "CaskaydiaCove Nerd Font", Roboto, Helvetica;
font-size: 14px;
font-weight: 600;
min-height: 0;
}
```

### Web Apps

Another idea I took directly from the Omarchy playbook is [web apps](https://learn.omacom.io/2/the-omarchy-manual/63/web-apps). Web apps are desktop shortcuts to your most frequently used sites, such as GitHub, YouTube, and ChatGPT. Launching one of these apps via the app launcher ([Fuzzel](https://codeberg.org/dnkl/fuzzel) in my case) opens Chromium to the web page for that application. This is a useful workaround for applications that don’t have a native Linux client. I added web apps for YouTube, Proton Mail, Proton Calendar, and the National Weather Service.

![Web Apps](/web-apps.png)

### Setup Scripts

With my packages and applications sorted, I wrote (or stole) a few bash scripts to set everything up on a fresh Arch install, just like Omarchy did in its early days. I broke the process into five separate scripts, mostly for debugging and testing things out when I was just getting started. I ended up with the following workflow:

```sh
# Installs yay, an AUR helper
./setup.sh
# Installs packages listed in the aforementioned text files
./install.sh
# Move config files to the correct locations
./configs.sh
# Miscellaneous tasks (enable systemd services, add user to docker group, etc.)
./post-setup.sh
```

Reboot the machine, then run:

```sh
# Install flatpaks + flatpak configurations
./post-reboot.sh
```

## The Final Result

![Screenshot](/screenshot.png)

After spending countless hours on this project, I am super happy with the result! I’ve been running this configuration on my personal computers for about two weeks now, and it has been an absolute joy to use. I just recently picked up a 12-year-old Lenovo Thinkpad T430 and immediately set it up with this configuration. Even on older hardware, the desktop environment is snappy and feels just as performant as my newer machines. (I’ll be writing another article specifically about the T430 soon!)

There’s a saying in the Linux community that “[Linux is only free if you don’t value your time.](https://www.youtube.com/watch?v=Qt2GkwwypDw)” While I do think that saying is becoming less true as time goes on, it was absolutely true for this project. I spent hours upon hours learning, researching, watching YouTube videos, reading forums, writing scripts, configuring files, and fixing bugs, just to reach a state that is, admittedly, probably still less stable than Windows or macOS. Not to mention, I will need to perform ongoing maintenance to the configuration as packages get updated. (Literally a few days after setting up my T430, Hyprland pushed a breaking change that required an update to a config file.) As someone who makes my living with a keyboard and mouse, I don't mind that extra bit of friction. Dare I say, I actually *enjoy* it. But I think it goes without saying that this project is certainly not for everyone, especially if you don't enjoy troubleshooting computers.

So is 2025 finally the year of the Linux desktop? Eh – probably not. However, I do think even non-tech-savvy people are beginning to question the direction big tech is taking consumer desktops/laptops. Questions like:

*Do I really want an [‘agentic AI’ running around on my computer](https://www.windowslatest.com/2025/11/19/microsoft-is-putting-an-ai-agent-on-the-windows-11-taskbar-heres-your-first-look/), reading all my personal information, taking actions without my knowledge?*

or 

*Do I really want to buy a non-upgradable, near-unrepairable laptop that will be [obsolete in 5 years due to a software update](https://applescoop.org/story/which-macs-will-stop-working-in-2024-and-2025-complete-list-of-compatible-apple-products)?*

If you spend most of your time in Windows or macOS, you might just find Linux to be a breath of fresh air, especially if you're a developer. There truly has never been a better time to try Linux!

![Changes You Forever](/changes-you.png)