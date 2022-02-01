pro getatmos,el=el,mjd=time,freq=freq,OUTput
;;Procedure to return zenith opacity, AtmTsys, and effective Tatm 
;;from RMaddale


my1='/users/rmaddale/bin/getForecastValues -elev '
my2=string(el)
my3=' -freqList '
my4=string(freq)
my5=' -timeList '
my6=string(time)

mystr1=my1+my2+my3+my4+my5+my6

mystr2=mystr1+' -type AtmTsys'
mystr3=mystr1+' -type Opacity'
mystr4=mystr1+' -type Tatm'

;print,mystr1
;print,mystr2
;print,mystr3

spawn,mystr2,result1
spawn,mystr3,result2
spawn,mystr4,result3
print,'(zenith)',result2
print,result1
print,result3


tmp=strsplit(result2,/extract)
ztau=float(tmp[2])

tmp=strsplit(result1,/extract)
atmtsys=float(tmp[2])

tmp=strsplit(result3,/extract)
tatm=float(tmp[2])

OUTput=[ztau,atmtsys,tatm]
return
end

