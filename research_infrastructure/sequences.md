---
title: "Sequences"
source_url: https://www.dartmouth.edu/dbic/research_infrastructure/sequences.html
retrieved: 2026-11-04
lead: "The sequences available on the scanner, and where to find their standard settings."
related:
  - { title: "fMRI scanner", url: "/research_infrastructure/fmri_scanner.html" }
  - { title: "Head coils", url: "/research_infrastructure/coils.html" }
  - { title: "Peripherals", url: "/research_infrastructure/peripherals.html" }
---

[Research Infrastructure](index.md) >

# Sequences

Mainstream sequences, including functional (BOLD), diffusion, anatomical (T1w, T2w, T2-FLAIR), spectroscopy, and angiography are available for use.

## Available sequences

Vendor supplied sequences come from Siemens; the others have been installed here.

| Kind of scan | Vendor supplied | Installed (CMRR or custom) | Settings (PDF) |
|---|---|---|---|
| **Functional MRI (BOLD)**: brain activity, from blood-oxygenation changes | ep2d_bold | cmrr_mbep2d_bold (also used for **multi-echo fMRI**) | [BOLD](../assets/dbic/docs/sequences/bold_acquisition.pdf); [Multi-echo fMRI](../assets/dbic/docs/sequences/multiechofmri.pdf) |
| **Diffusion**: the diffusion of water, used to map white-matter pathways | ep2d_diff; qDWI (q-space diffusion weighted) | cmrr_mbep2d_diff | [Diffusion](../assets/dbic/docs/sequences/dwi_acquisiton.pdf) |
| **Spectroscopy**: the chemical content of a chosen region | csi_se; csi_slaser | MEGA-PRESS (custom-installed) | |
| **Angiography**: blood vessel mapping | phase contrast (PC) and time of flight (TOF) | | |
| **Anatomical (T1w, T2w, T2-FLAIR)**: brain structure | mprage (T1w); T2w and T2-FLAIR sequences | | |
| **Field mapping**: magnetic-field uniformity, used to correct image distortion | field-mapping sequences | | |
| **Spin-echo EPI** | | cmrr_mbep2d_se | |

All of these sequences can be customized (for example slice thickness, repetition and echo times, or turning filters on and off) to suit each researcher’s needs.

## Simultaneous multislice (SMS)

Simultaneous multislice (SMS, also called multiband or MB) acquires several slices at once, so data can be collected faster. It can be used with either the vendor supplied BOLD and diffusion sequences or the CMRR versions that are installed.

## Multi-echo fMRI

This allows multiple images to be collected at different echo times (TEs) after a single excitation pulse, improving data quality and analysis options, though at the cost of analysis complexity and longer acquisitions (TRs). It is provided by the CMRR BOLD pulse sequences.

## CMRR sequences

The CMRR sequences are modified versions of the vendor supplied BOLD and diffusion pulse sequences, made by CMRR at the University of Minnesota. They give more flexibility to customize protocols. More about them: [CMRR multiband instructions (PDF)](https://www.cmrr.umn.edu/multiband/Multi-Band_C2P_Instructions_R016a.pdf).
