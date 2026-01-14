= Abstract
Can a rarely-played violin improve in sound quality by being played? It is a strong belief among musicians and manufacturers that playing "opens up" an instrument, although no study has been able to demonstrate this effect.
We have revisited this question by performing multiple types of measurements and by testing an alternative hypothesis: whether the violinist adapts to the instrument.

We conducted a controlled longitudinal study centered on three rarely-played violins. The protocol involved one test violinist who played the target violin daily until she considered it "opened" (six months), two control violins kept in storage, and a group of ten control violinists. To disentangle physical evolution from player adaptation, we performed a multimodal assessment at the beginning and end of the playing period. The protocol included: (1) input admittances measured via laser vibrometry, (2) musical recordings, (3) subjective violin ratings provided by the players, (4) blind listening tests, and (5) motion capture of the test violinist's bowing gestures.

Our results show no evidence of acoustical change in the played violin compared to control instruments, nor do they indicate any adaptation by the player.

= Methods

== Study Design and Participants
The experiment employed a longitudinal protocol comparing a "played" condition against a controlled storage condition over a six-month period. The cohort consisted of 11 professional violinists. One musician, a professional soloist, was designated as the *Test Violinist* and performed the daily playing intervention. The remaining 10 participants served as a *Control Group*; this group consisted of professional and semi-professional violinists who were naive to the specific goals of the study and the roles of the instruments, participating solely in the measurement sessions.

Three "rarely-played" violins were selected for the study. The *Test Violin* was selected by the Test Violinist based on its perceived potential to "open up." Two additional instruments served as *Control Violins*. While the Test Violin was played extensively, the Control Violins were kept in the instrumental collection of the _Conservatoire National Supérieur de Musique et de Danse de Paris_ (CNSMDP). This location provided a stable, instrument-friendly storage environment comparable to a professional luthier’s workshop. To ensure consistent mechanical boundary conditions, all three violins were adjusted by a luthier prior to the study, equipped with identical strings and chinrests.

== Timeline and Procedure
The protocol was divided into three measurement sessions ($T_0, T_{1w}, T_{6m}$):
+ *Session 1 ($T_0$):* Baseline measurements (Phase 1).
+ *Session 2 ($T_{1w}$):* Measurements repeated one week later without playing intervention to establish test-retest reliability and measurement variability.
+ *Intervention Phase:* The Test Violinist played the Test Violin daily (with minor exceptions during concert tours). The Control Violins remained in storage. The duration of this phase was determined by the Test Violinist's subjective assessment of the instrument's evolution.
+ *Session 3 ($T_{6m}$):* Final measurements (Phase 2) conducted after the playing-in period concluded.

Following the physical and behavioral acquisitions, a listening test (Phase 3) was conducted to assess perceptual changes.

== Vibro-acoustical Measurements
Input admittance (point mobility) was measured using a Laser Doppler Vibrometer (Polytec OFV-505/OFV-3001) and an instrumented impact hammer (PCB 086E80). To simulate a supported boundary condition while minimizing damping of the corpus modes, violins were placed horizontally on a heavy table supported by a block of open-cell viscoelastic foam. Excitation was applied to the bridge on the G-string side, and velocity was measured at the E-string side.

== Musical Recordings
Recordings were acquired in a large dry room (approx. $100 "m"^2$) with low reverberation. Signals were captured using a stereo pair of DPA 4010 omnidirectional microphones positioned 50 cm from the player. To ensure longitudinal repeatability, microphone gain was fixed via the audio interface (RME Fireface) across all sessions, and player/microphone positions were standardized using floor markings.

The recording protocol for each violin consisted of a 5–10 minute familiarization period followed by the performance of standardized excerpts from the repertoire (scales and melodic phrases).

== Subjective Violin Ratings
Prior to the recording tasks, participants evaluated each violin based on three criteria: *Power*, *Ease of Playing*, and *Beauty of Tone* (rated on a continuous scale from 0 to 10). The presentation order of the violins was randomized for each participant.

_Note:_ Evaluations were performed under two conditions: a visual condition and a blinded condition (using opaque sunglasses). Preliminary analysis revealed no statistically significant interaction between the visual condition and the ratings. Consequently, to report results with maximum ecological validity, only the ratings from the visual condition are presented here.

== Motion Capture
Kinematic data of the Test Violinist were acquired using an OptiTrack Motive system comprising 12 cameras operating at 120 Hz. Passive reflective markers were attached to the Test Violin, the Control Violin, the player’s personal violin, and the bow. The system was calibrated to a mean residual error of $< ["XX mm"]$.

The procedure mirrored the audio recording protocol: markers were affixed, and the violinist performed the standardized repertoire after a warm-up period. Extracted features included bow velocity, bow-bridge distance, and bowing skewness.

