# Checkmk Glossary

Source: https://docs.checkmk.com/latest/en/glossar.html

License: LicenseRef-Vendor-Copyright (Checkmk GmbH; internal CSA use only — not redistributable).

Extracted: 54 terms.

---

## Activating changes

Changes to the configuration only take effect on the monitoring after they have been activated in a second step; in a similar way to how partitioning programs handle this, for example: Configure, check, apply. The activation of changes is accessed via the Changes icon in the navigation bar.

## Active check

An active check is a small program or script that establishes a direct connection to a service on the network or internet, from where it queries the monitoring data. Active checks are used for network-based services such as HTTP, SMTP or IMAP, e.g. check_http for querying web pages. An active check handles both the collection and the evaluation of the data. This differs from a check plug-in, which is sometimes called a passive check, because a passive check only evaluates existing data.

## Agent

An agent on a host collects data relevant for the monitoring. The agent can be a small program installed on the host (the Checkmk agent), or an SNMP agent running independently of Checkmk on the host, or a special agent that obtains the information through an API provided by the target systemâââor an active check that queries network-based services.

## Agent Bakery

In the commercial editions, the Agent Bakery is used to individually package agents, and as an option the packages can also be distributed automatically.

## Agent plug-in

An agent plug-in extends the functions of the standard agent supplied with Checkmk. It is a small program or script that is called by the Checkmk agent which enhances the agentâs output with additional sections of monitoring data. This data is processed on the Checkmk server by a compatible check plug-in. An example of an agent plug-in is the Agent Updater.

## Agent Updater

In the commercial editions, the Agent Updater is an agent plug-in that enables agents to be updated automatically.

## API integrations

When the Checkmk Setup refers to API integrations , it means monitoring data that uses the Checkmk agentâs data format but which originates from a different source. Such sources can be data source programs, special agents or hosts that piggyback their data. If data received via an API integration is to be used in monitoring, API integrations must be enabled in a hostâs properties.

## Automation user

A special account for querying and configuring Checkmk independently of the web interface, e.g. via API, command line, script or web service. By default, the automation user has a randomly chosen automation password ( automation secret ). At least one automation user is already set up in a fresh Checkmk site, for registering the agent with the Checkmk server for TLS-encrypted data transfer.

## Business Intelligence (BI)

Business Intelligence in Checkmk makes it possible to clearly display the overall status of a higher level overview derived from many individual status values. This superordinate level can be an abstract grouping of individual components or a business-critical application. For example, the status of an application email, consisting of various hosts, switches and services such as SMTP and IMAP, can be combined into a single display. The formulation of completely intangible and non-technical considerations is also possible here, for example the on-time availability of a product to be delivered: This goal lies in the future and depends on many factors, such as the supply chain, reliably functioning production, available personnel, etc. Any threats to this abstract goal can be identified and captured via the BI module.

## Check

In Checkmk, a check is a script or program that evaluates a host or service according to predefined rules, i.e. the process that determines the status of hosts and services and which results in the display of a status of OK , DOWN , UNREACH , WARN , CRIT , PEND or UNKNOWN . Checks can be implemented, for example, with a check plug-in, local check, or active check.

## Check plug-in

Check plug-ins are modules written in Python that run on the Checkmk site and which create and evaluate the services of a host. For example, the check plug-in df , found within a site at ~/local/lib/python3/cmk_addons/plugins/<plug-in_family>/agent_based/ (when using the Check API V2), creates services for a hostâs existing mounted file systems based on data from an agent on the site, and checks those services against that data, such as how much free space is left.

## Checkmk extension package (MKP)

MKP is Checkmkâs own file format for aggregating and distributing extensions, i.e. custom check plug-ins, agent plug-ins, time series graph definitions, notification scripts, views, dashboards, etc.

## Checkmk Relay

A Checkmk Relay is a remote unit on a Checkmk site that enables monitoring via SNMP or special agents of hosts that cannot be reached by the Checkmk site itself, for example because a firewall configuration blocks incoming traffic from a network. The relay collects the monitoring data from these hosts and sends this data to the site. The Checkmk Relay can be used with Checkmk Ultimate.

## Configuration environment

