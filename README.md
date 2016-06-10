# Mere Linux
Mere Linux is a simple Linux distribution built upon [musl](http://www.musl-libc.org/) libc and aimed at virtualized or containerized server instances.

## Why Another Distribution?
Mainstream Linux distributions tend to be a marriage of two main use cases:
* A long-lived Web/Internet server, running on physical hardware, supporting many users, often managed directly
* Full-blown desktop systems

As cloud infrastructure continues to gain popularity, such distributions have often been made to work inside virtual machines and containers, although they haven’t really been designed for that purpose.

What if support for the above use cases were stripped away? What if a distribution was designed to be run in a virtual machine or container, where:
* Scalability and flexibility are more important than traditional conventions
* It is understood that administration is not best done individually and directly
* Metrics and logs are intended to be collected and exported externally
* Deployment and configuration happens through instance creation and deletion

What would a distribution optimized for such a use case look like?

Mere Linux aims to find the answer.

## Getting Started
For additional details, such as how to install, how to contribute, or the goals and design decisions of Mere Linux, see the [Wiki](https://github.com/jhuntwork/merelinux/wiki).
