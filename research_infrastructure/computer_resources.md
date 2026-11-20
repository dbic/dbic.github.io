---
title: "Computer resources"
source_url: https://www.dartmouth.edu/dbic/research_infrastructure/computer_resources.html
retrieved: 2026-11-04
lead: "How DBIC scans are stored, how to get access, and how to work with the data in DICOM and BIDS formats."
related:
  - { title: "Using Discovery", url: "/research_infrastructure/discovery.html" }
  - { title: "Datasets", url: "/research_infrastructure/datasets.html" }
  - { title: "Data & computing", url: "/data-computing.html" }
  - { title: "Who to contact", url: "/contact.html" }
---

[Research Infrastructure](index.md) >

# Computer resources

## Quick links

- [DBIC systems access](#sysaccess)
- [Data storage and access](#datastorage)
- [DICOM storage](#dicomstorage)
- [BIDS storage](#bidsstorage)
- [Using DataLad](#accessingbids)

<a id="sysaccess"></a>

## DBIC systems access

To use Discovery and other Research Computing systems, you need an HPC account (also known as a “Discovery account”). Everyone at Dartmouth has a NetID to provide authentication, but HPC access has to be set up before it will work: request it once, signing in with your NetID, at the [HPC account request page](https://dashboard.dartmouth.edu/research/hpc_account). Research Computing creates the account and emails you when it is ready; it includes a 50 GB home directory on DartFS.

For access to DBIC-specific resources (such as the shared datasets and our Discovery allocation) and for troubleshooting, we encourage you to contact DBIC directly, so that DBIC is in the loop: [Courtney Rogers](mailto:courtney.rogers@dartmouth.edu?subject=DBIC%20systems%20access) is the main contact point, and you can also write to [Jamie Ford](mailto:james.c.ford@dartmouth.edu?subject=DBIC%20systems%20access). Contacting Research Computing ([research.computing@dartmouth.edu](mailto:research.computing@dartmouth.edu?subject=DBIC); this opens a support ticket) works too: Research Computing will typically either redirect these topics to DBIC or contact DBIC on your behalf, so DBIC may be involved in access decisions whether or not you realize it.

<a id="datastorage"></a>

## Data storage and access

DBIC scans appear on DartFS immediately after they are acquired at the scanner (see `/dartfs/rc/lab/D/DBIC/DBIC/dbic-inbox/DICOM/`), and are organized by date and accession. Access permissions are set based on the registered group nightly.

If scans are resent from the scanner, note that:

1. Resent scans go to the same folder (based on date and accession) and will overwrite earlier versions if the series have not changed. If the series need to change, coordinate with DBIC or Research Computing to clear the earlier DICOM files before resending.
2. Scans resent after the day of acquisition do not trigger the automatic setting of access permissions; DBIC or Research Computing can trigger an update manually.

<a id="dicomstorage"></a>

## Storage of DICOM images

All MRI studies collected at DBIC are stored in the DICOM format, and organized according to acquisition date and an accession number that is intended to be unique. Thus a study recorded on Jul 4, 2019, with an accession number of A00001234 can be found on the server under the `DICOM/` directory above at `DICOM/2019/07/04/A00001234`.

Always enter a unique accession value, even for test scans, because it determines where the scan is stored. A scan with no accession is stored as `/unknown`, and scans with a blank or generic accession (such as “test”) are at risk of colliding on DartFS if they are run on the same day.

### How the transfer works

The DICOM files contain reconstructed MRI images obtained directly from the Siemens Console, which communicates with a dedicated virtual machine running a DICOM receiver (Orthanc). Orthanc carries out basic checking, maintains a temporary copy of scan data, and exports each DICOM to DartFS as it arrives.

<a id="bidsstorage"></a>

## Storage of BIDS

See also: the [DBIC Handbook](https://dbic-handbook.readthedocs.io) (a user maintained resource that supplements this site).

DBIC has adopted the [Brain Imaging Data Structure (BIDS)](https://bids.neuroimaging.io/ "BIDS") file-naming conventions for many recently acquired studies. BIDS is widely used in neuroimaging, and it supports data sharing, reproducible results and open science ([Center for Open Neuroscience](http://centerforopenneuroscience.org/ "Center for Open Neuroscience")), principles the DBIC promotes.

All DBIC investigators are encouraged to convert their data from DICOM to BIDS.

All BIDS formatted data are converted to the NIfTI Data Format
([NIfTI website](https://nifti.nimh.nih.gov "NIFTI"))
directly from the DICOM data and are stored on the same
server. However, because multiple sessions (each with unique accession
numbers and which may be acquired on different days) must be organized
together according to Study Protocol under the BIDS specification, the
organization for a particular study on the file server follows the
convention:
```
<server>:/inbox/BIDS/<PI>/<LeadInvestigator>/<StudyName>/{sid-000, ... sid-N}.
```
Here, `<PI>` is the Principal Investigator's name, `<LeadInvestigator>` is the person responsible for running the study (typically a graduate student), `<StudyName>` is a unique number and short name for the study, and `sid-XXX` are unique directories for each subject in the study. For example, all data for
the study number 1021 which investigated brain activity for viewing
actions, run by Dr. Sam Nastase, a former graduate student of
Prof. Jim Haxby, is located at `<server>:/inbox/BIDS/Haxby/Sam/1021\_actions`.

<a id="accessingbids"></a>

## Using DataLad

Researchers can use the DataLad file-sharing and data-versioning utility (datalad.org). DataLad makes it possible to access your data using the
same version control systems developed for git and git-annex, which
allows for downloading file hierarchies and meta-data, without
checking file contents (such as large volumes of time-series fMRI
data) into git, which would be costly in terms of storage
space. Instructions on how to use DataLad can be found on the [DataLad website](https://www.datalad.org "DataLad").

All MRI data at DBIC is collected following
[ReproIn](http://reproin.repronim.org "ReproIn") (NIH
1P41EB019936-01A1) convention.