The Checkmk web interface is divided into monitoring and configuration environments. The latter refers to the processes with which rules are defined, hosts and services are added and defined, users are managed, or general options are specified. The configuration environment is accessed via the Setup menu in the navigation bar.

## Contact

Contacts are Checkmk users who are responsible for specific hosts and services. The assignment of contacts to hosts and services is done via contact groups. Contacts can also be user accounts that exist purely for notifications, such as for forwarding to a ticket system.

## Dashboard

A dashboard is a freely-configurable overview consisting of views and/or so-called widgets . These elements are available, for example, in the form of lists (such as host problems), time series graphs or small 'speedometers' that display individual values such as a CPU temperature.

## Distributed monitoring

In a distributed monitoring, the entire monitoring system consists of multiple interconnected Checkmk sites, i.e. a central site and at least one remote site. The data from all sites is displayed together in one place at the central site. This is called the central status in a distributed monitoring system. Distributed monitoring can optionally be combined with a central setup .

## Distributed monitoring with central setup

With a central setup , the configuration of all Checkmk sites that are connected to each other in the distributed monitoring is carried out in a single location. The configuration is performed only at the central site and is then distributed to all remote sites. A central setup always includes a central status .

## Edition

The Checkmk editions are the various software variants of Checkmk. These are the Open Source Checkmk Community (formerly Checkmk Raw), for professional users the Checkmk Pro (formerly Checkmk Enterprise) available by subscription, and the Checkmk Ultimate (formerly Checkmk Cloud (Self-hosted)) which is based on Checkmk Pro. Checkmk Ultimate with Multi-Tenancy (formerly Checkmk MSP) is the multi-tenant extension of Checkmk Ultimate. In this order, each edition contains the complete range of functions of the previous editionâââand expands this with specific additional functions. For example, Checkmk Ultimate is a Checkmk Pro that has been expanded and optimized for monitoring hybrid environments.

## Event Console (EC)

When monitoring hosts and services, Checkmk focuses on states. The Event Console is the module that, in contrast, takes care of events , i.e. monitoring from sources such as syslog or SNMP traps, but optionally also the Windows Event Log, log files and own applications. An example: A warning message from the SMTP service on a mail server would not change the status/state of its host or servicesâââyet it is still relevant information that belongs in the monitoring. The Event Console can be used to record and display such events in Checkmk.

## Flapping

If an object (host or service) changes its state multiple times over a short period, it is regarded as flapping and is marked with the icon. For an object identified as flapping, successive state changes trigger no further notifications. The flap detection can be switched on or offâââglobally or by ruleâââseparately for hosts and services.

## Host

Under Checkmk, a host is any stand alone, physical or virtual system that is monitored by Checkmk. These are usually components with their own IP address (servers, switches, SNMP devices, virtual machines), but also, for example, Docker containers or other logical objects which do not have such an IP address. Each host always has one of the states UP , DOWN , UNREACH or PEND , and always has at least one service.

## Host group

Hosts are primarily managed by folders in Checkmk. Host groups enable a different grouping of hosts to select hosts in monitoring, e.g. in views. Host tags, labels and folders are used to assign hosts to such groups via rules. Hosts can also be explicitly assigned to a host group.

## Host state

The state of a host, i.e. whether it can be reached via the network ( UP ), does not respond to requests from the network ( DOWN ) or whether its access path is blocked by failed intermediate devices (switches, routers, etc.) ( UNREACH ). For freshly added hosts that have never been queried before, there is also the PEND state, which is not a state in the true sense.

## Host tag

Host tags are characteristics that can be assigned to hosts so these can be targeted later in the configuration for rules or later in monitoring for views. Host tags are divided into groups, for example a tag group Operating systems can be set up with the tags Linux and Windows . Some tag groups are predefined, such as the type of Checkmk agent used or the IP address family used to record whether a host should be monitored over IPv4, IPv6, or both versions. The tags also have predefined values and a default value which is assigned to each host as long as it has not been overwritten with another option from the group.

## Label

