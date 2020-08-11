<Qucs Schematic 0.0.20>
<Properties>
  <View=48,-129,1287,965,1,0,0>
  <Grid=10,10,1>
  <DataSet=1x1-b-2.dat>
  <DataDisplay=1x1-b-2.dpl>
  <OpenDisplay=1>
  <Script=1x1-b-2.m>
  <RunScript=0>
  <showFrame=0>
  <FrameText0=Title>
  <FrameText1=Drawn By:>
  <FrameText2=Date:>
  <FrameText3=Revision:>
</Properties>
<Symbol>
</Symbol>
<Components>
  <IProbe w00 5 250 60 -26 16 0 0>
  <IProbe d00 5 300 170 -32 -26 0 3>
  <IProbe b00 5 340 310 -16 -26 0 3>
  <R R2 5 300 110 -15 -26 0 3 "R00" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "european" 0>
  <Vdc V0 5 140 90 18 -26 0 1 "V0" 1>
  <R R1 5 170 60 -26 15 0 0 "r_i_wl" 0 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "european" 0>
  <R R3 5 340 250 -15 -26 0 3 "r_i_bl" 0 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "european" 0>
  <GND * 5 100 460 0 0 0 0>
  <.DC DC1 1 440 -20 0 46 0 0 "26.85" 0 "0.001" 0 "1 pA" 0 "1 uV" 0 "no" 0 "150" 0 "no" 0 "none" 0 "CroutLU" 0>
  <Eqn Eqn1 1 500 60 -31 19 0 0 "r_i_wl=1" 1 "r_i_bl=2" 1 "R00=10" 1 "V0=1" 1 "yes" 0>
</Components>
<Wires>
  <280 60 280 80 "" 0 0 0 "">
  <280 80 300 80 "" 0 0 0 "">
  <300 200 300 220 "" 0 0 0 "">
  <300 220 340 220 "b00" 250 200 2 "">
  <200 60 220 60 "w00" 240 30 10 "">
  <100 120 140 120 "" 0 0 0 "">
  <100 120 100 420 "" 0 0 0 "">
  <340 340 340 420 "" 0 0 0 "">
  <100 420 340 420 "" 0 0 0 "">
  <100 420 100 460 "" 0 0 0 "">
</Wires>
<Diagrams>
</Diagrams>
<Paintings>
</Paintings>
