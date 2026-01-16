#set heading(numbering: "1.")
#set text(font: "EB Garamond")

= Abstract
Can a rarely-played violin improve in sound quality by being played? It is a strong belief among musicians and manufacturers that playing "opens up" an instrument, although no study has been able to demonstrate this effect.
We have revisited this question by performing multiple types of measurements and by testing an alternative hypothesis: whether the violinist adapts to the instrument.

We conducted a controlled longitudinal study centered on three rarely-played violins. The protocol involved one test violinist who played the target violin daily until she considered it "opened" (six months), two control violins kept in storage, and a group of ten control violinists. To disentangle physical evolution from player adaptation, we performed a multimodal assessment at the beginning and end of the playing period. The protocol included: (1) input admittances measured via laser vibrometry, (2) musical recordings, (3) subjective violin ratings provided by the players, (4) blind listening tests, and (5) motion capture of the test violinist's bowing gestures.

Our results show no evidence of acoustical change in the played violin compared to control instruments, nor do they indicate any adaptation by the player.

= Methods

== Study Design and Participants
The experiment employed a longitudinal protocol comparing a "played" condition against a controlled storage condition over a six-month period. The cohort consisted of 11 professional violinists. One musician, a professional soloist and violin professor, was designated as the *Test Violinist* and performed the daily playing intervention. The remaining 10 participants served as a *Control Group*; this group consisted of professional and semi-professional violinists who were naive to the specific goals of the study and the roles of the instruments, participating solely in the measurement sessions.

Three "rarely-played" violins were selected for the study. The *Test Violin* was selected by the Test Violinist based on its perceived potential to "open up." Two additional instruments served as *Control Violins*. While the Test Violin was played extensively, the Control Violins were kept in the instrumental collection of the _Conservatoire National Supérieur de Musique et de Danse de Paris_ (CNSMDP). This location provided a stable, instrument-friendly storage environment comparable to a professional luthier's workshop. To ensure consistent conditions, all three violins were adjusted by a luthier prior to the study, equipped with identical strings and chinrests.

== Timeline and Procedure
The protocol was divided into three measurement sessions ($T_0, T_{1w}, T_{6m}$):
+ *Session 1 ($T_0$):* Baseline measurements (Phase 1).
+ *Session 2 ($T_{1w}$):* Measurements repeated one week later without playing intervention to establish test-retest reliability and measurement variability.
+ *Intervention Phase:* The Test Violinist played the Test Violin daily (with minor exceptions during concert tours). The Control Violins remained in storage. The duration of this phase was determined by the Test Violinist's subjective assessment of the instrument's evolution.
+ *Session 3 ($T_{6m}$):* Final measurements (Phase 2) conducted after the playing-in period concluded.

Following the physical and behavioral acquisitions, a listening test was conducted to assess perceptual changes at the end of the experiment.

== Vibro-acoustical Measurements
Input admittance was measured at the bridge using a Laser Doppler Vibrometer (Polytec OFV-505/OFV-3001) and an instrumented impact hammer (PCB 086E80). Violins were placed horizontally on a heavy table supported by a block of soft foam, and the strings were damped to minimize string resonances in the measurement. Excitation was applied to the bridge on the G-string side, and velocity was measured at the E-string side.

== Musical Recordings<sec:methods.recordings>
Recordings were acquired in a large dry room (approx. $100 "m"^2$) with low reverberation. Signals were captured using a stereo pair of DPA 4010 omnidirectional microphones positioned 50 cm from the player. To ensure longitudinal repeatability, microphone gain was fixed via the audio interface (RME Fireface) across all sessions, and player/microphone positions were standardized using floor markings.

The recording protocol for each violin consisted of a 5-10 minute familiarization period followed by the performance of standardized excerpts from the repertoire (scales and melodic phrases).

== Subjective Violin Ratings
Prior to the recording tasks, participants evaluated each violin based on three criteria: _Power_, _Ease of Playing_, and _Beauty of Tone_ (rated on a continuous scale from 0 to 10). The presentation order of the violins was randomized for each participant.

