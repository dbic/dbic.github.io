---
title: "Computing"
source_url: https://www.dartmouth.edu/dbic/research_infrastructure/computer_resources.html
retrieved: 2026-11-04
lead: "How DBIC scans are stored, how to get access, and how to run analyses on DBIC's share of the Discovery cluster."
glance:
  - { kind: text, label: "Start here", title: "DBIC systems access", text: "Getting an HPC account, and who to ask", url: "#sysaccess" }
  - { kind: text, label: "Your scans", title: "DICOM scans", text: "Where scans appear and how they get there", url: "#dicomstorage" }
  - { kind: text, label: "Your scans", title: "BIDS and DataLad", text: "Converting and sharing your data", url: "#bidsstorage" }
  - { kind: text, label: "Your files", title: "Storage (DartFS)", text: "Home, lab and scratch space", url: "#discoverystorage" }
  - { kind: text, label: "Run jobs", title: "HPC (Discovery)", text: "DBIC's share of the cluster, nodes and limits", url: "#overview" }
  - { kind: text, label: "Run jobs", title: "Good practice", text: "Taking turns, requesting resources, credentials", url: "#bestpractices" }
related:
  - { title: "Datasets", url: "/data-computing.html" }
  - { title: "Dataset access details", url: "/research_infrastructure/datasets.html" }
  - { title: "Who to contact", url: "/contact.html" }
---

[Research Infrastructure](index.md) >

# Computing

<a id="sysaccess"></a>

## DBIC systems access

