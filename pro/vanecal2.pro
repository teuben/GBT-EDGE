pro vanecal2,scan1,ifnum=ifnum,maint=maint,nfd=nfd
;
;;Computes Tsys mean,sigma,min,max for given vane scan
;   summary,"summary.list"
;   grep VANE summary.list  | awk '{printf("vanecal2,%d\n",$1)}'
;
;;Inputs:
;;scan1 = vane scan (sky scan assume to be scan1+1
;;ifnum = IFnum of spectral window
;;plnum = pol-number =0 for argus
;;nfd = number of argus beams (16 default)
;;maint=1 during maintenance, ignore for normal observing 
;;
;;Output:
;;Prints approximate effective Tsys* for each beam (Tsys* = Tsys *exp(tau)/eta_l)
;;Tsys*=Tcal[Coff]/[Con-Coff]
;;Also prints the mapping between fdnum and beam number as well as
;;weather conditions during the scan 

if (n_elements(ifnum) eq 0) then ifnum = 0
if (n_elements(maint) eq 0) then maint=0
if (n_elements(nfd) eq 0) then nfd = 16

;;get center beam scan for ATM parameters
gettp,scan1,ifnum=ifnum,fdnum=9
;;Compute Tcal
;;twarm in C in header
twarm=!g.s[0].twarm+273.15
;twarm=280.0
time=!g.s[0].mjd
el=!g.s[0].elevation
freq = !g.s[0].reference_frequency/1.e9
;elevation not available in data during maintenance
if (maint ne 0) then el=77.85
getatmos,el=el,mjd=time,freq=freq,outvals
if (n_elements(tau) eq 0) then tau=outvals(0)
tatm=outvals(2)
am=1./sin(el*!pi/180.)
;;
tbg=2.725
tcal=(tatm -tbg) + (twarm-tatm)*exp(tau*am)
tsys=0
tsys2=0
tsys_min=99999
tsys_max=-99999
for i=0,nfd-1 do begin
  gettp,scan1,ifnum=ifnum,fdnum=i,/quiet
  copy,0,2
  gettp,scan1+1,ifnum=ifnum,fdnum=i,/quiet
  copy,0,1
  subtract,2,1
  divide,0,1
  ; print,'fdnum, beam, Tsys*[K]: ',i,!g.s[0].feed,tcal/median(getdata(0))
  tsys1 = tcal/median(getdata(0))
  tsys  = tsys + tsys1
  tsys2 = tsys2 + tsys1*tsys1
  if (tsys1 lt tsys_min) then tsys_min = tsys1
  if (tsys1 gt tsys_max) then tsys_max = tsys1  
endfor
;print,'Tcal, Twarm, tatm:',tcal,twarm,tatm
tsys_m = tsys/nfd
tsys_s = sqrt(tsys2/nfd - tsys_m*tsys_m)
print,scan1,tsys_m,tsys_s,tsys_min,tsys_max
return
end