_Note:_ Evaluations were performed under two conditions: a visual condition and a blinded condition (using opaque sunglasses). Preliminary analysis revealed no statistically significant interaction between the visual condition and the ratings. Consequently, to report results with maximum ecological validity, only the ratings from the visual condition are presented here.

== Motion Capture
Kinematic data of the Test Violinist were acquired using an OptiTrack Motive system comprising 12 cameras operating at 120 Hz. Passive reflective markers were attached to the Test Violin, the Control Violin, the player's personal violin, and her bow.

The procedure mirrored the audio recording protocol: markers were affixed, and the violinist performed the standardized repertoire after a warm-up period. Extracted features included bow position and velocity, bow-bridge distance, and the string deflection.

== Listening Test
A perceptual evaluation was conducted using a custom browser-based interface (HTML/JS). The participant pool ($N=20$) included the 11 violinists from the study and 9 additional musicians. Participants used Sennheiser HD 100 headphones (or equivalent high-quality hardware for home-based participants).

Stimuli consisted of excerpts (opening of the Tchaikovsky Violin Concerto) recorded during the experiment (see @sec:methods.recordings) cut to identical lengths. A fade-in/fade-out was applied, and loudness was normalized according to the EBU R128 standard. Participants were presented with pairs of recordings and asked to rate the dissimilarity on a scale of 0 to 10. Pairs included comparisons between sessions ($T_0$ vs. $T_{1w}$ and $T_0$ vs. $T_{6m}$) for both Test and Control instruments, played by both a violinist from the control group and the test violinist.

== Data Processing and Analysis

=== Admittance Processing
For each measurement point, the Frequency Response Function (FRF) was estimated using the $H_1$ estimator based on 5 consecutive impacts:

$ H_1(f) = (chevron.l G_(x y, i)(f) chevron.r) / (chevron.l G_(x x, i)(f) chevron.r) $

where $G_(x y, i)$ is the cross-power spectral density between the $i$-th impact force and velocity, $G_(x x, i)$ is the auto-power spectral density of the force, and $chevron.l dot chevron.r$ denotes the average over the 5 impacts.

To quantify repeatability, measurements were performed three times per phase. The representative amplitude curve for each session was calculated as the Root Mean Square (RMS) of the linear magnitudes:

$ |H|_"session" (f) = sqrt(1/3 sum_(k=1)^3 |H_(1,k)(f)|^2) $

Given the limited sample size ($N=3$ repetitions per phase), standard statistical confidence intervals were deemed inappropriate. Instead, measurement variability is represented by the min-max envelope of the recorded magnitudes. For each frequency bin, this interval is defined by the minimum and maximum dB values observed across the three independent measurement blocks, providing a conservative estimate of the experimental reproducibility.

=== Audio Feature Extraction
Audio recordings were resampled to 16 kHz for analysis. While this reduces the signal bandwidth, previous work by @ballesteros2025 demonstrated that this sampling rate preserves the spectral features necessary for high-accuracy violin identification, with no loss in classification performance compared to high-resolution audio.

The Long-Term Average Spectrum (LTAS) was computed over the entire duration of the excerpt using Welch's method (Hann window, length 2048 samples, hop size 512 samples). To minimize the influence of outliers, the median was employed to aggregate the spectral frames.

= Results

== Admittances Measurements
@fig:admittances presents the measured input admittances for the test violin (Klimke) and the two control violins (Levaggi, Stoppani). The top three panels show the frequency response functions for each instrument, while the bottom panel details the spectral difference between the two phases.

Visually, the frequency response functions exhibit high stability, with the post-playing curves (gray, $T_"6m"$) largely superimposing onto the baseline curves (black, $T_0$) for all instruments.