Hosts can be given host tags, but they can also be given direct labels. A label consists of two parts (key and value), separated by a colon. Such arbitrary key-value pairs ( os:linux , os:windows , foo:bar , etc.) can be set directly on a hostâââwithout any prior configuration, as is necessary for host tags. Labels therefore have no predefined scope, nor do they have a default value, but are very dynamic. In particular, Checkmk can take objects automatically created by container systems such as Kubernetes, Azure, or AWS as hosts into monitoring, and then enrich them with labels generated automatically from their metadata. Labels can be used, for example, for selecting conditions in rules or for filtering in monitoring views.

## Livestatus

Livestatus is the most important interface in Checkmk. Through it, Checkmk users get the fastest possible live access to all of the data for the hosts and services being monitored. For example, the data in the Overview snap-in is retrieved directly through this interface. The fact that the data is fetched directly from RAM avoids slow disk accesses and gives fast access to monitoring without putting too much load on the system.

## Local check

A local check is a (self-written) extension, in the form of a script in any coding language, that runs on the monitored host. Unlike regular checks, the status calculation runs directly on the host. The results from a script are added to the regular agent output.

## Metric

Measurable and calculable values for services over time, such as temperature, utilization or availability, which can be used for graphs, for example. Past values are stored in RRDs (Round Robin Database) and by default retained for up to 4 years.

## Monitoring environment

The Checkmk web interface is divided into monitoring and configuration environments. The former refers to the processes through which the status of the monitored infrastructure is displayed; these include the inventory, dashboards, lists of hosts, services, events or problems, historical data and so on. The monitoring environment is accessed via the Monitor menu of the navigation bar.

## Navigation bar

The navigation bar is the main navigation panel in the Checkmk interface, on the left side with, among other things, the Monitor , Setup and Customize menus.

## Notification

With a notification, a Checkmk user is actively informed of problems or other monitoring events, via HTML email, SMS, Slack or similar. Who is notified and how is determined by the notification rules. For example, if Mr. Hirsch receives an email informing him that the filesystem / service on host myserver123 has changed from WARN to CRIT , it is because Mr. Hirsch is a contact for that host and a notification rule states that all contacts for the host should receive an email when one of its services changes to CRIT .

## Physical appliance

The physical appliance is a 19" server with pre-installed firmware prepared for Checkmk that can be deployed immediately in data centers. It comes with a graphical configuration interface that eliminates the need for any Linux knowledge.

## Piggyback

Some hosts that are part of the monitoring are not queried directly because they are not physical devices, but rather they are virtual machines or containers, or the data can only be provided by a third-party system. These third-party systems (the physical hosts) provide the data as an attachment in their own agent output and are called piggyback hosts by us. So, for example, a Docker server would piggyback the container data along with its own data. The containers in this example are then the piggybacked hosts.

## Pull mode

In the pull mode, the Checkmk agent listens for incoming connections from the Checkmk server on TCP port 6556. As soon as the agent receives a request, it sends the monitoring data to the server. Here, the initiative for data transmission comes from the server, which basically pulls the data from the agent. The pull mode is the default way to transmit data from the Checkmk agentâââand works in all Checkmk editions.

## Push mode

In the push mode, the Checkmk agent sends the monitoring data to the Checkmk server once per minute. The agent pushes the data transmission on its own and does not wait for a request from the server. The push mode is always required if the Checkmk server cannot access the network in which the host to be monitored and its agent are located, for example, in a cloud-based configuration. For this reason, the push mode is only available in Checkmk Ultimate .

## Quick Setup configuration

A Quick Setup configuration consists of four components that you already know as individual parts from the Setup of a Checkmk site. The components are a rule for the respective special agent, a host, a connection in the dynamic host management and an entry in the password store.

## Rule

Rules are the basis for configuring hosts and services in Checkmk. The rules in a rule set always control a single, focused aspect of a host or service. Rules can be provided with conditions, and can be 'stacked' on top of each other arbitrarily within a rule set. The rule evaluation then takes place from top to bottom, so that there can be standard rules for when no condition applies, as well as very special rules that only affect a very specific host. Many rule sets in Checkmk already have predefined default values, so that additional rules only need to be created for alternative requirements.

## Rule set

