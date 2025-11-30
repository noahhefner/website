---
title: "On Customizing Linux"
date: 2025-11-09T18:50:40Z
draft: true
cover: "tux.jpg"
---

## Introduction

“[The year of the Linux desktop](https://yearofthelinuxdesktop.net/)” is somewhat of a running joke in the Linux community. It refers to the idea that one day, Linux will finally establish itself as a mainstream desktop operating system alongside Windows and macOS for everyday computer users. But the prophecy has not yet been fulfilled—thanks to limited support for popular software, a fragmented landscape of desktop environments, and minimal adoption from computer manufacturuers. All of this has kept Linux just out of reach for the average computer user.

But it feels to me like the tide is turning. Valve proved—through the [massive success of the Steam Deck](https://www.theverge.com/pc-gaming/618709/steam-deck-3-year-anniversary-handheld-gaming-shipments-idc?ref=birchtree.me)—that Linux doesn’t have to be intimidating; they put a full-fledged Linux desktop in the hands of millions of gamers, many of whom probably didn’t even realize it. More recently, [DHH](https://dhh.dk/) has helped generate enthusiasm for Linux through the release of [Omarchy](https://omarchy.org/), a beautiful, easy-to-install Arch Linux configuration gearned towards developers. In other news, Zorin OS, a popular Windows-like Linux distribution, just disclosed that their OS has [gained almost a million new users](https://www.windowscentral.com/microsoft/windows-10/windows-10-retirement-pushes-780-000-users-to-linux-as-zorin-os-hits-1m-downloads) thanks to Windows 10 reaching its end-of-life. With Linux picking up steam at such an astonishing rate, could 2026 be the year of the Linux desktop?

## First Contact with Linux Desktops

I was in high school the first time I installed Linux on a computer. I had just built my second desktop and I needed an operating system for it. While I don't remember why highschool me felt the need to own two desktops, I do recall that my primary motivation for installing Linux on that machine was simply because I did not want to buy a second Windows 10 license. I had worked hard all summer to save up for that machine and the last thing I wanted to do was fork over another $100 to Microsoft just to make it usable. I installed Ubuntu 16.04 LTS because that was the only Linux distribution I knew. As I booted into the GNOME desktop environment for the first time, I was both in awe and disbelief. Compared to my Windows machine, this OS booted faster, was more customizable, and completely free to use?! My mind was blown. There had to be a catch. Why isn't everybody using Linux?

After tinkering with my new toy for a while, I quickly figured out the answer to that question: software compatibility; or more accurately, the lack thereof. I was a bit dissapointed to discover that I could not run the Microsoft Office suite (which I needed for school work) or play any of my Steam games. Despite these challenges, I could not get over the fact that this operating system was completely free. I was enamoured by the idea of software being freely distributed for anyone to use.

I soon discovered that there were other Linux flavors outside Ubuntu and quickly developed a habit of [distro hopping](https://informatecdigital.com/en/What-is-distro-hopping-in-Linux--why-and-when-to-do-it/). Distro hopping is Linux slang for constantly installing different Linux distributions on your computer. It is common for Linux newcomers to become distro hoppers, simply because there are a ton of unique options to choose from! By changing your Linux distribution, you can completely change the appearance and functionality of your system. With so many different ways to experience Linux, it's hard to resist trying them all to see which one fits you best.

## Distribution vs. Desktop Environment

![Linux Desktop Comparision](/desktops.gif)

*GNOME, KDE, XFCE, and Cinnamon Desktop Environments*

Before the next section, it is imporant to understand the difference between a Linux distribution and a Linux desktop environment. Let's start with the distribution (or distro). My definition of a Linux distribution is a software suite which includes three key components:

1. The Linux kernel
2. A package manager (ie. a piece of software that manages additional software packages)
3. Some preinstalled packages

Most mainstream Linux distros are supported by some sort of governing body. Broadly speaking, this governing body is responsible for maintaining a repository of packages (software) for the distro, developing a package manager to interface with that software repository, and operating the servers required to *distribute* that software to the end user. Some distros are backed by corporate entities such as Fedora, which is supported by Red Hat. Other distros like Debian adopt a more [community-centeric philosophy](https://www.debian.org/intro/philosophy), where thousands of individual contributors bear the collective burden of maintenance and development. 

A Linux desktop environment (or DE for short) is simply a set of those preinstalled packages in a distro which provides all the graphical user interfaces for the system. The DE provides the neccessary software for managing windows, facilitating user interactions, and running applications. DE's often times come pre-loaded with commonly used software, such as a file manager, calendar, calculator, office suite, etc. Most of the **visually observable** differences between distributions are really in the DE, not the underlying distro (though there are certainly differences between distributions). This realization unlocks a whole new approach to customizing Linux, since most desktop environments can be installed on most distributions.

## Down The Rabbit Hole

After distro-hopping for a few years and installing more desktop environments than I could count, I was introduced to the world of [Linux ricing](https://dev.to/nucleofusion/complete-beginners-guide-to-linux-ricing-4i0e). In a nutshell, Linux “ricing” (no idea where that term came from) is the practice of heavily customizing the look and feel of your Linux desktop environment to make it uniquely stylish or visually impressive. To use an analogy that predates my existence, it's sort of like customizing your MySpace profile page, except instead of a social media site, you’re customizing an entire desktop experience. Ricing goes way beyond just changing your icon theme and setting a cool background. This is big nerd territory, requiring extensive knowledge of Linux systems and a willingness to tinker and troubleshoot for hours on end.

For my first rice, I used Debian 12 as the base distribution and installed [Sway](https://swaywm.org/) for my desktop environment. Sway is in a unique class of desktop environments known as “tiling window managers”. Unlike Windows, macOS, or even most mainstream Linux distros where application windows “float” around the screen, tiling window managers automatically “tile” or organize application windows for you. Another unique aspect of tiling window managers is that system navigation (switching between apps and workspaces) is typically driven entirely by keyboard shortcuts. The advantage of using a tiling window manager is that, with a little bit of practice, you can open and navigate between applications much faster than on a floating window system.

![Typical Tiling Window Manager](/tiling-wm.jpg)

*Tiling Window Manager Example*

Tiling window managers like Sway are extremely minimal by design. You won't find any preinstalled applications, graphical utilities, or built-in conveniences that you’d normally expect from a traditional desktop environment. They are geared towards power users who want to hand-select every piece of software that gets installed on their machine. Everything, and I mean *everything*, that makes up your system needs to be installed and configured manually. Even fundamental components—like an application launcher, notification daemon, network manager, screenshot tool, and sometimes even basic fonts—must be installed and configured by hand before the system feels usable. I spent hours upon hours picking packages and crafting config files until the system was aesthetically pleasing, performant, and taylored exactly to my neads.

Setting up Sway was a fantastic learning experience, it was also a pain in the neck sometimes. There were several occasions where I would take my laptop to a coffee shop to get some work done, only to spend the first 30 minutes troubleshooting why my WiFi wasn't working or worse, why my system wouldn’t boot. And it wasn’t just a few times; these little hiccups kept happening over and over again. After a while, I got fed up with Sway and I decided that this configuration was simply too much effort to maintain. It also seemed wrong to force myself to use a system that, despite its beauty, was so fragile and frustrating. Feeling defeated, I wiped my system and installed bone-stock Fedora with the GNOME desktop environment. Say what you want about GNOME, but dang it, it just works, no strings attached. For over the better part of two years, Fedora and GNOME provided me with a stable desktop experience for my everyday computer tasks.

## A New Hope

![Omarchy Logo](/omarchy-logo.png)

*Omarchy Logo*

And then, earlier this year, DHH released Omarchy. Unlike established Linux distros such as Ubuntu or Fedora, Omarchy isn’t a “distro” in the traditional sense. Instead, it’s essentially an Arch Linux install bundled with DHH’s favorite applications and configuration files-and an absolute boat-load of bash scripts.

Omarchy made an immediate splash in the Linux community. A longtime macOS user, DHH only made the switch to Linux earlier this year, and his enthusiasm for the platform has been infectious. Through interviews, podcasts, and blog posts, he has been documenting his Linux experience and delight in building Omarchy, even going so far as to make it the default system configuration for all employees at his company, 37Signals.

What struck me about Omarchy is how complete and cohesive it feels—especially for a tiling window manager setup. The theming system alone is remarkably thorough: cycling through the theme options automatically updates everything from the wallpaper to Neovim to even a [micro-forked version of Chromium](https://world.hey.com/dhh/omarchy-micro-forks-chromium-1287486d). Omarchy’s update utility is just as polished. It’s essentially a bash script that not only updates your system packages, but also pulls and installs the latest configuration files from the Omarchy GitHub repository. There’s even a mechanism for running migration scripts to help users set up new features, if any were included in the updates.

![Omarchy Screenshot](/omarchy.png)

*Omarchy Desktop*

At launch, the installation process for Omarchy was a bit unique. First, you would need to install Arch Linux manually using the `archinstall` utility. Then, you would boot into the system, download the Omarchy install script, and execute it. The script would download all the Omarchy assets, install all the Omarchy applications, and get everything ready to go. After the script is finished, simply reboot the machine to a fully configured system. This process has since been replaced by an ISO file, but the scripted setup workflow was intriguing.

Although I eventually decided Omarchy wasn’t the right daily driver for me, it reignited my interest in Linux ricing and inspired me to give tiling window managers another go. Omarchy demonstrates that a highly customized Linux setup doesn’t have to be delicate. With enough care, it is possible to build a desktop that’s both beautiful and reliable. I also loved the clarity and reproducibility that came from Omarchy’s bash-script centric approach, and I began work building a new rice of my own.

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

## Closing Thoughts

So will 2026 *finally* the year of the Linux desktop? Realistically, probably not. However, I do find it interresting that while Linux is gaining momentum, Windows is simultaneously getting worse by the day as Microsoft pushes out one anti-consumer update after another. Just this year, Microsoft has [patched multiple loopholes](https://www.pcguide.com/news/windows-11-update-removes-known-local-account-workarounds-so-now-you-definitely-need-to-sign-in-with-microsoft/) which allowed Windows 11 to be installed without a Microsoft account under the guise of "security improvements", requiring users to hand over their personal information to Microsoft just to use the machine that they **already paid for**. And lets not forget how Microsoft pushed millions of otherwise perfectly fine computers into obsolecense with completely unreasonable and seemingly arbitrary Windows 11 [minimum system requirements](https://www.ghacks.net/2024/12/05/windows-11-microsoft-sticks-to-system-requirements-despite-sluggish-conversion/). But perhaps Microsoft's worst offense of all is their insistence on injecting AI into every aspect of their OS. The disastrous launch of Recall made it abundantly clear that people do not, in fact, want AI spyware running on their computer at all times. The dumpter fire that is modern Windows has become a great advertisement for desktop Linux.

If you're a Windows user (or a macOS user for that matter) who is sick and tired of your computer spying on you without your consent, if you want to take control of your digital tools rather than your tools controlling you, if you don't care for the AI garbage thats being shoved into every new peice of software, you should know that **there has never been a better time to try Linux**. If you have an old laptop laying around, throw a Linux distro like Ubuntu or Fedora on there and take it for a test drive. Maybe even dip your toes into some open source applications like LibreOffice or GIMP. The worst that can happen is you lose a few hours learning something new! Who knows; you might just end up in the rabbit hole too.

![Changes You Forever](/changes-you.png)