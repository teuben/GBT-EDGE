# RMS calculations

Taking the example of NGC0001:


                                         size          RMS     delta[km/s]   pixel[arcsec]  beam[arcsec]
      NGC0001_12co.fits              148 x 148 x 896    28 mK   3.9  *freq    1.61
      NGC0001_12CO.fits               98 x  98 x 189    19      3.81          1.61          6.43
      NGC0001_12CO_rebase3.fits       98 x  97 x 341    19      3.81
      ... _smooth2_hanning2.fits      97 x  98 x  86    11.7   15.2           1.61         12.85


# RMS per galaxy

NEMO commands to get the RMS:

      source lmtoy/nemo/nemo_start.sh
	
      gal=NGC0001
      fitsccd $gal/${gal}_12CO.fits - | ccdstat - bad=0 robust=t 
      -> look for "Sigma Robust"

here are the results:

      Galaxy              RMS (native)   elev
      ------              ------------   ----
      NGC0001               25           74?      ra:35    dec:37
      UGC01659              21           64?
      UGC02239              25           82?
	  
      NGC0169               26           69?
      NGC0932               28           68?
      UGC04262              32           40?
      NGC2449               25           69?
      UGC04258              28           76?
      UGC04136              28           ?        ra:44  dec:34
	  
      UGC04659              39           75?
