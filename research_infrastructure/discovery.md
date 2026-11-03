---
title: "Using Discovery"
source_url: https://www.dartmouth.edu/dbic/research_infrastructure/discovery.html
retrieved: 2026-11-03
---

[Research Infrastructure](index.md) >

# DBIC Policy for Computing Resources on Discovery

- [Overview](#overview)
- [Cluster usage](#clusterusage)
- [Best practices guidelines for SLURM cluster usage](#bestpractices)
- [Storage space on Discovery hard drives](#discoverystorage)
- [Be a good citizen](#citizen)

<a id="overview"></a>

## Overview

DBIC owns a share of 15 Nodes on the Research Computing (RC) Discovery cluster, each node comprising 16 cores totaling 240 cores. RC's policy for sharing specifies that all share holders have access to five times the resources owned, giving DBIC account users access to 1200 cores in total at any given time. The SLURM scheduler enforces hard limits on resource allocation so that once the DBIC usage meets the limit, no more DBIC jobs can run until resources are freed. In order to ensure equitable service to all DBIC users and to preserve the peace in our community, we aim to adopt a DBIC-specific set of policies. These policies are explained below. The implementation and enforcement of policies will be carried out by the RC Systems Administrators.

### Interactive nodes

Access to the Discovery cluster requires logging on to an interactive node using SSH and your DartID credentials. The primary interactive head node ([discovery7.hpcc.dartmouth.edu](discovery7.hpcc.dartmouth.edu/index.md)) may be used for normal file manipulation and for submitting jobs to the cluster via SLURM. The head node must not be used for interactive jobs that require large amounts of memory or multiple processors.

**Ndoli:** For testing code or running interactive jobs, there is a DBIC-dedicated interactive node called Ndoli ([ndoli.dartmouth.edu](ndoli.dartmouth.edu/index.md)) available to all DBIC users with Discovery access. DBIC users are encouraged to use this resource for testing code before submitting large jobs to the cluster.

**Andes and Polaris**: Similar to Ndoli, but not limited to only DBIC users, interactive nodes Andes ([andes.dartmouth.edu](andes.dartmouth.edu/index.md)) and Polaris ([polaris.dartmouth.edu](polaris.dartmouth.edu/index.md)) are also available for interactive jobs that require large amounts of memory. For more information see the High Performance Computing section of the Dartmouth Services Portal."

The link above is :  
<https://services.dartmouth.edu/TDClient/1806/Portal/Requests/ServiceCatalog?CategoryID=11669>

## Using DBIC's Allocation

- [Cluster usage](#clusterusage)
- [Best practices guidelines for SLURM Cluster usage](#bestpractices)
- [Storage space on Discovery hard drives](#discoverystorage)
- [Be a good citizen](#citizen)

<a id="clusterusage"></a>

## Cluster Usage

### Individual User Limits on Trackable Resources and Quality of Service

The SLURM job scheduler provides for specifying user limits for Trackable Resources (TRES) by using a mechanism called Quality of Service (QOS). A QOS defines a level of service for all users who are assigned to that particular QOS. All DBIC users are assigned to a DBIC-specific QOS with individual limits on TRES. This includes a hard limit of 240 cores that an individual can use at any time, or one fifth of the DBIC total share.

**The following limits are in effect for all DBIC Account users:**

- GroupWallTime: 1680 days
- IndividualWallTime: 163 days
- GroupMaxCPUs: 1280
- IndividualMaxCPUs: 240

Note that the wall-time for a single job is the time the job is running multiplied by the number of cores that the job uses. So the individual wall time (163 days or 3912 hours) allows for any of the following scenarios:

**A single user can simultaneously run:**

- One job that uses 16 cores for 10 days (10 \* 16 = 160 days)
- Four jobs that use 4 cores each running for ten days (4 \* 4 \* 10)
- 240 single core jobs that each run for 16 hours or less
- 120 two-core jobs that run for 16 hours or less
- 10 eight-core jobs that run for two days
- 10 sixteen-core jobs that run for 1 day

The most efficient way to get your jobs running is to chunk them into small chunks, and submit them in parallel to the cluster, so that each job chunk uses a small number of cpu's (ideally just one!), and that the complete in a short amount of time (a few hours is ideal). Long jobs that take up multiple cpus, while occasionally necessary, should be avoided.

**Access to the DBIC allocation can be requested from [Jamie Ford](mailto:james.c.ford@dartmouth.edu?subject=DBIC%20allocation). Requests can also be made for variations from the standard DBIC TRES limits.**

### Queue Priority

Fairshare scheduling is not currently active on Discovery, so balancing by historic usage is off, and all jobs are accepted and run on a “first come, first served” basis.

<a id="bestpractices"></a>

## Best Practices Guidelines for SLURM Cluster Usage

### Take turns by avoiding excessively long jobs

Taking Turns is the essence of Fairshare on a cluster. One way to ensure fair turn-taking is to run jobs that take a short time to complete so that the job queue keeps moving. So when possible users should aim to submit multiple short jobs as opposed to one long job that takes a long time to complete.

### Requesting resources

Jobs should only request as many resources as they actually need. So, if a job will run efficiently on 8 cores, the submission script should not request a larger number of cores, for example.

### Interactive sessions

Interactive sessions should be used to test and debug code before submitting large numbers of jobs that might crash or otherwise need to be run again. Interactive sessions can be run on the cluster to provide a shell for users to stop, start, and monitor the progress of the jobs they launch from the interactive command line. Interactive sessions can be run using multiple nodes and cores, with the limit of 240 cores per user. So, if a user runs an interactive session that uses 40 cores, they still have access to 200 cores while the interactive session is running.

It is also possible to run interactive jobs without using any cluster resources by running jobs directly from the command line without submitting any jobs to the cluster. There are two nodes available on for this: x01 and ndoli. Just ssh to one of those nodes from Discovery, and have at it.

<a id="discoverystorage"></a>

## Storage space on Discovery Hard drives

### Your home directory

Individual User accounts have 50G standard quota. This should be used for all code, writing, and anything that a user may need as they see fit. However, this space is not adequate for storing most datasets, and certainly not for multiple datasets. It is also insufficient for writing temporary files needed for complicated analyses and preprocessing.

### Lab space owned by your PI

All Dartmouth Faculty can request a storage of 1T for free to host data for their lab. This space should be shared among lab members, and managed among those members by respective labs. Faculty members can buy more Lab-dedicated space as needs and resources demand and allow.

### Temporary Scratch Space

There is a shared scratch space available to all users located at  
/dartfs-hpc/scratch. This should be used as a work-space for all analyses. Temporary files can sit there for long periods of time, and users are notified by RC-SysAdmins before anything gets deleted. So, when processing data, users should utilize this space as needed, and then a final results folder (without intermediate steps) should be copied to a permanent location, such as a user's home directory or a directory owned and managed by the user's Lab, and ultimately (in the near future) for finalized data to a procured derivative on the shared DBIC partition.

<a id="citizen"></a>

## Be a good citizen

### Never share your login credentials

Your Dartmouth ID and password are needed to log in to your Discovery account. As you should be aware, your Dartmouth ID is connected to all of your personal information concerning your relationship with Dartmouth College, including your academic and employment status, including financial information such as salary, stipend, financial aid, and tax information. Therefore, it is crucial for your own protection and for the protection of the of the computing resources that you **never** share your login credentials.

### Never borrow someone else's resources

If you are having trouble getting jobs done because you have maxed-out your TRES quota, you should email the SLURM coordinator to request a temporary increase in your limits. However, it might be tempting to ask another DBIC user, whose account is otherwise idle, to run your jobs for you, thereby doubling the resources available on the cluster for running your jobs. Please don't do this because it is unfair to other users. All users should only run jobs under their account if they are directly involved in the project as a collaborator. So if two users are working on the same project, it should be fine for two users to divvy up the jobs and run them on two accounts.
