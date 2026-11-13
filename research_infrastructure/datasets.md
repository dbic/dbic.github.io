---
title: "DBIC-hosted datasets"
source_url: https://www.dartmouth.edu/dbic/research_infrastructure/datasets.html
retrieved: 2026-11-04
lead: "Public datasets hosted at the DBIC for DBIC users: where each one lives, how to reach it, and any access terms."
related:
  - { title: "Computer resources", url: "/research_infrastructure/computer_resources.html" }
  - { title: "Using Discovery", url: "/research_infrastructure/discovery.html" }
  - { title: "Data & computing", url: "/data-computing.html" }
  - { title: "Who to contact", url: "/contact.html" }
---

[Research Infrastructure](index.md) >

# Public datasets hosted by DBIC

Recently, the world-wide neuroscience community has experienced a rise in data sharing efforts aimed at increasing transparency and reproducibility of experimental findings.  As a result, many collated and annotated functional imaging datasets have become publicly available. Access to such resources provides investigators and students a great opportunity to explore and test models of brain function and cognition. However, many datasets are very large and can be challenging for individuals to access. To facilitate easy access and promote the use of publicly available data resources at DBIC, we host several datasets on the Dartmouth Research Computing file system where they are readily available to DBIC users for analyzing on the Discovery cluster.

### List of hosted datasets