To use Discovery and other Research Computing systems, you need an HPC account (also known as a “Discovery account”). Everyone at Dartmouth has a NetID to provide authentication, but HPC access has to be set up before it will work: request it once, signing in with your NetID, at the [HPC account request page](https://dashboard.dartmouth.edu/research/hpc_account). Research Computing creates the account and emails you when it is ready; it includes a 50 GB home directory on DartFS.

For access to DBIC-specific resources (such as the shared datasets and our Discovery allocation) and for troubleshooting, we encourage you to contact DBIC directly, so that DBIC is in the loop: [Courtney Rogers](mailto:courtney.rogers@dartmouth.edu?subject=DBIC%20systems%20access) is the main contact point, and you can also write to [Jamie Ford](mailto:james.c.ford@dartmouth.edu?subject=DBIC%20systems%20access). Contacting Research Computing ([research.computing@dartmouth.edu](mailto:research.computing@dartmouth.edu?subject=DBIC); this opens a support ticket) works too: Research Computing will typically either redirect these topics to DBIC or contact DBIC on your behalf, so DBIC may be involved in access decisions whether or not you realize it.

<a id="dicomstorage"></a>

## DICOM scans

### Where scans appear

DBIC scans appear on DartFS immediately after they are acquired at the scanner (see `/dartfs/rc/lab/D/DBIC/DBIC/dbic-inbox/DICOM/`), and are organized by date and accession. Access permissions are set based on the registered group nightly.

If scans are resent from the scanner, note that:

1. Resent scans go to the same folder (based on date and accession) and will overwrite earlier versions if the series have not changed. If the series need to change, coordinate with DBIC or Research Computing to clear the earlier DICOM files before resending.
2. Scans resent after the day of acquisition do not trigger the automatic setting of access permissions; DBIC or Research Computing can trigger an update manually.

### Folders and accession numbers

All MRI studies collected at DBIC are stored in the DICOM format, and organized according to acquisition date and an accession number that is intended to be unique. Thus a study recorded on Jul 4, 2019, with an accession number of A00001234 can be found on the server under the `DICOM/` directory above at `DICOM/2019/07/04/A00001234`.

Always enter a unique accession value, even for test scans, because it determines where the scan is stored. A scan with no accession is stored as `/unknown`, and scans with a blank or generic accession (such as “test”) are at risk of colliding on DartFS if they are run on the same day.

### How the transfer works

The DICOM files contain reconstructed MRI images obtained directly from the Siemens Console, which communicates with a dedicated virtual machine running a DICOM receiver (Orthanc). Orthanc carries out basic checking, maintains a temporary copy of scan data, and exports each DICOM to DartFS as it arrives.

<a id="bidsstorage"></a>

## BIDS and DataLad

DBIC has adopted the [Brain Imaging Data Structure (BIDS)](https://bids.neuroimaging.io/ "BIDS") file-naming conventions for many recently acquired studies. BIDS is widely used in neuroimaging, and it supports data sharing, reproducible results and open science ([Center for Open Neuroscience](http://centerforopenneuroscience.org/ "Center for Open Neuroscience")), principles the DBIC promotes. All DBIC investigators are encouraged to convert their data from DICOM to BIDS. All MRI data at DBIC is collected following [ReproIn](http://reproin.repronim.org "ReproIn") (NIH 1P41EB019936-01A1) convention.

Researchers can also use the DataLad file-sharing and data-versioning utility ([datalad.org](https://www.datalad.org "DataLad")). For technical details, including how to set up DataLad, see the [DBIC Handbook](https://dbic-handbook.readthedocs.io) (a user maintained resource that supplements this site).

<a id="discoverystorage"></a>

## Storage (DartFS)

DBIC's own scans and hosted datasets are on the DBIC share of DartFS: see [DICOM scans](#dicomstorage) and the [Datasets](datasets.md) page.

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

<a id="overview"></a>

## HPC (Discovery)

### Overview

DBIC owns a share of the Research Computing (RC) Discovery cluster. RC's sharing policy gives share holders access to more than the resources they own, up to the limits shown below. The SLURM scheduler enforces these hard limits on resource allocation, so that once DBIC usage meets the limit, no more DBIC jobs can run until resources are freed. To ensure fair service for all DBIC users, the DBIC applies the policies below. RC system administrators implement and enforce them.

### Interactive nodes

Access to the Discovery cluster requires an HPC account (see [DBIC systems access](#sysaccess)); you then log on to an interactive node using SSH and your DartID credentials.

| Node | Address | Who can use it | Use it for |
|---|---|---|---|
| Discovery head node | discovery7.hpcc.dartmouth.edu | all Discovery users | file handling and submitting jobs via SLURM; not for interactive jobs that need a lot of memory or multiple processors |
| Ndoli | ndoli.dartmouth.edu | all DBIC users with Discovery access | High memory system for testing code and interactive jobs |
| Andes, Polaris | andes.dartmouth.edu, polaris.dartmouth.edu | all Discovery users | High memory systems for testing code and interactive jobs |

DBIC users are encouraged to use Ndoli for testing code before submitting large jobs to the cluster.

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

**Access to the DBIC allocation can be requested from [Courtney Rogers](mailto:courtney.rogers@dartmouth.edu?subject=DBIC%20allocation) or [Jamie Ford](mailto:james.c.ford@dartmouth.edu?subject=DBIC%20allocation), once you have an HPC account (see [DBIC systems access](#sysaccess)). Requests can also be made for variations from the standard DBIC TRES limits.**

### Queue priority

Fairshare scheduling is not currently active on Discovery, so balancing by historic usage is off, and all jobs are accepted and run on a “first come, first served” basis.

<a id="bestpractices"></a>

## Good practice

### Take turns by avoiding excessively long jobs

One way to ensure fair turn-taking is to run jobs that take a short time to complete so that the job queue keeps moving. So when possible users should aim to submit multiple short jobs as opposed to one long job that takes a long time to complete.

### Requesting resources

Jobs should only request as many resources as they actually need. So, if a job will run efficiently on 8 cores, the submission script should not request a larger number of cores, for example.

### Interactive sessions

Interactive sessions should be used to test and debug code before submitting large numbers of jobs that might crash or otherwise need to be run again. Interactive sessions can be run on the cluster to provide a shell for users to stop, start, and monitor the progress of the jobs they launch from the interactive command line. Interactive sessions can be run using multiple nodes and cores, with the limit of 240 cores per user. So, if a user runs an interactive session that uses 40 cores, they still have access to 200 cores while the interactive session is running.

It is also possible to run interactive jobs without using any cluster resources by running jobs directly from the command line without submitting any jobs to the cluster. DBIC maintains its own Discovery head node, Ndoli, which DBIC users can SSH to.

### Never share your login credentials

Your Dartmouth ID and password are needed to log in to your HPC account. Your Dartmouth ID gives access to personal information about you (your academic and employment status, pay, stipend, financial aid and tax records) and to the computing resources. Sharing your login credentials puts both at risk.

### Never borrow someone else's resources

If you are having trouble getting jobs done because you have maxed-out your TRES quota, do not ask another DBIC user to run your jobs on their idle account to get more resources: this is unfair to other users. All users should only run jobs under their account if they are directly involved in the project as a collaborator. So if two users are working on the same project, it should be fine for two users to divvy up the jobs and run them on two accounts.
