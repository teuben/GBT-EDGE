pro argus_onoff_freq,son,soff,vcal,ifnum=ifnum,fdnum=fdnum,maint=maint, freq=freq
;
;;Calibrates Argus with VANE cal scan vcal
;;Inputs:
;;son = on scan
;;soff = off scan
;;vcal = vane cal scan
;;ifnum = IFnum of spectral window
;;fdnum = beam_number - 1
;;
;;Output:
;;Ta*=Tsys*x(On-Off)/Off, where Tsys* is scalar 
;;
;;Warnings: uses container 1,2 in computations
;;
if (n_elements(ifnum) eq 0) then ifnum = 0
if (n_elements(fdnum) eq 0) then fdnum = 0
if (n_elements(maint) eq 0) then maint = 0
if (n_elements(freq) eq 0) then freq = 0


;;Get ON
gettp,son,fdnum=fdnum,ifnum=ifnum,quiet=1
copy,0,1

wait, 1

;;Get OFF
gettp,soff,fdnum=fdnum,ifnum=ifnum,quiet=1
copy,0,2
off=getdata(0)

wait, 1

;;Get Vane Cal scan
gettp,vcal,fdnum=fdnum,ifnum=ifnum,quiet=1
;;Compute Tcal
;;twarm in K currently file uses C
twarm=!g.s[0].twarm+273.15
time=!g.s[0].mjd

if freq eq 0 then begin
   freq=!g.s[0].reference_frequency/1.e9
endif

;elevation not available in data during maintenance
if (maint ne 0) then el=77.85
el=!g.s[0].elevation
getatmos,el=el,mjd=time,freq=freq,outvals
if (n_elements(tau) eq 0) then tau=outvals(0)
tatm=outvals(2)
am=1./sin(el*!pi/180.)
;;
tbg=2.725
tcal=(tatm -tbg) + (twarm-tatm)*exp(tau*am)
;;compute Tsys* = Tcal/(VANE/OFF -1)
tsysvec=tcal/(getdata(0)/off -1)
vtsys=median(tsysvec)

;; Ta*=Tsys*x(ON-OFF)/OFF
subtract,1,2
wait, 1
divide,0,2
wait, 1
!g.s[0].units='Ta*'
!g.s[0].tsys=vtsys
scale,vtsys
wait,1


return
end



