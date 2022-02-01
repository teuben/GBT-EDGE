pro vanecal_freq,scan1,ifnum=ifnum,maint=maint, freq=freq
;
;;Computes Tsys values for Argus beams for ifnum 
;
;;Inputs:
;;scan1 = vane scan (sky scan assume to be scan1+1
;;ifnum = IFnum of spectral window
;;plnum = pol-number =0 for argus
;;fdnum = beam-number -1 for argus
;;
;;Output:
;;Prints approximate effective Tsys* for each beam (Tsys* = Tsys *exp(tau)/eta_l)
;; Tsys*=Tcal[Coff]/[Con-Coff]
  
if (n_elements(ifnum) eq 0) then ifnum = 0
if (n_elements(maint) eq 0) then maint=0
if (n_elements(freq) eq 0) then freq=0

;;get center beam scan for ATM parameters
gettp,scan1,ifnum=ifnum,fdnum=10
;;Compute Tcal
;;twarm in C in header
twarm=!g.s[0].twarm+273.15
time=!g.s[0].mjd
el=!g.s[0].elevation
if freq eq 0 then begin
   freq = !g.s[0].reference_frequency/1.e9
endif 

;elevation not available in data during maintenance
if (maint ne 0) then el=77.85
getatmos,el=el,mjd=time,freq=freq,outvals
if (n_elements(tau) eq 0) then tau=outvals(0)
tatm=outvals(2)
am=1./sin(el*!pi/180.)
;;
tbg=2.725
tcal=(tatm -tbg) + (twarm-tatm)*exp(tau*am)

for i=0,15 do begin
  getsigref,scan1,scan1+1,ifnum=ifnum,fdnum=i,/quiet,tau=tau,ap_eff=0.3
  print,'beam, Tsys*[K]: ',i+1,tcal/median(getdata(0))    
endfor
print,'Tcal, Twarm, tatm:',tcal,twarm,tatm
return
end



