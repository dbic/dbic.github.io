---
title: "Sequences"
source_url: https://www.dartmouth.edu/dbic/research_infrastructure/sequences.html
retrieved: 2026-11-04
lead: "The sequences available on the scanner, and where to find their standard settings."
kit:
  listcards: ["Sequence settings"]
related:
  - { title: "fMRI scanner", url: "/research_infrastructure/fmri_scanner.html" }
  - { title: "Head coils", url: "/research_infrastructure/coils.html" }
  - { title: "Peripherals", url: "/research_infrastructure/peripherals.html" }
---

[Research Infrastructure](index.md) >

# Sequences

Sequences available for use in the DBIC are: [BOLD](../assets/dbic/docs/sequences/bold_acquisition.pdf), [Diffusion](../assets/dbic/docs/sequences/dwi_acquisiton.pdf), Spectroscopy, and multiple anatomical sequences (T1, T2, T2-flair)

## Standard sequences

The standard gradient and spin echo-based echo planer imaging sequences are available for BOLD (ep2d_bold) and Diffusion (ep2d_diff) imaging.

The following sequences - csi_se, csi_slaser, and the custom-installed "mega press" - are available for Spectroscopy.

Also available are the standard T1 weighted (mprage), q-space diffusion weighted (qDWI), and field-mapping sequences.

All of these sequences are customizable (e.g. adjusting T1/T2, slice thickness, turning on/off filters) to meet each researchers' needs and preferences.

## CMRR multiband sequences

In addition to the above sequences, we have also installed modified versions of the native [BOLD](../assets/dbic/docs/sequences/bold_acquisition.pdf) and [Diffusion](../assets/dbic/docs/sequences/dwi_acquisiton.pdf) sequences by CMRR at the University of Minnesota. These modified versions provide extended flexibilities to customize the protocols. The cmrr_mbep2d_bold is used to acquire multi-echo images for **multi-echo fMRI**.

- cmrr_mbep2d_bold
- cmrr_mbep2d_diff
- cmrr_mbep2d_se

You can learn more about these sequences in the [CMRR multiband instructions](https://www.cmrr.umn.edu/multiband/Multi-Band_C2P_Instructions_R016a.pdf).

\* Please note that both native (Siemens BOLD and Diffusion) sequences, as well as the cmrr versions, are capable of acquiring simultanous slices (SMS/MB).

## Sequence settings

- [BOLD](../assets/dbic/docs/sequences/bold_acquisition.pdf)
- [Diffusion](../assets/dbic/docs/sequences/dwi_acquisiton.pdf)
- [Multi-Echo fMRI](../assets/dbic/docs/sequences/multiechofmri.pdf)