Regarding the spectral differences, while localized fluctuations are observable, it is crucial to note that the deviations recorded for the test violin are of the same order of magnitude as those observed for the control violins. The spectral changes for the played instrument do not exceed the baseline variability established by the unplayed instruments, suggesting that the measured variations are attributable to environmental factors or measurement reproducibility rather than a specific "playing-in" effect.

#figure(
  image("../figures/admittances.png"),
  caption: [Input admittance measured at the bridge for the test violin (Klimke) and two control violins (Levaggi, Stoppani). Black curves indicate the baseline phase ($T_0$) and gray curves indicate the post-playing phase ($T_"6m"$). Shaded areas represent the measurement uncertainty (minimum and maximum values over 3 repetitions). The bottom panel displays the magnitude difference between Phase 2 and Phase 1 for each instrument.],
) <fig:admittances>

== Musical Recordings
@fig:recordings presents the Long-Term Average Spectra (LTAS) of scales recorded on the test violin (Klimke) and the two control violins (Levaggi, Stoppani). The data are organized by cohort: the Control Group (left column) and the Test Violinist (right column). The top three panels show the LTAS for each instrument, while the bottom panel details the difference between the two phases.

Visually, the spectra exhibit high stability between phases, with the post-playing curves (gray, $T_"6m"$) largely superimposing onto the baseline curves (black, $T_0$) for all instruments. This stability is observed both in the control group and on the recordings of the test violinist.

The LTAS differences displayed in the bottom panel indicate that the spectral deviations recorded for the test violin are of the same order of magnitude as those observed for the control violins. This suggests that the measured variations are attributable to environmental factors or measurement reproducibility rather than a specific "playing-in" effect.

#figure(
  image("../figures/recordings.png"),
  caption: [Long-Term Average Spectra (LTAS) of scales recorded on the test violin (Klimke) and two control violins (Levaggi, Stoppani). The left column displays the average across the Control Group (10 violinists), while the right column displays the Test Violinist. Black curves indicate the baseline phase ($T_0$) and gray curves indicate the post-playing phase ($T_"6m"$). Shaded areas represent the variability range (min-max across participants for the left column; min-max across takes for the right column). The bottom panel displays the mean LTAS magnitude difference between Phase 2 and Phase 1.],
) <fig:recordings>

== Subjective Violin Ratings
@fig:ratings presents the subjective evaluations provided by the musicians for each instrument (Klimke, Levaggi, Stoppani) and each criterion (Power, Ease of Playing, Tone). The top three rows illustrate the absolute ratings for each instrument, while the bottom row displays the rating difference between Phase 2 and Phase 1. Within each panel, ratings are shown for the Control Group ($N=10$) and the Test Violinist.

Consistent with the physical and acoustical measurements, the ratings exhibit high stability between the baseline ($T_0$, black) and post-playing ($T_{6m}$, gray) phases.

Inspection of the last row indicates that for the Control Group, the mean differences cluster near zero. While the confidence intervals exclude the null line for the Tone criterion (suggesting a statistically detectable shift for the Stoppani and Levaggi), the magnitude of these variations remains small ($<1$ point on a 10-point scale), likely reflecting slight fluctuations in group preference rather than a clear instrumental evolution. Similarly, the results provided by the Test Violinist do not reveal a systematic improvement of the played violin compared to the controls. Although she reported a distinct increase in Ease of Playing for the test violin (Klimke, blue), this trend was not replicated for Tone, where a control violin (Stoppani, green) was rated as having improved the most. This inconsistency—where unplayed instruments are perceived to improve as much as or more than the played instrument depending on the criterion—suggests that the observed variations stem from the natural variability of the musician's judgment rather than a physical "playing-in" effect.

#figure(
  image("../figures/ratings.png"),
  caption: [Subjective ratings for the test violin (Klimke) and two control violins (Levaggi, Stoppani) across three criteria: Power, Ease of Playing, and Tone. The top three rows display the absolute ratings, while the bottom row displays the rating difference between Phase 2 and Phase 1. Within each panel, results are stratified by rater: the Control Group ($N=10$) and the Test Violinist. Black markers indicate the baseline session ($T_0$) and gray markers indicate the post-playing session ($T_{6m}$). Transparent dots represent individual ratings, while solid dots with error bars represent the mean $plus.minus$ 95% confidence interval.],
) <fig:ratings>