== Listening Test
A perceptual evaluation was conducted using a custom browser-based interface (HTML/JS) with high-quality audio playback. The participant pool ($N=20$) included the 11 violinists from the study and 9 additional musicians. Participants used Sennheiser HD 100 headphones (or equivalent high-quality hardware for home-based participants).

Stimuli consisted of excerpts (opening of the Tchaikovsky Violin Concerto) cut to identical lengths. A fade-in/fade-out was applied, and loudness was normalized according to the EBU R128 standard. Participants were presented with pairs of recordings and asked to rate the dissimilarity on a scale of 0 to 10. Pairs included comparisons between sessions ($T_0$ vs. $T_{1w}$ and $T_0$ vs. $T_{6m}$) for both Test and Control instruments.

== Data Processing and Analysis

=== Admittance Processing
For each measurement point, the Frequency Response Function (FRF) was estimated using the $H_1$ estimator based on 5 consecutive impacts:

$ H_1(f) = (angle.l G_(x y, i)(f) angle.r) / (angle.l G_(x x, i)(f) angle.r) $

where $G_(x y, i)$ is the cross-power spectral density between the $i$-th impact force and velocity, $G_(x x, i)$ is the auto-power spectral density of the force, and $angle.l dot angle.r$ denotes the average over the 5 impacts.

To quantify repeatability, measurements were performed three times per session. The representative amplitude curve for each session was calculated as the Root Mean Square (RMS) of the linear magnitudes:

$ |H|_"session" = sqrt(1/3 sum_(k=1)^3 |H_(1,k)|^2) $

Finally, measurement uncertainty was defined as the standard deviation of the magnitudes converted to the decibel scale ($20 log_(10) |H_1|$).

=== Audio Feature Extraction
Audio recordings were resampled to 16 kHz for analysis. The Long-Term Average Spectrum (LTAS) was computed over the entire duration of the excerpt using Welch's method (Hann window, length 2048 samples, hop size 512 samples). To minimize the influence of transient outliers, the median was used

= Results

== Admittances Measurements
@fig:admittances presents the measured input admittances for the test violin (Klimke) and the two control violins (Levaggi, Stoppani). The top three panels show the frequency response functions for each instrument, while the bottom panel details the spectral difference between the two phases.

Visually, the frequency response functions exhibit high stability, with the post-playing curves (red, $T_"6m"$) largely superimposing onto the baseline curves (gray, $T_0$) for all instruments.

Regarding the spectral differences, while localized fluctuations are observable, it is crucial to note that the deviations recorded for the test violin are of the same order of magnitude as those observed for the control violins. The spectral changes for the played instrument do not exceed the baseline variability established by the unplayed instruments, suggesting that the measured variations are attributable to environmental factors or measurement reproducibility rather than a specific "playing-in" effect.

#figure(
  image("../figures/admittances.svg"),
  caption: [Input admittance measured at the bridge for the test violin (Klimke) and two control violins (Levaggi, Stoppani). Gray curves indicate the baseline phase ($T_0$) and red curves indicate the post-playing phase ($T_"6m"$). Shaded areas represent the measurement uncertainty (minimum and maximum values over 3 repetitions). The bottom panel displays the magnitude difference between Phase 2 and Phase 1 for each instrument.],
) <fig:admittances>

== Musical Recordings
@fig:ltas presents the Long-Term Average Spectra (LTAS) of scales recorded on the test violin (Klimke) and the two control violins (Levaggi, Stoppani). The data are organized by cohort: the Control Group (left column) and the Test Violinist (right column). The top three panels show the LTAS for each instrument, while the bottom panel details the difference between the two phases.

Visually, the spectra exhibit high stability between phases, with the post-playing curves (red, $T_"6m"$) largely superimposing onto the baseline curves (gray, $T_0$) for all instruments. This stability is observed both in the control group and on the recordings of the test violinist.

The LTAS differences displayed in the bottom panel indicate that the spectral deviations recorded for the test violin are of the same order of magnitude as those observed for the control violins. This suggests that the measured variations are attributable to environmental factors or measurement reproducibility rather than a specific "playing-in" effect.

#figure(
  image("../figures/recordings.svg"),
  caption: [Long-Term Average Spectra (LTAS) of scales recorded on the test violin (Klimke) and two control violins (Levaggi, Stoppani). The left column displays the average across the **Control Group** (10 violinists), while the right column displays the **Test Violinist**. Gray curves indicate the baseline phase ($T_0$) and red curves indicate the post-playing phase ($T_"6m"$). Shaded areas represent the variability range (min-max across participants for the left column; min-max across takes for the right column). The bottom panel displays the mean LTAS magnitude difference between Phase 2 and Phase 1.],
) <fig:ltas>
