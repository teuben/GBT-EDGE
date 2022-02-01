pro argus_fsw,fdnum=fdnum,ifnum=ifnum,maint=maint,scan,scal
;
;;Calibrates Argus in-band frequency switching scan
;;
;;scan=fsw track scan
;;scal=vanecal scan (uses SKY with scan number =scal+1)
;;ifnum = IFnum of spectral window
;;fdnum = beam_number - 1

if (n_elements(maint) eq 0) then maint=0
if (n_elements(ifnum) eq 0) then ifnum=0
if (n_elements(fdnum) eq 0) then fdnum=0

;;
;;use maint=1 for maintenance day test observations
;;
;;Output:
;;Ta*=Tcal*(Sig-Ref)/(VANE-SKY)
;;
;;Warnings: uses container 1 in computations
;;
;;Note if VANE,SKY are taken too far in time or position from Sig,Ref
;;then should use Sig,Ref data to estimate OFF for Tsys*
;;Tsys* = Tcal/(VANE/OFF -1)  (e.g., see argus_onoff.pro)
;;and Ta*=Tsys*x(Sig-Ref)/Ref which may give better baselines
;;

if n_elements(fdnum) eq 0 then fdnum = 1

;;Get ON
gettp,scan,plnum=plnum,fdnum=fdnum,ifnum=ifnum,sig_state=0
v1=getdata(0)
;;save copy of on for meta-data
copy,0,1
;;
obsfreq0 = !g.s[0].reference_frequency
freq=obsfreq0/1.e9
;;Get OFF
gettp,scan,plnum=plnum,fdnum=fdnum,ifnum=ifnum,sig_state=1
v2=getdata(0)

;;will get the shift of 2nd versus 1st
obsfreq1 = !g.s[0].reference_frequency
fs = (obsfreq1-obsfreq0)/!g.s[0].frequency_interval

;;Calibrate scan on Ta* using scal scan
;;Get Cal-ON
gettp,scal,plnum=plnum,fdnum=fdnum,ifnum=ifnum
v3=getdata(0)
;;
;;Get Cal-OFF
gettp,scal+1,plnum=plnum,fdnum=fdnum,ifnum=ifnum
v4=getdata(0)
;;
;;Compute Tcal
;;twarm in K currently file uses C
twarm=!g.s[0].twarm+273.15
time=!g.s[0].mjd
el=!g.s[0].elevation
;elevation not available in data during maintenance
if (maint ne 0) then el=77.85
getatmos,el=el,mjd=time,freq=freq,outvals
if (n_elements(tau) eq 0) then tau=outvals(0)
tatm=outvals(2)
am=1./sin(el*!pi/180.)
;;
tbg=2.725
tcal=(tatm -tbg) + (twarm-tatm)*exp(tau*am)

;;compute Ta*
print,'Tcal Tatm Twarm',tcal,tatm,twarm
tastar=tcal*(v1-v2)/(v3-v4)

copy,1,0
setdata,tastar

;;folding starts here
;;save the calibrated spectrum

copy,0,1

;shift it

gshift,fs

;subtract it and divide by 2 (i.e., average the two)
subtract,1,0
scale,0.5
!g.s[0].units='Ta*'

;;estimate Tsys*
vtsys=tcal*median(v4/(v3-v4))

!g.s[0].tsys=vtsys
show


return
end



