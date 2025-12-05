#set heading(numbering: "1.")

#title[
    #set align(center)
    Disentangling Physical Change from Player Adaptation in Violin \"Playing-In\": \
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
    - 10 controls : 
        - professional and semi-professionals violinists
        - blinded to the study goals
        - participated only in measurements sessions

- 3 "not-played" violins
    - 1 test : selected by the "test" violinist for its "opening potential". Unknown for the other participants
    - 2 controls : kept in storage except for measurements sessions
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

== Musical Recordings
- Dry large room
- Pair DPA-4010, 48000Hz, 50cm from the violinists
- Protocol 
    - Play each violin for 5-10 min (familiarization phase)
    - For each each violin, record excerpts of the "repertoire" : a scale, ...
- Features extracted :
    - LTAS (@ballesteros2025)

== Subjective Violin Ratings
Before recordings, rate each violin based on 3 criteria :
- Power
- Ease of play
- Beauty of tone

== Motion Capture
- Materials :
    - OptiTrack Motive + 12 cameras @ 120Hz + markers
    - Test violinist
    - Test violinist's bow
    - Test violin + 1 control violin + Test violinist's violin

- Procedure :
    - Place markers on the bow and each violin
    - For each violin
        - Play it for 5-10 min (warming-up and / or familiarization)
        - Record excerpts of the repertoire : ...

- Processing
    - Alignment using DTW
    - Extracted features :
        - bow velocity
        - bow-bridge distance
        - bowing skewness

== Listening Test


= Results

== Admittances Measurements
#figure(
    image("../figures/admittances.png", width: 80%),
    caption: [Admittances of the three violins before and after the playing phase.],
) <fig:admittances>

== Musical Recordings
#figure(
    image("../figures/ltas.png", width: 80%),
    caption: [LTAS of the three violins before and after the playing phase.],
) <fig:ltas>

== Subjective Violin Ratings
#figure(
    image("../figures/ratings.png", width: 80%),
    caption: [Subjective ratings of the three violins before and after the playing phase.],
) <fig:ratings>

== Motion Capture
#figure(
    image("../figures/mocap_beta.png", width: 80%),
    caption: [Bow-bridge distance before and after the playing phase.],
) <fig:ratings>

== Listening Test
#figure(
    image("../figures/tests.png", width: 80%),
    caption: [Subjective ratings of the three violins before and after the playing phase.],
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