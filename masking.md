# Masking

Masking can be important for EDGE.   The default of the pipeline is to use
some fraction of the edge (the beginning and ending of an RA or DEC scan).
Typically we have 35 scans, each scan consisting of 61 integrations,
though often the final one if very short (and full of NaN).


?  there is the 'mask' where the OFF is defined, as on  Ta = Tsys * (ON-OFF)/OFF
!  there is the 'mask' where the baselines are determined

- if no mask (-m) is giving, it uses a default X% of the beginning and end of 
  a row (scan in GBT lingo)

- main dependencies:     gbtpipe, degas (depends on gbtpipe)

- flow in reduce.py:

```
  # 1) set up mask
  maskstrategy=functools.partial(gbtpipe.ArgusCal.SpatialMask, mask=np.any(mask, axis=0), wcs=wcs.WCS(hdu[0].header).celestial)
  or
  maskstrategy=functools.partial(gbtpipe.ArgusCal.ZoneOfAvoidance, radius=1*u.arcmin, 
  or
  maskstrategy=None

  # 2) calibration
  my_calscans(gal, scan, maskstrategy, maskfile, badfeeds=badfeeds)
      gbtpipe.ArgusCal.calscans(dirname, start=start, stop=stop, refscans=refscans, badfeeds=badfeeds, OffType=OffType, nProc=1, opacity=True, OffSelector=maskstrategy, varfrac=0.1)


  # 3) gridding
  edgegrid(gal, badfeeds, maskfile)
      gbtpipe.griddata(...)
      degas.postprocess.cleansplit(...)

```