== Listening Test
@fig:tests presents the results of the listening test. Participants rated the instrument dissimilarity between pairs of recordings on a scale from 0 (identical) to 10 (very different). The analysis focuses on "same-violin" pairs to quantify perceptual evolution.

The top three rows display the raw dissimilarity ratings. The baseline comparisons (Phase 1 vs. Phase 1, black markers, $Delta_(11)$) yield ratings averaging between 3 and 4, establishing a "perceptual noise floor" caused by natural performance variability between takes. The cross-session comparisons (Phase 1 vs. Phase 2, gray markers, $Delta_(21)$) generally result in slightly higher dissimilarity ratings.

To isolate the specific effect of the six-month interval, the bottom row displays the net perceptual shift, calculated as the difference between the cross-session ratings and the baseline ratings ($Delta_(21) - Delta_(11)$). For the Control Group listeners, the confidence intervals for this net shift encompass zero for nearly all conditions, indicating no statistically significant audible change. The sole exception is the control violin (Levaggi, orange) recorded by the Test Violinist, which exhibits a statistically significant positive shift. Crucially, the played test violin (Klimke, blue) shows no such effect (CI crosses zero in all cases). These results support a twofold conclusion. First, the null result for the test violin played by the control group indicates no audible acoustical evolution of the instrument itself. Second, the null result for the test violin played by the test violinist suggests that if the player did adapt to the instrument over six months, this adaptation did not result in a perceptible modification of the produced sound.

#figure(
  image("../figures/tests.png"),
  caption: [Results of the pairwise listening test. The top three rows display the mean dissimilarity ratings (0=Identical, 10=Very Different) for "same-violin" pairs. Black markers ($Delta_(11)$) represent the baseline dissimilarity between two takes from Phase 1. Gray markers ($Delta_(21)$) represent the dissimilarity between a Phase 1 take and a Phase 2 take. The bottom row displays the net perceptual shift ($Delta_(21) - Delta_(11)$), quantifying the audible change over 6 months after subtracting the performance variability. Columns indicate the player who produced the stimuli, while the x-axis groups results by listener: the Control Group ($N=20$) and the Test Violinist.],
) <fig:tests>

== Motion Capture
@fig:mocap_xs presents the aligned bow position profiles ($x_s$) for the test violin (Klimke) and two reference instruments (the player's Personal Violin and the Stoppani control). Each column corresponds to a distinct musical excerpt. Black curves indicate the baseline phase ($T_0$) and gray curves indicate the post-playing phase ($T_"6m"$).

Visually, the Test Violinist exhibits high stability in her bowing strategy for each excerpt. The post-playing curves (gray, $T_"6m"$) largely superimpose onto the baseline curves (black, $T_0$) for all instruments.

Inspection of the bow position differences reveals that the deviations recorded for the test violin are of the same order of magnitude as those observed for the reference violins. The changes in bow position for the played instrument do not exceed the baseline variability established by the unplayed instrument (Stoppani) and the familiar instrument (Personal Violin). This suggests that the measured variations are attributable to natural motor variability or measurement reproducibility rather than a specific behavioral adaptation to the test violin.

#figure(
  image("../figures/mocap_xs.png"),
  caption: [Aligned bow position profiles ($x_s$) recorded on the test violin (Klimke) and two reference instruments (the player's Personal Violin and the Stoppani control). Columns correspond to distinct musical excerpts. Black curves denote the baseline phase ($T_0$) and gray curves denote the post-playing phase ($T_"6m"$). Shaded bands indicate the variability range across repeated takes. The bottom panel displays the mean bow position difference between Phase 2 and Phase 1.],
) <fig:mocap_xs>

#bibliography("Thèse.bib")
