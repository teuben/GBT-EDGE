pro argus_mapcal,sc1,sc2,calsc,nint,cut=cut,datasm=datasm
;;
;;Calibrates total power OTF mapping assuming the edges of each scan
;;can be used as the OFF
;;
;;sc1=Initial scan leg
;;sc2=Final scan leg
;;calsc=VANE scan
;;nint=Number of Integrations in Scan leg
;;cut = rms level above which data are ignored in units of [K] in Ta*
;;datasm = smoothing the output data channels
 
;;Warning set baseline parameters before running
;;e.g., setregion on input example data
;;and modify nfit parameter below as needed

nfit,7

;;;
;;Writes output data file for each beam 
outfile1='keep_beam_'

;;
;;use end samples of each scan to define OFF
;;edge of sca
nn=nint-1
i1=0
i2=9
;;map range 10-291 int
i3=10
i4=nn-10
;;edge of scan
i6=nn-9
i7=nn

;;avoid showing plots which helps with speed
freeze
;;
;;rms threshold in K for data to ignore 
if (n_elements(cut) eq 0) then cut=1000.0
;;If no cut limit given then keep all data with rms < 1000.0 K 
;;
;;No smoothing if smoothing paramater not given
if (n_elements(datasm) eq 0) then datasm=1
;;
;;Input initial scan for info
gettp,sc1
nchans=fix(!g.s[0].bandwidth/!g.s[0].frequency_resolution)
;;Smoothing parameter to compute RMS to find bad data
nsmooth=30
;;Box for computing stats ignoring end channels
stat1=fix(0.05*nchans)
stat2=fix(0.95*nchans)

;;Get Vane Cal scan
gettp,calsc,fdnum=fdnum,ifnum=ifnum,quiet=1


;;Compute Tcal
;;twarm in C convert to K
twarm=!g.s[0].twarm+273.15
time=!g.s[0].mjd
freq=!g.s[0].reference_frequency/1.e9
el=!g.s[0].elevation
getatmos,el=el,mjd=time,freq=freq,outvals
if (n_elements(tau) eq 0) then tau=outvals(0)
tatm=outvals(2)
am=1./sin(el*!pi/180.)
;;
tbg=2.725
tcal=(tatm -tbg) + (twarm-tatm)*exp(tau*am)
vcal=median(getdata(0))

;;
outstats='Output_RMS_stats'
openw,lun,outstats,/GET_LUN,/append
printf,lun,'FDNUM SCAN INT  RMS[K]'
fmt='(i3,i6,i6,f12.5)'
free_lun,lun

;;Loop over Beams
for kk=0,15 do begin
;;Hack to make string with beam number 
   if (kk lt 10) then st2=string(kk,format='(i1)')
   if (kk ge 10) then st2=string(kk,format='(i2)')
   fileout,outfile1+st2+'.fits'
;;beams are k, scans are ii
   for ii=sc1,sc2 do begin
      chunk = getchunk(scan=ii,fdnum=kk,count=nchunk)
;;Averaging OFF data for scan
      for j =i1,i2 do accum, dc=chunk[j]
      for j =i6,i7 do accum, dc=chunk[j]
      ave
;;Copy OFF to container 1 
      copy,0,1
      vec=median(getdata(0))
;;Compute Tsys*=Tcal/(VANE/OFF -1.0)
      mytsys=tcal/(vcal/vec - 1.)    
;;Calibrate via tsys*(ON-REF)/REF for every ON sample in scan
      for j =i3,i4 do begin 
         set_data_container,chunk[j],buffer=0
         subtract,0,1
         divide,0,1
         scale,mytsys
;;Fit and remove baseline 
         bshape
         baseline
;;Baseline removed data copied to container-2
         copy,0,2
;;Smooth data to detect possible baseline ripples 
;;using rms cut
         gsmooth,nsmooth
         stats,stat1,stat2,/chan,/quiet,ret=sres
;;Write output stats output file
         openw,lun,outstats,/GET_LUN,/append
         printf,lun,format=fmt,kk,ii,j,sres.rms
         free_lun,lun
;;Bring back unsmoothed baseline removed data
         copy,2,0
;;Smooth output data
         gsmooth,datasm,/decimate         
;;If rms < threshold cut then save data to keep file
         if (sres.rms lt cut) then begin
           print,'saving',kk,ii,j
           keep
         endif
      endfor
   endfor
endfor


return
end
