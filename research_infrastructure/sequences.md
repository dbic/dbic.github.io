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

Mainstream sequences, including [functional (BOLD)](../assets/dbic/docs/sequences/bold_acquisition.pdf), [diffusion](../assets/dbic/docs/sequences/dwi_acquisiton.pdf), spectroscopy, and anatomical (T1w, T2w, T2-FLAIR), are available for use.

## Standard sequences

Vendor supplied gradient and spin echo-based echo planer imaging sequences are available for BOLD (ep2d_bold) and Diffusion (ep2d_diff) imaging.

The following sequences - csi_se, csi_slaser, and the custom-installed MEGA-PRESS - are available for Spectroscopy.

Also available are the standard T1 weighted (mprage), q-space diffusion weighted (qDWI), and field-mapping sequences.

All of these sequences can be customized (for example slice thickness, repetition and echo times, or turning filters on and off) to suit each researcher’s needs.

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