- [Amsterdam Open MRI Collection (AOMIC)](#aomic)
- [Bissett Self-Regulation Dataset](#bsrd)
- [DBIC QA dataset](#dbicqa)
- [HCP Young Adult](#HumanConnectomeProject)
- [HCP Lifespan: Aging and development](#lifespan)
- [Healthy Brain Network (HBN)](#hbn)
- [ImageNet database](#imagenet)
- [Individual Brain Charting](#ibc)
- [Life](#life)
- [Narratives dataset](#Narratives)
- [Natural Scenes Dataset (NSD)](#NaturalScenes)
- [Spacetop](#spacetop)
- [The Moth](#moth)
- [103 Tasks dataset](#tasks)

### Contact

For questions about existing datasets or requests to add new datasets, please contact Jamie Ford (James.C.Ford@dartmouth.edu)

<a id="dbicqa"></a>

## DBIC QA dataset

The Dartmouth Brain Imaging Center's QA data, converted to BIDS standard, can be accessed using the DataLad file-sharing and data-versioning utility (see: <https://www.datalad.org/>).

- **Path to DBIC QA data on Discovery:** /dartfs/rc/lab/D/DBIC/DBIC/dbic-inbox/BIDS/dbic/QA
- **Access:**Open (no restrictions to rc-DBIC users)

### Online resources

- [Clone of DBIC QA dataset - DataLad Repository](https://datasets.datalad.org/?dir=/dbic/QA)

<a id="Narratives"></a>

## Narratives dataset

The Narratives Dataset is a large collection of fMRI studies in natural language processing conducted at [Princeton Neuroscience Institute](https://pni.princeton.edu/) by the labs of Professors [Ken Norman](https://pni.princeton.edu/faculty/kenneth-norman) and [Uri Hasson](https://psychology.princeton.edu/people/uri-hasson) and procured by DBIC alumnus Dr. [Sam Nastase](https://snastase.github.io/). The dataset consists of normalized 3T fMRI data collected while subjects (345 individuals) listened to various spoken word narratives with 28 unique stories and over 800 scanning sessions. This dataset is a benchmark for testing models of language processing and language comprehension.

- **Path to the Narratives dataset on Discovery:** /dartfs/rc/lab/D/DBIC/DBIC/archive/narratives
- **Access:** Open (no restrictions to rc-DBIC users)

### Online resources

- [Nastase, S.A., Liu, YF., Hillman, H. et al. The “Narratives” fMRI dataset for evaluating models of naturalistic language comprehension. Sci Data 8, 250 (2021)](https://www.nature.com/articles/s41597-021-01033-3)
- [Narratives Dataset - DataLad Repository](http://datasets.datalad.org/?dir=/labs/hasson/narratives)

<a id="NaturalScenes"></a>

## Natural Scenes Dataset (NSD)

The [Natural Scenes Dataset (NSD)](https://naturalscenesdataset.org/) is a large ultra-high-field 7T fMRI dataset conducted by the [Center for Magnetic Resonance Research](https://www.cmrr.umn.edu/) at the University of Minnesota. It consists of high-resolution fMRI data collected from 8 adult subjects while they viewed thousands of images of natural scenes. Each subject was scanned multiple times with 30 to 40 sessions per subject. The NSD dataset is an excellent resource for testing models of visual representation and cognition.

- **Path to the NSD on Discovery:** /dartfs/rc/lab/D/DBIC/DBIC/archive/NSD.
- **Access:** Data Use Agreement (DUA) and group limited access permission
  - **Link to DUA:** <https://forms.gle/eT4jHxaWwYUDEf2i9>
  - **Group limited access permission**: Email [Jamie Ford](mailto:james.c.ford@dartmouth.edu?subject=NSD%20dataset%20access)

### Online resources

- <http://naturalscenesdataset.org>

<a id="HumanConnectomeProject"></a>

## HCP Young Adult

The Human Connectome Project  (HCP) is a massive collaborative undertaking led by PIs Dr. [David Van Essen](https://neuroscience.wustl.edu/people/david-van-essen-phd/) of Washington University and Dr. [Kamil Ugurbil](https://www.cmrr.umn.edu/facultystaff/kamil/) of the University of Minnesota. The DBIC currently hosts the HCP Young Adult dataset, which contains 3T MRI data (structural, diffusion, resting-state and task fMRI) from over 1,100 healthy adults ages 22–35, in two forms: HCP1200 (original) and HCP-YA 2025 (released in 2025).

- **Path to HCP YA datasets**:
  - /dartfs/rc/lab/D/DBIC/DBIC/archive/HCP/HCP1200
  - /vast/labs/DBIC/datasets/HCP-YA-2025
- **Access**: Data Use Agreement (DUA) and group limited access permission
  - **Link to DUA**: <https://balsa.wustl.edu/project?project=HCP_YA>
    - **note:** same agreement and access applies to both versions
  - **Group limited access permission:**Email [Jamie Ford](mailto:james.c.ford@dartmouth.edu?subject=Group%20limited%20access%20permission)

Information about the directory structure and file names: [HCP1200 guide (PDF)](../assets/dbic/docs/userguides/hcp_refmanual.pdf); [HCP-YA 2025 release documentation](https://www.humanconnectome.org/study/hcp-young-adult/document/hcp-young-adult-2025-release).

### Online resources

- <https://www.humanconnectome.org/study/hcp-young-adult>

<a id="hbn"></a>

## Healthy Brain Network (HBN)

The [Healthy Brain Network](https://fcon_1000.projects.nitrc.org/indi/cmi_healthy_brain_network/) (HBN) is a large 3T fMRI dataset conducted by the Child Mind Institute for developing human brains (ages 5–21). The whole study includes eye tracking, EEG and rich demographic and behavioral data that can be found [here](https://fcon_1000.projects.nitrc.org/indi/cmi_healthy_brain_network/). The data hosted by DBIC only includes the fMRI data. It consists of subjects under resting-state, eye-tracking calibration and watching two short movie clips ("Despicable Me" and "The Present").   We used the version from "[Reproducible Brain Charts](https://reprobrainchart.github.io/) (RBC)" and the 845 subjects passing the quality check by the RBC team (up to "Release 9" by the HBN team). The paper on "Reproducible Brain Charts" can be found [here](https://www.sciencedirect.com/science/article/abs/pii/S0896627325006610). In addition to the downloaded raw BIDS data and FreeSurfer 6 outputs, custom processing derivatives made with [fMRIPrep](https://zenodo.org/records/17087258) and [nb\_prep](https://zenodo.org/records/17087243) are included.

- **Path to HBN dataset on Discovery**: /dartfs/rc/lab/D/DBIC/DBIC/archive/HBN
- **Access:** Creative Commons (CC license) (open with restrictions)
  - The HBN data uses a [Creative Commons license](https://creativecommons.org/licenses/list.en) with "**BY-NC-SA**" restrictions.
    - **BY (attribution)**: citation requirements on eventual publications
    - **NC (non-commercial)**
    - **SA (share-alike):** if you reshare you must keep the CC restrictions

### Online resources

- <https://www.nature.com/articles/sdata2017181>
- [https://www.sciencedirect.com/science/article/pii/S0896627325006610](https://www.sciencedirect.com/science/article/abs/pii/S0896627325006610)

<a id="aomic"></a>

## Amsterdam Open MRI Collection (AOMIC)

The [Amsterdam Open MRI Collection](https://nilab-uva.github.io/AOMIC.github.io/) (AOMIC) is a collection of three independent, open-access datasets—known as ID1000, PIOP1, and PIOP2—collected at 3T and totaling over 1,300 unique participants (N=928, N=216, N=226, respectively). Participants received T1-weighted, diffusion-weighted (DWI), and fMRI imaging. The functional data in the largest component, ID1000, is from movie watching of natural scenes by 19-26 year olds, while the two PIOP datasets include resting state and task-based fMRI of university students, with the latter targeting emotion matching and working memory (both), face perception, cognitive control, and emotion anticipation (PIOP1 only), and response inhibition (PIOP2 only). Demographics and psychometric variables are also included.

- **Path to the AOMIC datasets on Discovery:** /vast/labs/DBIC/datasets/Amsterdam-Open-MRI
- **Access:** Open (no restrictions to rc-DBIC users)

### Online resources

- Snoek, L., van der Miesen, M.M., Beemsterboer, T. et al. The Amsterdam Open MRI Collection, a set of multimodal MRI datasets for individual difference analyses. Sci Data 8, 85 (2021). [https://doi.org/10.1038/s41597-021-00870-6](https://www.nature.com/articles/s41597-021-00870-6)

<a id="bsrd"></a>

## Bissett Self-Regulation Dataset

This dataset includes neuroimaging and behavioral data collected to examine the general construct of self-regulation. It consists of anatomical MRI, resting-state fMRI, and task-based fMRI (Stroop and Stop-signal) along with various self-report surveys from 103 healthy adult subjects.

- **Path to dataset on Discovery:** /vast/labs/DBIC/datasets/Bissett-Self-Regulation
- **Access:** Open (no restrictions to rc-DBIC users)

### Online resources

- Bissett, P.G., Eisenberg, I.W., Shim, S. et al. Cognitive tasks, anatomical MRI, and functional MRI data evaluating the construct of self-regulation. Sci Data 11, 809 (2024). [https://doi.org/10.1038/s41597-024-03636-y](https://www.nature.com/articles/s41597-024-03636-y)

<a id="ibc"></a>

## Individual Brain Charting

The Individual Brain Charting (IBC) dataset is a high-resolution 3T fMRI dataset collected at NeuroSpin, CEA Saclay, France. It consists of extensive functional imaging data from 12 participants who each underwent multiple scanning sessions. Paradigms span over 50 task conditions spanning cognitive domains such as visual perception, language, comprehension, and working memory. Participants also completed multiple naturalistic movie watching sessions. The IBC dataset is particularly valuable for studying individual variability in brain organization and for developing high-precision functional atlases. Two versions are installed: /IBC (EBRAINS, most complete) and /IBC\_openneuro (more strictly BIDS compliant and standardized, slightly fewer sessions).

**Path to dataset on Discovery**:  /dartfs/rc/lab/D/DBIC/DBIC/archive/Individual-Brain-Charting  
**Access:** Open (no restrictions to rc-DBIC users)

### Online resources

- Dataset documentation: <https://individual-brain-charting.github.io/docs/index.html> (EBRAINS), <https://openneuro.org/datasets/ds002685/versions/2.0.0>(OpenNeuro)
- Pinho, A.L., Amadon, A., Ruest, T. et al. Individual Brain Charting, a high-resolution fMRI dataset for cognitive mapping. Sci Data 5, 180105 (2018). <https://doi.org/10.1038/sdata.2018.105>

<a id="moth"></a>

## The Moth

The Moth dataset is a naturalistic 3T fMRI dataset conducted at
University of Texas, Austin by the lab of Professor Alexander
Huth. The dataset contains densely sampled fMRI data from 8
participants that listened to naturalistic narratives from The Moth
Radio Hour. Functional localizers are also available for all
participants. This dataset often serves as a benchmark for encoding
model performance in predicting language-associated brain activity.

- **Path to the dataset on Discovery:** /dartfs/rc/lab/D/DBIC/DBIC/archive/ds003020
- **Access:** Open (no restrictions to rc-DBIC users)

### Online resources

- Lebel, A., Jain, S., Pennington, J. et al. The Moth narratives: a naturalistic fMRI dataset. Sci Data 10, 421 (2023). [https://www.nature.com/articles/s41597-023-02437-z](https://www.nature.com/articles/s41597-023-02437-z)

<a id="tasks"></a>

## 103 Tasks dataset

The 103 Tasks dataset is a deep phenotyping dataset that includes 18 scans collected over 3 days from 6 participants (ages 22–33) in Osaka, Japan. Each day included 6 scans during which the full battery of tasks was completed. These include visual, auditory, motor, language, memory and introspective tasks. Each scan includes 77-83 tasks, and pairs of scans provide the full complement, thus providing both repeated measures within and across days within participant. Data were collected at 3 T using a gradient-echo multiband EPI sequence with a 2s TR and 2x2x2mm voxels. T1 images are also provided. Relative to other dense phenotyping datasets this dataset has relatively poor signal quality, but in exchange is especially task rich within scan and session allowing for characterization of high dimensional neural representations without scan or session confounds.

- **Path to the dataset on Discovery:**  
  /vast/labs/DBIC/datasets/103tasks
- **Access:** Open (no restrictions to rc-DBIC users)

### Online resources

- Nakai, Tomoya and Nishimoto, Shinji (2020). "Quantitative models reveal the organization of diverse cognitive functions in the brain". Nature Communications 11(1). [doi:10.1038/s41467-020-14913-w](https://rdcu.be/fwSiA)

<a id="imagenet"></a>

## ImageNet database

ImageNet is a large visual database (14M images) used to train visual object recognition and localization models. Images are categorized into 1,000 semantic sets ("synsets") which serve as object category labels. This dataset is used as part of the "ImageNet Large Scale Visual Recognition Challenge" (ILSVRC) and the 2012 version of the dataset has seen particular use in neuroAI applications for training feedforward neural network models for comparison with the ventral visual system and other brain networks. It is particularly well suited for training very deep neural networks like ResNets. This dataset includes a lot of small files and is stored as a tarball to avoid poor performance over NFS storage. Please copy the tarball to local scratch space (`/scratch`) and extract it there: this is orders of magnitude faster on HPC systems. A script that shows how to do this efficiently, `copy_imgnet_train_to_scratch.sh`, is provided in the top-level `ImageNet` folder.

- **Path to dataset on Discovery:** /vast/labs/DBIC/datasets/ImageNet
- **Access:** All users must read the ImageNet terms of access (<https://www.image-net.org/download.php>) and credit both the below citations.
  - **Group limited access permission: Email Jamie Ford**

### Online resources

- Deng J, Dong W, Socher R, Li L-J, Li K, Fei-Fei L. ImageNet: A large-scale hierarchical image database. CVPR 2009. <https://doi.org/10.1109/CVPR.2009.5206848>
- Olga Russakovsky\*, Jia Deng\*, Hao Su, Jonathan Krause, Sanjeev Satheesh, Sean Ma, Zhiheng Huang, Andrej Karpathy, Aditya Khosla, Michael Bernstein, Alexander C. Berg and Li Fei-Fei. (\* = equal contribution) ImageNet Large Scale Visual Recognition Challenge. arXiv:1409.0575, 2014.

<a id="spacetop"></a>

## Spacetop

Spacetop is a large-scale, multi-task 3T fMRI dataset collected at the Dartmouth Brain Imaging Center (DBIC) : N = 101 participants and 6 hours of scanning per participant, including 6 multifaceted functional tasks, 2 hours of naturalistic movie viewing, structural T1 images and multi-shell diffusion imaging as well as autonomic physiological data. The dataset combines a large sample, extensive data per participant (over 600 hours of data in total), and a wide range of experimental conditions, including cognitive, affective, social, and somatic/interoceptive tasks. This hosted version consists of BIDS-compliant fMRIPrep derivatives created using fMRIPrep version 25.1.4 (corresponding to OpenNeuro dataset ds007070, version 1.0.3).

**Path to dataset on Discovery:**/dartfs/rc/lab/D/DBIC/DBIC/archive/Spacetop **Access:**Open (no restrictions to rc-DBIC users)

### Online resources

- Dataset documentation: <https://openneuro.org/datasets/ds007070/versions/1.0.3> (OpenNeuro)
- Jung, H., Amini, M., Hunt, B.J. et al. Spacetop: A multimodal fMRI dataset unifying naturalistic processes with a rich array of experimental tasks. Sci Data **12**, 1465 (2025). <https://doi.org/10.1038/s41597-025-05154-x>

<a id="life"></a>

## Life

The Life Dataset is a naturalistic 3T fMRI dataset collected at the Dartmouth Brain Imaging Center (DBIC). In this naturalistic dataset, 18 subjects freely viewed segments of the “Life” nature documentary narrated by David Attenborough. The audiovisual stimulus was presented in four ~15-minute segments for ~1 hour of functional data in total for each participant.

**Path to dataset on Discovery:** /vast/labs/DBIC/datasets/Life  
**Access:** Open (no restrictions to rc-DBIC users)

### Online resources

- Van Uden, C. E., Nastase, S. A., Connolly, A. C., Feilong, M., Hansen, I., Gobbini, M. I., & Haxby, J. V. (2018). Modeling semantic encoding in a common neural representational space. Frontiers in Neuroscience, 12, 437. <https://doi.org/10.3389/fnins.2018.00437>
- Datalad Repository: <https://datasets.datalad.org/?dir=/labs/haxby/life>

<a id="lifespan"></a>

## HCP Lifespan: Aging and development

The Lifespan Human Connectome Project extends the HCP Young Adult study to characterize changes in brain structure, function, and connectivity across aging and development. The DBIC currently hosts the HCP-Aging (HCP-A) and HCP-Development (HCP-D) Lifespan 2.0 datasets. HCP-A includes data from 725 healthy participants ages 36–100+, while HCP-D includes data from 652 healthy participants ages 5–21, for a total of 1,377 participants.

The datasets include preprocessed structural MRI, resting-state fMRI, and task-based fMRI, as well as unprocessed structural MRI, diffusion MRI, resting-state and task-based fMRI, and arterial spin labeling data. HCP-A also includes high-resolution hippocampal T2-weighted imaging. Demographic, behavioral, and biomeasure data are available for both studies.

- **Path to the HCP Lifespan datasets on Discovery:** /vast/labs/DBIC/datasets/HCP-Lifespan
- **Access:** NDA Data Use Certification (DUC) and group-limited access permission
  - [NDA access and download instructions](https://www.humanconnectome.org/storage/app/media/documentation/LS2.0/LS_Release_2.0_Access_Instructions_June2022.pdf)
  - Group-limited access permission: Email Yuqi Zhang ([yuqi.zhang.gr@dartmouth.edu](mailto:yuqi.zhang.gr@dartmouth.edu?subject=HCP%20Lifespan%3A%20Aging%20%26%20Development)) and Jamie Ford ([james.c.ford@dartmouth.edu](mailto:james.c.ford@dartmouth.edu?subject=HCP%3A%20Aging%20%26%20Development))

### Online resources

- [HCP Aging](https://www.humanconnectome.org/study/hcp-lifespan-aging)
- [HCP Development](https://www.humanconnectome.org/study/hcp-lifespan-development)
