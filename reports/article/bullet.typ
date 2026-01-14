#set heading(numbering: "1.")
#set text(font: "EB Garamond")

#title[
  #set align(center)
  Disentangling Physical Change from Player Adaptation in Violin "Playing-In": \
  A Longitudinal Study
]

= Introduction
- Topic :
  - "Playing-in" : long-term improvement of violin sound quality due to playing
    - strong belief among luthiers and players
    BUT
    - no physical evidence (@inta2005, @piacsek2023)

- SOTA
  - @inta2005, @piacsek2023
    - Null results regarding physical changes
    - Gaps
      - physical measurements of the instrument only $=>$ no player influence
      - player adaptation not investigated

- Research Hypotheses
  1. Vibro-acoustic evolution : violin properties change due to playing

    OR

  2. Musician adaptation : gestures' adjustments to the violin

- Proposed Approach
  - Longitudinal study involving
    - 1 "to-be-played" violin, 2 control violins
    - 1 "to-play" player, 10 control players
  - Multimodal Assesment
    - Vibro-acoustical measurements : radiativities
    - Musical recordings
    - Subjective violin ratings
    - Motion Capture measurements
    - Listening tests

= Methods
== Study Design
Goal : A longitudinal study comparing a "played" condition against controlled storage.

- 11 professional violinists
  - 1 test violinist : professional soloist. Will extensively play the test violin
  - 10 controls violinists :
    - professional and semi-professionals violinists
    - Naive to the experimental hypothesis: Participants were not informed about the "playing-in" goal nor the specific roles (Test vs. Control) of the instruments to avoid expectation bias.
    - participated only in measurements sessions

- 3 "not-played" violins
  - 1 test : selected by the "test" violinist for its "opening potential". Unknown for the other participants
  - 2 controls : kept in storage in the instrumental collection of the CNSMDP, except for measurements sessions.
  - violins are checked and adjusted according to the "test" player $=>$ same strings, same chinrests

=== Timeline
- Phase 1
  1. Session 1 : Measurements
    $ "ONE WEEK LATER (to measure variability)" $
  2. Session 2 : Measurements
- Playing-in period
  - test violinist plays the test violin daily (some exceptions during concert tours)
  - control violins remain in storage
  - ends when "test" player decides
- Phase 2 : Session 3 : Measurements
- Phase 3 : Listening tests

== Admittances Measurements
- Materials :
  - Laser Doppler Vibrometer (Polytec OFV-505/OFV-3001)
  - Impact hammer (PCB 086E80)
- Excitation at the G string
- Velocity at the E string
- Violins were placed horizontally on a heavy table, supported by a block of viscoelastic foam

== Musical Recordings
- Dry large room (approx. 10m×10m, surface ≈100m2) with low reverberation.
- Pair DPA-4010, 48000Hz
- Player position and microphone stand placement (50cm distance) were standardized using floor markings (tape) to ensure consistent source-receiver alignment.
- Gain was fixed via the RME Fireface interface preamp and remained constant across all sessions.
- Protocol
  - Play each violin for 5-10 min (familiarization phase)
  - For each each violin, record excerpts of the "repertoire" : a scale, ...
- Features extracted :
  - LTAS (@ballesteros2025)

== Subjective Violin Ratings
- The presentation order of the three violins was randomized for each participant to minimize order effects.
Before recordings, rate each violin over 3 criteria on a scale from 0 to 10 :
- Power
- Ease of play
- Beauty of tone

== Motion Capture
- Materials :
  - OptiTrack Motive + 12 cameras @ 120Hz + markers
  - Test violinist
  - Test violinist's bow
  - Test violin + 1 control violin + Test violinist's violin

- Markers: [See Figure X]. Passive markers were placed to track the 6-DOF motion of the violin and bow.

- Procedure :
  - Place markers on the bow and each violin
  - For each violin
    - Play it for 5-10 min (warming-up and / or familiarization)
    - Record excerpts of the repertoire : ...

- Extracted features :
  - bow velocity
  - bow-bridge distance
  - bowing skewness

- Alignment: To account for temporal variations between takes, time-series were aligned using Dynamic Time Warping (DTW) based on the longitudinal bow position (xs​: distance from the frog to the string contact point).

== Listening Test
- Population: N=20 participants (the 11 violinists from the study + 9 additional professional/semi-professional musicians).
- Interface: The test was conducted via a custom-developed browser-based interface (HTML/JS).

#figure(
  table(
    columns: (auto, 1fr, 1fr, 1fr, 1fr, 1fr, 1fr),
    align: center,
    table.header(
      table.cell(rowspan: 2)[Pair n°],
      table.cell(colspan: 3)[Stimuli 1],
      table.cell(colspan: 3)[Stimuli 2],
      [Violin], [Player], [Session], [Violin], [Player], [Session],
    ),
    [1], [Klimke], [SMD], [1], [Klimke], [SMD], [2],
    [2], [Klimke], [SMD], [1], [Klimke], [SMD], [3],
    [3], [Levaggi], [SMD], [1], [Levaggi], [SMD], [2],
    [4], [Levaggi], [SMD], [1], [Levaggi], [SMD], [3],
    [5], [Stoppani], [SMD], [1], [Stoppani], [SMD], [2],
    [6], [Stoppani], [SMD], [1], [Stoppani], [SMD], [3],
    [7], [Klimke], [SMD], [3], [Levaggi], [SMD], [3],
    [8], [Stoppani], [SMD], [1], [Klimke], [SMD], [1],
    [9], [Klimke], [SMD], [1], [Klimke], [SMD], [1na],
    [10], [Klimke], [SMD], [2], [Klimke], [SMD], [2],
    [11], [Klimke], [Norimi], [1], [Klimke], [Norimi], [2],
    [12], [Klimke], [Norimi], [1], [Klimke], [Norimi], [3],
    [13], [Levaggi], [Norimi], [1], [Levaggi], [Norimi], [2],
    [14], [Levaggi], [Norimi], [2], [Levaggi], [Norimi], [3],
    [15], [Stoppani], [Norimi], [1], [Stoppani], [Norimi], [2],
    [16], [Stoppani], [Norimi], [2], [Stoppani], [Norimi], [3],
    [17], [Klimke], [Norimi], [1], [Levaggi], [Norimi], [1],
    [18], [Stoppani], [Norimi], [1], [Klimke], [Norimi], [1],
    [19], [Klimke], [Norimi], [2], [Klimke], [Norimi], [2na],
    [20], [Klimke], [SMD], [1], [Klimke], [Norimi], [1],
  ),
  caption: [List of presented pairs in the listening test],
)<t:pairs>

