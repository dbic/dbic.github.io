---
title: "Computer Resources"
source_url: https://www.dartmouth.edu/dbic/research_infrastructure/computer_resources.html
retrieved: 2026-11-04
---

[Research Infrastructure](index.md) >

# Computer Resources

## Quick links

- [DBIC systems access](#sysaccess)
- [Data storage and access](#datastorage)
- [DICOM storage](#dicomstorage)
- [BIDS storage](#bidsstorage)
- [Accessing BIDS data using DataLad](#accessingbids)

<a id="sysaccess"></a>

## DBIC Systems Access

Research Computing ([research.computing@dartmouth.edu](mailto:research.computing@dartmouth.edu?subject=DBIC)) is available for providing new user accounts, access to data, and help with existing user accounts across campus. For access to DBIC specific resources (e.g., shared datasets and our allocation of Discovery CPUs), users are welcome to contact DBIC directly ([James.C.Ford@dartmouth.edu](mailto:james.c.ford@dartmouth.edu?subject=DBIC%20systems%20access)), as Research Computing will typically either redirect these topics to DBIC, or contact DBIC on your behalf.

<a id="datastorage"></a>

## Data Storage and Access

DBIC scans appear on DartFS immediately after they are acquired at the scanner (see /dartfs/rc/lab/D/DBIC/DBIC/dbic-inbox/DICOM/), and are organized by date and accession. Access permissions are set based on the registered group nightly. In the event scans are resent from the scanner for any reason, care should be exercised.  
1. Resent scans will go to the same folder (based on date and accession), and  
will overwrite prior versions if no changes in series have been made. (If  
series need to change, it is suggested to coordinate with DBIC and/or  
Research Computing to clear prior DICOM files before a resend.)  
2. When scans are resent after the initial date of acquisition, they do not  
trigger automated setting of access permissions (DBIC and/or Research  
Computing can manually trigger an update).

<a id="dicomstorage"></a>

## Storage of DICOM images

All MRI studies collected at DBIC are stored in the DICOM format, and organized according to acquisition date and an accession number that is intended to be unique. Thus a study recorded on July 4, 2019, with an accession number of A00001234 can be found on the server under the DICOM/ directory above at : /DICOM/2019/07/04/A00001234.  
In some situations, no accession number is assigned (e.g. for a test scan). In these cases, use of an identifiable and unique accession value is highly recommended, as this determines the path. A blank accession is stored as /unknown, and multiple scans using a blank value, or using generic names like “test”, will collide on DartFS if run on the same day.  
The DICOM files contain reconstructed MRI images obtained directly from the  
Siemens Console, which communicates with a dedicated virtual machine running a DICOM receiver (Orthanc). Orthanc carries out basic checking, maintains a temporary copy of scan data, and exports each DICOM to DartFS as it arrives.

<a id="bidsstorage"></a>

## Storage of BIDS

In addition to storage of the original DICOM images, DBIC has adopted the standard file-naming conventions specified in the Brain Imaging Data Structure (BIDS) protocol ([bids.neuroimaging.io](https://bids.neuroimaging.io/ "BIDS")) for many recently acquired studies. The BIDS format provides a convenient common framework for organizing and storing data that has been adopted widely in the neuroimaging community. The universal adoption of BIDS will enhance efforts for data sharing, reproduction of results, and promoting Open Science ([http://centerforopenneuroscience.org](http://centerforopenneuroscience.org/ "Center for Open Neuroscience")); which are all principles that DBIC aims to promote. All investigators at DBIC have the option of transforming their data from DICOM to BIDS. For instructions, please contact [Yaroslav Halchenko](mailto:yaroslav.halchenko@dartmouth.edu?subject=BIDS).

All BIDS formatted data are converted to the NIfTI Data Format ([https://nifti.nimh.nih.gov](https://nifti.nimh.nih.gov "NIFTI")) directly from the DICOM data and are stored on the same server. However, because multiple sessions (each with unique accession numbers and which may be acquired on different days) must be organized together according to Study Protocol under the BIDS specification, the organization for a particular study on the file server follows the convention: <server>:/inbox/BIDS/<PI>/<LeadInvestigator>/<StudyName>/{sid-000, ... sid-N}. Where <PI> is the name of the Principal Investigator, <LeadInvestigator> is the person responsible for the execution of the study (typically a graduate student), <StudyName> is a unique number and mnemonic shorthand for the study, and sid-XXX are unique directories for each subject in the study. For example, all data for the study number 1021 which investigated brain activity for viewing actions, run by Dr. Sam Nastase, a former graduate student of Prof. Jim Haxby is located at <server>:/inbox/BIDS/Haxby/Sam/1021\_actions.

<a id="accessingbids"></a>

## Accessing BIDS data using Datalad

To further promote data accesibility, sharing, and reproducibility, all BIDS formatted data on the DBIC server can be accessed using the DataLad file-sharing and data-versioning utility (datalad.org). DataLad makes it possible to access your data using the same version control systems developed for git and git-annex, which allows for downloading file hierarchies and meta-data, without checking file contents (such as large volumes of time-series fMRI data) into git, which would be costly in terms of storage space. Instructions on how to use DataLad can be found at [https://www.datalad.org](https://www.datalad.org "DataLad").

All MRI data at DBIC is collected following [ReproIn](http://reproin.repronim.org "ReproIn") (NIH 1P41EB019936-01A1) convention and provided to researchers as [BIDS](https://bids-specification.readthedocs.io "BIDS") datasets under [DataLad version control system](http://datalad.org "Datalad") (NSF CRCNS 1429999).

Suggested resource: [DBIC BIDS Handbook](https://dbic-handbook.readthedocs.io)

## DBIC Internal

- [Reports](https://rcweb.dartmouth.edu/DBIC/reports/) (Restricted access / NetID authentication required)