A rule set is applicable to a specific aspect of a host or service, such as CPU utilization thresholds. Any number of individual rules can be created within each rule set. For example, the CPU utilization on Linux/Unix rule set could contain two rules that set the service to WARN status at 90 percent on certain hosts and as low as 70 percent on others.

## Scheduled downtime

Scheduled downtimes are planned outages, for example for updates of certain hosts. Scheduled downtimes temporarily override notifications, and, for example, are accounted for in the availability calculation and temporarily prevent related hosts and services from showing up as problems.

## Service

A service is a logical object that summarizes one or more aspects of a host. For example, size, utilization and trends of file systems, CPU utilization, temperatures, age and number of running programs, ports, sensors and so on. At any given time, each service in the monitoring has one of the states OK , WARN , CRIT , UNKNOWN or PEND , is always assigned to exactly one host, and can optionally contain one or more metrics.

## Service discovery

As soon as a host has been added, Checkmk automatically detects all available services that can be included in the monitoringâââand keeps this list up to date even during operation. A service discovery can also be started manually at any time via the configuration of a host function.

## Service group

Like hosts, services can also be grouped together so that these groups can be filtered later in views or addressed specifically in the configuration. Groups can be formed by folders, host tags, host and service labels, and host and service names filtered via regular expressions.

## Service state

A serviceâs state is always OK WARN , CRIT or UNKNOWN , and describes the current state of the service according to predefined rules. For freshly added services that have never been queried before, there is also the PEND state, which is not a state in the strict sense.

## Sidebar

The sidebar can be displayed from the navigation bar with a mouse click. Users can add various snap-ins to the sidebar to make navigation easier or to show important status data at a glance.

## Site

A site is a single , currently running Checkmk monitoring project. Checkmk can be run in parallel on the same server as multiple, independent sites, for example to test different Checkmk versions or editions, or to run a separate monitoring for (new) hosts that are not (yet) to be included in production monitoring.

## Snap-in

Snap-ins, also called sidebar elements, are the individual building blocks that can be placed in the sidebar, for example Overview and Master control . Access to the snap-ins is provided by the plus icon at the bottom of the sidebar.

## SNMP

The 'Simple Network Management Protocol' is used to monitor and configure network devices such as routers, switches, or firewalls. Checkmk supports this protocolâââbut since it is comparatively inefficient, you should only use SNMP on devices that donât support better monitoring alternatives, such as special agents. SNMP devices that cannot be reached by the Checkmk site itself can be connected via the Checkmk Relay.

## Special agent

On some systems, the regular Checkmk agent cannot be installed and SNMP is not (satisfactorily) available. Instead, these systems provide management APIs based on Telnet, SSH or HTTP/XML. Via a special agent running on the Checkmk server, Checkmk queries these interfaces, integrating the host into Checkmk via API.

## Time period

In Checkmk it is possible to restrict things like notifications, availability calculations and even the general execution of checks to certain, regularly recurring time ranges. Time periods can be used, for example, to define daily working hours, to specify vacations and holidays, or to separate weekends from weekdays. These time periods can then be used in rules.

## View

In addition to the dashboards, the views are the most frequently used displays of hosts, services and other components in the Checkmk interface. These views are displayed as tables with attributes relevant to the current context. For example, All hosts and Host problems are views in monitoring. Supplied standard views can be customized in their display, and they can also serve as the basis for new views. It is also possible to create views from scratch.

## Virtual appliance

The virtual appliance is a system created for VMware ESXi, Microsoft Hyper-V, or Proxmox with pre-installed firmware prepared for Checkmk. It includes a graphical configuration interface that eliminates the need for any Linux knowledge.

## WATO

The 'Web Administration Tool' was the GUI tool for configuring Checkmk up until Checkmk version 1.6.0 . With the introduction of WATO, for the first time users had the ability to customize Checkmk through a web interface instead of by using configuration files. WATO was replaced in version 2.0.0 by the Setup menu in the navigation bar.

## Werk

The Checkmk software development is organized in so-called 'Werks'. Each change, bug fix or new feature that will have an impact on the userâs experience is recorded in a separate Werk, along with notes on impacts and any possible incompatibilities. The list of Werks is available directly in Checkmk via the Help menu in the navigation bar and on the Checkmk website .