== Data Processing and Analysis
=== Admittances
For each measurement, the Frequency Response Function (FRF) was computed using the $H_1$ estimator on 5 consecutive taps :
$ H_1 (f) = (<G_("xy", i) (f)>) / (<G_("xx", i) (f)>) $
where:
- $G_("xy", i)$ is the cross-power spectral density between the $i$-th impact force and the i-th bridge velocity
- $G_("xx", i)$ is the auto-power spectral density of the i-th impact force
- $< dot >$ denotes the average over the 5 consecutive impacts.

To assess repeatability, measurements repeated 3 times per session for each violin. Final curves are calculated as follows :
- Amplitude : the arithmetic mean of the square linear magnitudes $|H_1|^2$
- Uncertainty : the standard deviation of the magnitudes converted to dB scale ($20 log(|H_1|)$)

=== Recordings
- Recordings resampled to $16"kHz"$
- LTAS computed on the entire recording, using `scipy.signal.welch` method, with a Hann window of length 2048 and a hop length of 512 samples, and setting the averaging method to `median`
- Amplitudes converted to decibel scale

=== Listening test
- Recordings were kept in stereo, at their original sample rate of 48kHz.
- Recordings were cut manually in order to contain the exactly the same content (beginning of Tchaikovsky concerto)
- A fade-in and fade-out was applied to each recording
- The loudness of each recording was normalized using the EBU R128 loudness normalzation algorithm.

- Participants had to do the listening test using Sennheiser HD 100 headphones, except for three participants who had to do the test at home. They were told to use the highest quality headphones available.

=== Mocap
- For each take, bow parameters such as
- In order to account for slight temporal variations, multiple takes of the same excerpt were aligned using DTW based on the bow position profile.

= Results

== Admittances Measurements
#figure(
  image("../figures/admittances.svg"),
  caption: [Input admittance measured at the bridge for the test violin (Klimke) and two control violins (Levaggi, Stoppani). Gray curves indicate the baseline phase ($T_0$) and red curves indicate the post-playing phase ($T_"6m"$). Shaded areas represent the measurement uncertainty (minimum and maximum values over 3 repetitions). The bottom panel displays the magnitude difference between Phase 2 and Phase 1 for each instrument.],
) <fig:admittances>

== Musical Recordings
#figure(
  image("../figures/recordings.svg"),
  caption: [Long-Term Average Spectra (LTAS) of scales recorded on the test violin (Klimke) and two control violins (Levaggi, Stoppani). The left column displays the average across the **Control Group** (10 violinists), while the right column displays the **Test Violinist**. Gray curves indicate the baseline phase ($T_0$) and red curves indicate the post-playing phase ($T_"6m"$). Shaded areas represent the variability range (min-max across participants for the left column; min-max across takes for the right column). The bottom panel displays the mean LTAS magnitude difference between Phase 2 and Phase 1.],
) <fig:ltas>

== Subjective Violin Ratings
#figure(
  image("../figures/ratings.svg"),
  caption: [Subjective ratings for Power (P), Ease of Playing (F), and Tone Quality (T) given to the test violin (Klimke) and two control violins (Levaggi, Stoppani). Ratings are separated by rater type (x-axis: Control group vs. Test player). Blue markers indicate the baseline session ($T_0$) and orange markers indicate the post-playing session ($T_"6m"$). Transparent dots represent individual ratings, while the solid dot and bar represent the mean and 95% confidence interval.],
) <fig:ratings>

== Motion Capture
#figure(
  image("../figures/mocap_beta.png", width: 80%),
  caption: [Bow-bridge distance before and after the playing phase.],
) <fig:ratings>

== Listening Test
#figure(
  image("../figures/tests.svg"),
  caption: [Results of the listening test showing the excess dissimilarity after 6 months relative to the 1-week baseline($Delta_21 - Delta_31$). $Delta_31$ represents the perceived difference between Session 1 ($T_0$) and Session 3 ($T_"6m"$), while $Delta_21$ represents the perceived difference between Session 1 ($T_0$) and Session 2 ($T_"1w"$).
    Error bars indicate 95% confidence intervals; values crossing zero suggest that the long-term evolution was not distinguishable from short-term measurement variability.
  ],
) <fig:tests>

= Discussion

= Conclusion

= Acknowledgements
- Julien Dubois
- Léa Martinez
- Stéphanie-Marie Degand
- CNSM
- Mehdi Maglach
- François Longo
- Emma Barthe
- Victor Salvador Castrillo

#bibliography("Thèse.bib")
