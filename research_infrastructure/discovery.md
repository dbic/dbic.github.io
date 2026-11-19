---
title: "Using DBIC's Discovery allocation"
source_url: https://www.dartmouth.edu/dbic/research_infrastructure/discovery.html
retrieved: 2026-11-04
lead: "DBIC's share of the Discovery computing cluster: how to use it, the limits that apply, and good practice."
related:
  - { title: "Computer resources", url: "/research_infrastructure/computer_resources.html" }
  - { title: "Datasets", url: "/research_infrastructure/datasets.html" }
  - { title: "Data & computing", url: "/data-computing.html" }
  - { title: "Who to contact", url: "/contact.html" }
---

[Research Infrastructure](index.md) >

# Using DBIC's Discovery allocation

- [Overview](#overview)
- [Cluster usage](#clusterusage)
- [Best practices guidelines for SLURM cluster usage](#bestpractices)
- [Storage space on Discovery hard drives](#discoverystorage)
- [Be a good citizen](#citizen)

<a id="overview"></a>

## Overview

DBIC owns a share of 15 Nodes on the Research Computing (RC) Discovery cluster, each node comprising 16 cores totaling 240 cores. Under RC's sharing policy, Discovery users can, subject to availability, use additional nodes beyond their own, so the DBIC sets a limit of 240 cores on each DBIC user. Note that the SLURM scheduler enforces hard limits on resource allocation, so that once DBIC usage reaches a cap, no more DBIC jobs can run until resources are freed. To ensure fair service for all DBIC users, the DBIC applies the policies below. RC system administrators implement and enforce them.

### Interactive nodes

Access to the Discovery cluster requires logging on to an interactive node using SSH and your DartID credentials.

| Node | Address | Who can use it | Use it for |
|---|---|---|---|
| Discovery head node | discovery7.hpcc.dartmouth.edu | all Discovery users | file handling and submitting jobs via SLURM; not for interactive jobs that need a lot of memory or multiple processors |
| Ndoli | ndoli.dartmouth.edu | all DBIC users with Discovery access | High memory system for testing code and interactive jobs |
| Andes, Polaris | andes.dartmouth.edu, polaris.dartmouth.edu | all Discovery users | High memory systems for testing code and interactive jobs |

DBIC users are encouraged to use Ndoli for testing code before submitting large jobs to the cluster. For more information, see the [Dartmouth Services Portal: High Performance Computing](https://services.dartmouth.edu/TDClient/1806/Portal/Requests/ServiceCatalog?CategoryID=11669).

## Using DBIC's allocation


<a id="clusterusage"></a>

## Cluster usage

### Individual user limits

The SLURM job scheduler provides for specifying user limits for Trackable Resources (TRES), and all DBIC users have individual limits on TRES. This includes a hard limit of 240 cores that an individual can use at any time.

**The following limits are in effect for all DBIC Account users:**

| Limit | Whole DBIC group | Per person |
|---|---|---|
| Wall time (core-days) | 1680 | 163 |
| Maximum CPUs | 1280 | 240 |

Wall time is the time a job runs multiplied by the number of cores it uses. So the individual wall time (163 days or 3912 hours) allows for any of the following scenarios:

**A single user can simultaneously run:**

- One job that uses 16 cores for 10 days (10 \* 16 = 160 days)
- Four jobs that use 4 cores each running for ten days (4 \* 4 \* 10)
- 240 single core jobs that each run for 16 hours or less
- 120 two-core jobs that run for 16 hours or less
- 10 eight-core jobs that run for two days
- 10 sixteen-core jobs that run for 1 day

The most efficient way to get your jobs running is to split them into small chunks and submit them in parallel, so that each chunk uses few CPUs (ideally just one) and completes in a short time (a few hours is ideal). Long jobs that take up multiple cpus, while occasionally necessary, should be avoided.

**Access to the DBIC allocation can be requested from [Jamie Ford](mailto:james.c.ford@dartmouth.edu?subject=DBIC%20allocation). Requests can also be made for variations from the standard DBIC TRES limits.**

### Queue priority

Fairshare scheduling is not currently active on Discovery, so balancing by historic usage is off, and all jobs are accepted and run on a “first come, first served” basis.

<a id="bestpractices"></a>

## Best practices guidelines for SLURM cluster usage

### Take turns by avoiding excessively long jobs

Taking Turns is the essence of Fairshare on a cluster. One way to ensure fair turn-taking is to run jobs that take a short time to complete so that the job queue keeps moving. So when possible users should aim to submit multiple short jobs as opposed to one long job that takes a long time to complete.

### Requesting resources

Jobs should only request as many resources as they actually need. So, if a job will run efficiently on 8 cores, the submission script should not request a larger number of cores, for example.

### Interactive sessions

Interactive sessions should be used to test and debug code before submitting large numbers of jobs that might crash or otherwise need to be run again. Interactive sessions can be run on the cluster to provide a shell for users to stop, start, and monitor the progress of the jobs they launch from the interactive command line. Interactive sessions can be run using multiple nodes and cores, with the limit of 240 cores per user. So, if a user runs an interactive session that uses 40 cores, they still have access to 200 cores while the interactive session is running.

It is also possible to run interactive jobs without using any cluster resources by running jobs directly from the command line without submitting any jobs to the cluster. DBIC maintains its own Discovery head node, Ndoli, which DBIC users can SSH to.

<a id="discoverystorage"></a>

## Storage space on Discovery hard drives

Both the standard home directory quota and the free lab space below are set out in the [Research Computing Bill of Rights](https://rc.dartmouth.edu/research-computing-bill-of-rights/).

### Your home directory

Individual user accounts have a standard quota of 50 GB. This should be used for all code, writing, and anything that a user may need as they see fit. However, this space is not adequate for storing most datasets, and certainly not for multiple datasets. It is also insufficient for writing temporary files needed for complicated analyses and preprocessing.

### Lab space owned by your PI

All Dartmouth faculty can request 1 TB of free storage for their lab's data. This space should be shared among lab members, and managed among those members by respective labs. Faculty members can buy more Lab-dedicated space as needs and resources demand and allow.

### Temporary scratch space

There is a shared scratch space available to all users located at
`/dartfs-hpc/scratch` that can be used as a workspace for
analyses. Temporary files can sit there for long periods of time, and
users will be notified by sysadmins before anything gets deleted. It
is suggested that when processing data, users utilize this space as
needed, and then copy a results folder (without intermediate products)
to a permanent location, such as a home directory or lab directory.

<a id="citizen"></a>

## Be a good citizen

### Never share your login credentials

Your Dartmouth ID and password are needed to log in to your Discovery account. Your Dartmouth ID gives access to personal information about you (your academic and employment status, pay, stipend, financial aid and tax records) and to the computing resources. Sharing your login credentials puts both at risk.

### Never borrow someone else's resources

If you are having trouble getting jobs done because you have maxed-out your TRES quota, do not ask another DBIC user to run your jobs on their idle account to get more resources: this is unfair to other users. All users should only run jobs under their account if they are directly involved in the project as a collaborator. So if two users are working on the same project, it should be fine for two users to divvy up the jobs and run them on two accounts.
