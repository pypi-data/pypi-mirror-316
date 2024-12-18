import numpy as np
from datacube import DataCube

from astropy.visualization.wcsaxes import WCSAxes, WCSAxesSubplot
from astropy.visualization.wcsaxes.patches import _rotate_polygon
import astropy.units as u
from astropy.wcs import WCS
from astropy.io import fits
from astropy.io.fits import PrimaryHDU, Header
from astropy.coordinates import SkyCoord
from spectral_cube.lower_dimensional_structures import LowerDimensionalObject
from spectral_cube import SpectralCube
from reproject import reproject_interp

###test with matplotlib-3.4.2
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib.markers import MarkerStyle
from matplotlib.path import Path
from matplotlib.patches import Polygon, PathPatch, FancyArrow

from tqdm import tqdm



class ChannelMap():
	def __init__(self):
		pass



class EasyNorm():
	###functions to scale values
	def _norm_linear(x, **kws):
		return x
	def _norm_log(x, p=1000, **kws):
		r = x.copy()
		idx = (x>0) & (x<1)
		r[idx] = np.log(p*x[idx]+1)/np.log(p+1)
		#r[(x<0) | (x>1)] = x[(x<0) | (x>1)]
		return r
	def _norm_power(x, p=1000, **kws):
		r = x.copy()
		idx = (x>0) & (x<1)
		r[idx] = (p**x[idx]-1)/(p-1)
		#r[(x<0) | (x>1)] = x[(x<0) | (x>1)]
		return r
	def _norm_sqrt(x, p=2, **kws):
		r = x.copy()
		idx = (x>0) & (x<1)
		r[idx] = x[idx]**(1/p)
		#r[(x<0) | (x>1)] = x[(x<0) | (x>1)]
		return r
	def _norm_sq(x, p=2, **kws):
		r = x.copy()
		idx = (x>0) & (x<1)
		r[idx] = x[idx]**p
		#r[(x<0) | (x>1)] = x[(x<0) | (x>1)]
		return r
	def _norm_asinh(x, p=1000, **kws):
		r = x.copy()
		idx = (x>0) & (x<1)
		r[idx] = np.arcsinh(p*x[idx])/np.arcsinh(p)
		#r[(x<0) | (x>1)] = x[(x<0) | (x>1)]
		return r
	def _norm_sinh(x, p=1000, **kws):
		r = x.copy()
		idx = (x>0) & (x<1)
		r[idx] = np.sinh(np.arcsinh(p)*x[idx])/p
		#r[(x<0) | (x>1)] = x[(x<0) | (x>1)]
		return r

	def get(scale=None, **kws):
		if scale is None: scale = 'linear' ###default norm
		scale = scale.lower()
		if scale in ['lin', 'linear']:
			return EasyNorm.LinearNorm(**kws)
		elif scale in ['log']:
			return EasyNorm.LogNorm(**kws)
		elif scale in ['pow', 'power', 'powerlaw']:
			return EasyNorm.PowerNorm(**kws)
		elif scale in ['sqrt', 'squareroot']:
			return EasyNorm.SqrtNorm(**kws)
		elif scale in ['sq', 'square', 'squared']:
			return EasyNorm.SquareNorm(**kws)
		elif scale in ['asinh', 'arcsinh']:
			return EasyNorm.AsinhNorm(**kws)
		elif scale in ['sinh',]:
			return EasyNorm.SinhNorm(**kws)
		elif scale in ['he', 'histeq', 'histequal', 'histogramequalization']:
			return EasyNorm.HistEqualNorm(**kws)
		else: raise ValueError("norm should be one of 'lin', 'log', 'pow', 'sqrt', 'sq', 'asinh', 'sinh', and 'histeq'.")

	class NormBase(mpl.colors.Normalize):
		def __init__(self, functions, limit=None, vmin=None, vmax=None, clip=False, **func_kws):
			super().__init__(vmin, vmax, clip)
			self._forward, self._backward = functions
			self.func_kws = func_kws
			self._limit = limit

		@property
		def limit(self): return self._limit

		def __call__(self, value, clip=None):
			result = super().__call__(value, clip)
			#result[~result.mask] = self._forward(result[~result.mask])
			return np.ma.array(self._forward(result.data, **self.func_kws), mask=result.mask, copy=False)

		def inverse(self, value):
			result = self._backward(value, **self.func_kws)
			return super().inverse(result)

		def autoscale_None(self, A):
			A = np.asanyarray(A)
			if self.vmin is None and A.size:
				if self.limit is None:
					self.vmin = np.nanmin(A)
				else:
					#if self.limit == 'zscale':
					self.vmin = np.nanpercentile(A.compressed(), (100-self.limit)/2)
			if self.vmax is None and A.size:
				if self.limit is None:
					self.vmax = np.nanmax(A)
				else:
					self.vmax = np.nanpercentile(A.compressed(), (100+self.limit)/2)

	class LinearNorm(NormBase):
		def __init__(self, **kws):
			super().__init__((EasyNorm._norm_linear, EasyNorm._norm_linear), **kws)

	class LogNorm(NormBase):
		def __init__(self, **kws):
			if kws.get('p') is None: kws['p'] = 1000
			super().__init__((EasyNorm._norm_log, EasyNorm._norm_power), **kws)

	class PowerNorm(NormBase):
		def __init__(self, **kws):
			if kws.get('p') is None: kws['p'] = 1000
			super().__init__((EasyNorm._norm_power, EasyNorm._norm_log), **kws)

	class SqrtNorm(NormBase):
		def __init__(self, **kws):
			if kws.get('p') is None: kws['p'] = 2
			super().__init__((EasyNorm._norm_sqrt, EasyNorm._norm_sq), **kws)

	class SquareNorm(NormBase):
		def __init__(self, **kws):
			if kws.get('p') is None: kws['p'] = 2
			super().__init__((EasyNorm._norm_sq, EasyNorm._norm_sqrt), **kws)

	class AsinhNorm(NormBase):
		def __init__(self, **kws):
			if kws.get('p') is None: kws['p'] = 1000
			super().__init__((EasyNorm._norm_asinh, EasyNorm._norm_sinh), **kws)

	class SinhNorm(NormBase):
		def __init__(self, **kws):
			if kws.get('p') is None: kws['p'] = 1000
			super().__init__((EasyNorm._norm_sinh, EasyNorm._norm_asinh), **kws)

	class HistEqualNorm(NormBase):
		def __init__(self, **kws):
			super().__init__((None, None), **kws)

		def autoscale_None(self, A):
			if self.vmin is None or self.vmax is None or self._forward is None or self._backward is None:
				super().autoscale_None(A)
				###bin image
				hist, bins = np.histogram(A, 256, [self.vmin, self.vmax])
				bins = (bins[:-1] - self.vmin) / (self.vmax - self.vmin)
				cdf = hist.cumsum()
				cdf = (cdf - cdf.min()) / (cdf.max() - cdf.min())
				def fo(x, *args, **kws): return np.interp(x, bins, cdf)
				self._forward = fo
				def ba(x, *args, **kws): return np.interp(x, cdf, bins)
				self._backward = ba



class EasyWCSImage():
	###an image of NxM or 3xNxM
	def __init__(self, data=None, wcs=None, **kws):
		self._data = data
		self._wcs = wcs
		self.config(**kws)

	def __getitem__(self, index):
		config = {k:v[index] for k,v in self.config_kws.items()}
		if isinstance(index, slice):
			return EasyWCSImage(self._data[index], self._wcs, **config)
		else:
			return EasyWCSImage(self._data[index][np.newaxis], self._wcs, **config)


	def __repr__(self):
		line = 'EasyWCSImage:'
		if self.data is None: line += ' None data'
		else: line += ' %s data' % str(self.data.shape)
		if self.wcs is None: line += ' without wcs'
		else: line += ' with wcs'
		return line

	__str__ = __repr__

	@property
	def data(self): return self._data
	@property
	def wcs(self): return self._wcs
	@property
	def header(self):
		if self.wcs is None: return None
		else:
			header = self.wcs.to_header()
			header['NAXIS'] = self.wcs.pixel_n_dim
			if self.wcs.pixel_shape is not None:
				header['NAXIS1'] = self.wcs.pixel_shape[0]
				header['NAXIS2'] = self.wcs.pixel_shape[1]
				if self.wcs.naxis==3: header['NAXIS3'] = self.wcs.pixel_shape[2]
			return header
	@property
	def nx(self):
		if self.data is None:
			return 1 if self.wcs is None else self.wcs.pixel_shape[0]
		else: return self.data.shape[-1]
	@property
	def ny(self):
		if self.data is None:
			return 1 if self.wcs is None else self.wcs.pixel_shape[1]
		else: return self.data.shape[-2]
	@property
	def nc(self):
		if self.data is None: return 1
		else: return self.data.shape[-3]
	@property
	def is_scalar(self): return self.nc==1
	@property
	def is_vector(self): return self.nc>1
	@property
	def coordinates(self):
		xgrid, ygrid = np.meshgrid(np.arange(self.nx), np.arange(self.ny))
		if self.wcs is None: return xgrid.ravel(), ygrid.ravel(), None
		else:
			coord = SkyCoord.from_pixel(xgrid, ygrid, self.wcs.sub(2)).icrs.ravel()
			return coord.ra, coord.dec, 'icrs'

	def process_config_value(self, value):
		if isinstance(value, str) or (not np.iterable(value)): return [value]*self.nc
		if len(value)>self.nc: value = value[:self.nc]
		while len(value)<self.nc: value.append(None)
		return value

	def config(self, **kws):
		scale = self.process_config_value(kws.get('scale'))
		limit = self.process_config_value(kws.get('limit'))
		vmin = self.process_config_value(kws.get('vmin'))
		vmax = self.process_config_value(kws.get('vmax'))
		p = self.process_config_value(kws.get('p'))
		self.config_kws = dict(scale=scale, limit=limit, vmin=vmin, vmax=vmax, p=p)

	@property
	def image(self):
		if self.data is None:
			return np.zeros((self.ny, self.nx)), EasyNorm.get('linear')
		else:
			norm = [EasyNorm.get(clip=True, **{k:v[i] for k,v in self.config_kws.items()}) for i in range(min(self.nc, 4))]

			if self.nc == 1:
				###scalar image
				im = self.data[0]
				norm = norm[0]
			else:
				###vector image, scale to 0-1
				im = [norm[i](self.data[i]) for i in range(min(self.nc, 4))]

				if len(im) == 2:
					###add empty channel
					empty = np.full(im[0].shape, np.nan)
					im.append(empty)
					emptynorm = EasyNorm.get(scale='linear')
					emptynorm(empty)
					norm.append(emptynorm)
				if len(im) == 3:
					###add alpha channel
					alpha = np.isfinite(self.data).sum(axis=0)>0
					im.append(alpha)
				if len(im) == 4:
					norm = norm[:3]
				im = np.dstack(im)
			return im, norm

	@property
	def cube(self):
		if self.data is None:
			return np.zeros((1, self.ny, self.nx)), np.array([0])
		else:
			if self.wcs is None:
				vaxis = np.arange(self.nc)
			else:
				#print(self.wcs)
				#print(DataCube(self.data, self.wcs))
				vaxis = DataCube(data=self.data, wcs=self.wcs).velocity()
			return self.data, vaxis

	def load(obj, naxis=2):
		###load varisou type
		if obj is None:
			data, wcs = None, None
		elif isinstance(obj, WCS):
			data, wcs = None, obj.sub(naxis)
		elif isinstance(obj, fits.Header):
			data, wcs = None, WCS(obj, naxis=naxis)
		elif isinstance(obj, str):
			hdu = fits.open(obj)[0]
			data, wcs = hdu.data, WCS(hdu.header, naxis=naxis)
		elif isinstance(obj, fits.PrimaryHDU):
			data, wcs = obj.data, WCS(obj.header, naxis=naxis)
		elif isinstance(obj, LowerDimensionalObject):
			data, wcs = obj._data, WCS(obj.header, naxis=naxis)
		elif isinstance(obj, SpectralCube):
			data, wcs = obj._data, obj.wcs.sub(naxis)
		elif isinstance(obj, EasyWCSImage):
			return obj
		elif isinstance(obj, np.ndarray):
			if obj.ndim==3 and (obj.shape[2] in (1,3,4)): obj = obj.transpose(2,0,1)
			data, wcs = obj, None
		else: raise TypeError('unknown image type.')
		###regulate data

		if data is not None:
			while data.ndim>3: data = data[0]
			while data.ndim<3: data = data[np.newaxis]
		if wcs is not None:
			wcs.wcs.restfrq = 0

		#data[data==0] = np.nan
		return EasyWCSImage(data, wcs)


	def reproject(self, refheader, **kws):
		refimage = EasyWCSImage.load(refheader)

		if self.data is None:
			###empty data
			rpj_data = np.full((1, refimage.ny, refimage.nx), np.nan)
			rpj_image = EasyWCSImage(rpj_data, refimage.wcs, **self.config_kws)
		else:
			###data is not empty
			if (self.wcs is None) or (self.wcs.wcs.compare(refimage.wcs.wcs, cmp=1)):
				###empty wcs or the same as ref
				refimage.wcs.pixel_shape = (self.ny, self.nx)
				#rpj_data = np.full((self.nc, refimage.ny, refimage.nx), np.nan)
				#nx = min(self.data.shape[-1], rpj_data.shape[-1])
				#ny = min(self.data.shape[-2], rpj_data.shape[-2])
				#rpj_data[..., :ny, :nx] = self.data[..., :ny, :nx]
				rpj_image = EasyWCSImage(self.data, refimage.wcs, **self.config_kws)
			else:
				print(refimage)
				refheader = refimage.header
				oldheader = self.header
				if self.wcs.naxis==2:
					###fake the 3rd dimension
					refheader['NAXIS']  = oldheader['NAXIS'] = 3
					refheader['NAXIS3'] = oldheader['NAXIS3'] = self.nc
					refheader['CTYPE3'] = oldheader['CTYPE3'] = ''
					refheader['CRPIX3'] = oldheader['CRPIX3'] = 0
					refheader['CRVAL3'] = oldheader['CRVAL3'] = 0
					refheader['CDELT3'] = oldheader['CDELT3'] = 1
				else:
					###copy the 3rd dimension
					refheader['NAXIS']  = oldheader['NAXIS'] = 3
					refheader['NAXIS3'] = self.nc
					refheader['CTYPE3'] = oldheader['CTYPE3']
					refheader['CRPIX3'] = oldheader['CRPIX3']
					refheader['CRVAL3'] = oldheader['CRVAL3']
					refheader['CDELT3'] = oldheader['CDELT3']
					if 'CUNIT3' in oldheader: refheader['CUNIT3'] = oldheader['CUNIT3']
				rpj_data , _ = reproject_interp(fits.PrimaryHDU(self.data, oldheader), refheader, **kws)
				rpj_image = EasyWCSImage(rpj_data, WCS(refheader), **self.config_kws)
		return rpj_image



class EasyWCSImageList():
	###a List of image of NxM or 3xNxM
	def __init__(self, *images):
		self.imagelist = list(images)

	def __getitem__(self, index):
		if isinstance(index, slice):
			return EasyWCSImageList(*self.imagelist[index])
		else:
			return self.imagelist[index]

	def __repr__(self):
		line = 'EasyWCSImageList:\n'
		for im in self.imagelist:
			line += ' %s;\n' % im
		return line

	@property
	def data(self): return [im.data for im in self.imagelist]
	@property
	def wcs(self): return [im.wcs for im in self.imagelist]
	@property
	def header(self): return [im.header for im in self.imagelist]
	@property
	def nx(self): return [im.nx for im in self.imagelist]
	@property
	def ny(self): return [im.ny for im in self.imagelist]
	@property
	def nc(self): return sum([im.nc for im in self.imagelist])

	def finest_header(self):
		header = None
		pix_area = np.inf
		for im in self.imagelist:
			if (im.wcs is not None) and (im.data is not None):
				if np.abs(np.prod(im.wcs.cdelt)) < pix_area:
					header = im.wcs
					pix_area = np.abs(np.prod(im.wcs.cdelt))
		return header

	def merge(self):
		###try to merge data if wcs(es) are the same or there is only one wcs
		###return None if fail to merge
		###merge wcs
		wcslist = []
		for im in self.imagelist:
			if (im.wcs is not None) and (im.data is not None): wcslist.append(im.wcs)
		if len(wcslist)==0: merge_wcs = None
		elif len(wcslist)==1: merge_wcs = wcslist[0]
		else:
			if all([wcslist[0].wcs.compare(w.wcs, cmp=1) for w in wcslist[1:]]):
				merge_wcs = wcslist[0]
				merge_wcs.pixel_shape = (max(self.nx), max(self.ny))
			else: return None	###unable to merge
		###merge data
		if all([d is None for d in self.data]): merge_data = None
		else:
			merge_data = []
			for im in self.imagelist:
				if im.data is None: data = np.full((1, max(self.ny), max(self.nx)), np.nan)
				else:
					data =  np.full((im.nc, max(self.ny), max(self.nx)), np.nan)
					data[:, :im.ny, :im.nx] = im.data[:, :im.ny, :im.nx]
				merge_data.append(data)
			merge_data = np.vstack(merge_data)
		return EasyWCSImage(merge_data, merge_wcs)

	def load(*obj):
		if len(obj) == 1:
			return EasyWCSImage.load(obj[0])
		else:
			imagelist = EasyWCSImageList(*[EasyWCSImage.load(o) for o in obj])
			merge_image = imagelist.merge()
			if merge_image is None: return imagelist
			else: return merge_image

	def reproject(self, refheader, **kws):
		rpj_data = []
		for im in self.imagelist:
			rpj_im = im.reproject(refheader, **kws)
			rpj_data.append(rpj_im.data)
		return EasyWCSImage(np.vstack(rpj_data), rpj_im.wcs)



class EasyFigure(mpl.figure.Figure):
	def add_axes(self, arg, **kws):
		if isinstance(arg, (mpl.axes.Axes, WCSAxes)):
			return super().add_axes(arg)
		else:
			ax = EasyWCSAxes(self, arg, **kws)
			return super().add_axes(ax)


	def add_subplot(self, *args, **kws):
		if isinstance(args[0], (mpl.axes.Subplot, WCSAxesSubplot)):
			return super().add_subplot(args[0])
		else:
			sp = EasyWCSAxesSubplot(self, *args, **kws)
			return super().add_subplot(sp)


	#def subplots_adjust(self, **kws):
	#	super().subplots_adjust(**kws)

	#def autoscale(self):
	#	self.get_figwidth()
	#	self.get_figheight()



class EasyWCSAxes(WCSAxes):
	def __init__(self, fig, rect, **kws):
		self.figure = fig
		kws = self._init_wcs(**kws)
		super().__init__(self.figure, rect, **kws)
		self._post_setting()

	def _init_wcs(self, **kws):
		###get wcs
		wcs = kws.pop('projection', None)
		if wcs is None: wcs = kws.get('wcs', None)

		###replace kws
		if wcs is None:
			self.fimage = None
		else:
			self.fimage = EasyWCSImage.load(wcs)
			kws['wcs'] = self.fimage.wcs.sub(2)
		return kws

	@property
	def header(self):
		if self.fimage is None: return None
		else:return self.fimage.header

	def _post_setting(self):
		try: 
			self.set_aspect(np.abs(self.wcs.wcs.cd[0,0] / self.wcs.wcs.cd[1,1]))
		except:
			self.set_aspect(np.abs(self.wcs.wcs.cdelt[0] / self.wcs.wcs.cdelt[1]))
		if 'GLON' in self.wcs.wcs.ctype[0]:
			self.coords[0].set_axislabel('Galactic Longitude')
			self.coords[0].set_major_formatter('d.dd')
		elif 'RA' in self.wcs.wcs.ctype[0]:
			self.coords[0].set_axislabel('Right Ascension')
		if 'GLAT' in self.wcs.wcs.ctype[1]:
			self.coords[1].set_axislabel('Galactic Latitude')
			self.coords[1].set_major_formatter('d.dd')
		elif 'DEC' in self.wcs.wcs.ctype[1]:
			self.coords[1].set_axislabel('Declination')
		self.coords[0].tick_params(top=True, bottom=True, labeltop=False, labelbottom=True, direction='in')
		self.coords[1].tick_params(left=True, right=True, labelleft=True, labelright=False, direction='in')
		

	def imshow(self, *image_obj, reproject=True, scale=None, limit=None, vmin=None, vmax=None, p=None, **kws):
		'''
		image_obj : str, (str, str, ...), HDU, (HDU, HDU, ...) or None
		FITS filename(s) / HDU(s) / WCS(s)
		e.g.
			'a.fits'
			'red.fits', 'green.fits', 'blue.fits', 'alpha.fits'
		    hdu_red, hdu_green, hdu_blue
			hdu_r, None, hdu_b

		reproject : bool
		transform or reproject to the wcs of axes

		scale : None, str, or [str, str, ...]
		same length as image_obj.
		should be 'lin', 'log', 'pow', 'sqrt', 'sq', 'asinh', 'sinh', or 'histeq'.
		default is 'lin'.

		vmin, vmax : None, float, or [float, float, ...]
		lower and upper limit.

		limit : None, float, or [float, float, ...]
		percentile cut of image value (95%, 99%, ...).
		ignore if vmin and vmax is not None.
		'''
		###load image
		ewimage = EasyWCSImageList.load(*image_obj)

		###convert list to image with either transform or reproject
		if (not reproject) and isinstance(ewimage, EasyWCSImage):
			kws['transform'] = self.get_transform(ewimage.wcs)
		else:
			ewimage = ewimage.reproject(self.wcs)

		###config image
		ewimage.config(scale=scale, limit=limit, vmin=vmin, vmax=vmax, p=p)

		###get image and norm
		im, norm = ewimage.image

		###add keywords
		if ewimage.is_scalar:
			if kws.get('norm') is None:
				kws['norm'] = norm
		else:
			kws['cmap'] = None
			kws['vmin'] = 0
			kws['vmax'] = 1
		
		artist = super().imshow(im, **kws)
		if ewimage.is_vector: artist.norms = norm
		return artist



	def colorbar(self, mappable, hspace=0.03, **kws):
		###default
		default_kws = dict(width='4%', height='100%', borderpad=0, loc="lower right", axes_kwargs={'facecolor':'none'}, \
				bbox_transform=self.transAxes, bbox_to_anchor=(0.06, 0, 1, 1))
		default_kws.update(kws)

		if 'norms' not in mappable.__dict__:
			###scalar colorbar
			self._colorbar_axes = inset_axes(self, **default_kws)
			self.figure.colorbar(mappable, cax=self._colorbar_axes)
		else:
			###vector colorbar
			###get mappable, and remove empty ones
			mappablelist = []
			for i in range(3):
				if np.isfinite(mappable.norms[i].vmin) & np.isfinite(mappable.norms[i].vmax):
					cmap = mpl.colors.ListedColormap(np.linspace(0,1,256)[:,np.newaxis]*np.array([i==0,i==1,i==2]))
					norm = mappable.norms[i]
					mappablelist.append(mpl.cm.ScalarMappable(cmap=cmap, norm=norm))

			###adjust bbox
			bbox = default_kws['bbox_to_anchor']
			nm = len(mappablelist)
			height = (bbox[3] - bbox[1]) * (1 - hspace*(nm-1)) / nm
			hspace = (bbox[3] - bbox[1]) * hspace
			bbox = [(bbox[0], bbox[1]+i*(height+hspace), bbox[2], height) for i in range(nm)]

			###colorbar
			self._colorbar_axes = []
			for i,mappable in enumerate(mappablelist):
				subaxes_kws = default_kws.copy()
				subaxes_kws['bbox_to_anchor'] = bbox[i]
				self._colorbar_axes.append(inset_axes(self, **subaxes_kws))
				self.figure.colorbar(mappable, cax=self._colorbar_axes[-1])



	def contour(self, image_obj, reproject=True, **kws):
		ewimage = EasyWCSImage.load(image_obj)

		###convert list to image with either transform or reproject
		if not reproject:
			kws['transform'] = self.get_transform(ewimage.wcs)
		else:
			ewimage = ewimage.reproject(self.wcs)

		###get image and norm
		im, norm = ewimage[0].image

		artist = super().contour(im, **kws)		
		return artist



	def _process_frame(self, frame):
		if frame is None:
			### default frame is pixel
			return self.transData
		elif frame.lower() == 'pixel'[:len(frame)]:
			return self.transData
		elif frame.lower() == 'normalized'[:len(frame)]:
			### normalize 0-1
			return self.transAxes
		else:
			### wcs
			try:
				return self.get_transform(frame)
			except:
				raise ValueError("unknown frame, use 'pixel', 'normal', 'icrs', 'fk5', 'galactic', etc.")



	def _process_value(self, value):
		### process value with unit
		if value is None: return None
		else: return value
		'''
		if isinstance(value, u.Quantity):
			if frame in 'pixel normalized':
				if value.unit==u.Unit(): return value.value
				else: raise ValueError("%s should be number without unit in frame 'pixel' or 'normal'" % name)
			else:

				return value
		else:
			if frame in 'pixel normalized': return value
			else: return value*u.deg
		'''


	def _process_image(self, arg, mode='coord'):
		### process image
		try:
			### deal as EasyWCSImage
			image = EasyWCSImage.load(arg)
			if mode == 'coord':
				return image.coordinates
			elif mode == 'data':
				return image.data.ravel()
			elif mode == 'all':
				x, y, frame = image.coordinates
				return x, y, image.data.ravel(), frame
		except:
			return arg




	def plot(self, *args, frame='pixel', **kws):
		if frame is not None: kws['transform'] = self.get_transform(frame)
		artist = super().plot(*args, **kws)
		return artist



	def scatter(self, *args, s=None, c=None, frame='pixel', **kws):
		'''
		x,y: array, image
		unit: str or astropy.units.Unit
			unit for x, y
		'''
		if len(args)==0:
			raise TypeError("scatter() missing required positional argument: 'x, y' or 'image'.")
		elif len(args)==1:
			### load coordinates from image
			try:
				x, y, frame = self._process_image(args[0], mode='coord')
				kws['transform'] = self._process_frame(frame)
			except: raise TypeError("scatter() missing required positional argument: 'x, y' or 'image'.")
		elif len(args)==2:
			### generally load x, y
			kws['transform'] = self._process_frame(frame)
			x = self._process_value(args[0])
			y = self._process_value(args[1])
		else:
			raise TypeError("scatter() missing required positional argument: 'x, y' or 'image'.")

		try: s = self._process_image(s, mode='data')
		except: s = _process_value(s)
		try: c = self._process_image(c, mode='data')
		except: c = _process_value(c)

		artist = super().scatter(x, y, s=s, c=c, **kws)
		return artist



	def text(self, *args, s=None, c=None, frame='pixel', fmt='%.1f', **kws):
		if len(args)==0:
			raise TypeError("text() missing required positional argument: 'x, y, t' or 'image'.")
		elif len(args)==1:
			### load coordinates and text from image
			try:
				x, y, t, frame = self._process_image(args[0], mode='all')
				kws['transform'] = self._process_frame(frame)
			except: raise TypeError("text() missing required positional argument: 'x, y, t' or 'image'.")
		elif len(args)==2:
			try:
				x, y, frame = self._process_image(arg[0], mode='coord')
				t = arg[1]
				kws['transform'] = self._process_frame(frame)				
			except: raise TypeError("text() missing required positional argument: 't'")
		elif len(args)==3:
			### generally load x, y
			kws['transform'] = self._process_frame(frame)
			x = self._process_value(args[0])
			y = self._process_value(args[1])
			t = args[2]
		else:
			raise TypeError("scatter() missing required positional argument: 'x, y' or 'image'.")

		if not np.iterable(x):
			artist = super().text(x, y, t, **kws)
		else:
			try: s = self._process_image(s, mode='data')
			except: s = _process_value(s)
			try: c = self._process_image(c, mode='data')
			except: c = _process_value(c)

			ha = kws.pop('ha', 0.5)
			va = kws.pop('va', 0.5)

			paths = []
			for i in range(len(x)):
				if not isinstance(t[i], str):
					if np.isnan(t[i]): continue
					else: ti = np.char.mod(fmt, t[i])
				else: ti = t[i]
				marker_obj = MarkerStyle('$%s$' % ti)
				path = marker_obj.get_path()#.transformed(marker_obj.get_transform())
				vertices = path.vertices - (path.vertices.min(axis=0)*(1-ha, 1-va) + path.vertices.max(axis=0)*(ha, va))
				path = Path(vertices, path.codes)
				paths.append(path)
			artist = super().scatter(x, y, s=s, c=c, **kws)
			artist.set_paths(paths)

		return artist



	def vector(self, *args, s=None, c=None, unit='deg', frame=None, **kws):
		if len(args)==0:
			raise TypeError("vector() missing required positional argument: 'x, y, pa' or 'image'")
		elif len(args)==1:
			### load coordinates and pa from image
			try:
				x, y, pa, frame = self._process_image(args[0], mode='all')
				pa *= u.Unit(unit)
				kws['transform'] = self._process_frame(frame)
			except: raise TypeError("vector() missing required positional argument: 'x, y, pa' or 'image'.")
		elif len(args)==2:
			try:
				x, y, frame = self._process_image(args[0], mode='coord')
				pa = self._process_image(args[0], mode='data') * u.Unit(unit)
				kws['transform'] = self._process_frame(frame)				
			except: raise TypeError("vector() missing required positional argument: 'pa'")
		elif len(args)==3:
			### generally load x, y
			kws['transform'] = self._process_frame(frame)
			x = self._process_value(args[0])
			y = self._process_value(args[1])
			pa = self._process_value(args[2])*u.Unit(unit)
		else:
			raise TypeError("scatter() missing required positional argument: 'x, y' or 'image'.")

		try: s = self._process_image(s, mode='data')
		except: s = _process_value(s)
		try: c = self._process_image(c, mode='data')
		except: c = _process_value(c)

		paths = []
		if not np.iterable(pa): pa = np.repeat(pa, len(x))
		for pai in pa:
			if np.isnan(pai): continue
			vertices = ((-np.sin(pai)/2, np.cos(pai)/2), (np.sin(pai)/2, -np.cos(pai)/2), (np.sin(pai)/2, -np.cos(pai)/2))
			codes = [Path.MOVETO, Path.LINETO, Path.STOP]
			paths.append(Path(vertices, codes, closed=False))

		artist = super().scatter(x, y, s=s, c=c, **kws)
		artist.set_paths(paths)
		return artist



	def quiver(self, *args, frame='pixel', **kws):
		kws['transform'] = self._process_frame(frame)
		super().quiver(*args, **kws)



	def rectangle(self, x, y, width, height, pa=0, unit='deg', frame=None, **kws):
		###modified from astropy.visualization.wcsaxes.patches.SphericalCircle
		if frame is not None: kws['transform'] = self.get_transform(frame)
		x = self._process_value(x, unit)
		y = self._process_value(y, unit)
		width = self._process_value(width, unit)
		height = self._process_value(height, unit)
		pa = self._process_value(pa, unit).to(u.radian)

		theta = np.arctan(height/width).to_value(u.radian)
		lon = [theta, np.pi-theta, np.pi+theta, -theta] * u.radian + np.pi/2*u.radian - pa
		lat = np.repeat(90 * u.deg - np.sqrt(width**2 + height**2)/2, 4).to(u.radian)
		lon, lat = _rotate_polygon(lon, lat, x, y)
		lon = lon.to_value('deg')
		lat = lat.to_value('deg')
		vertices = np.array([lon, lat]).transpose()

		p = Polygon(vertices, **kws)
		artist = self.add_patch(p)
		return artist


	def quadrangle(self, x, y, width, height, unit='deg', center=True, frame=None, **kws):
		from astropy.visualization.wcsaxes import Quadrangle
		if frame is not None: kws['transform'] = self.get_transform(frame)
		x = self._process_value(x, unit)
		y = self._process_value(y, unit)
		width = self._process_value(width, unit) / np.cos(y)
		height = self._process_value(height, unit)

		if center:
			x -= width/2
			y -= height/2
		p = Quadrangle((x, y), width, height, **kws)
		artist = self.add_patch(p)
		return artist


	def ellipse(self, x, y, a, b, pa=0, unit='deg', frame=None, resolution=100, **kws):
		###modified from astropy.visualization.wcsaxes.patches.SphericalCircle
		if b > a: a, b = b, a
		if frame is not None: kws['transform'] = self.get_transform(frame)
		x = self._process_value(x, unit)
		y = self._process_value(y, unit)
		ha = self._process_value(a, unit)
		hb = self._process_value(b, unit)
		pa = self._process_value(pa, unit).to(u.radian)

		lon = np.linspace(0.0, 2*np.pi, resolution+1)[:-1] * u.radian
		lat = (90 * u.deg - (ha * hb / np.sqrt(hb**2 * np.cos(lon+pa)**2 + ha**2 * np.sin(lon+pa)**2))).to('rad')
		lon, lat = _rotate_polygon(lon, lat, x, y)
		lon = lon.to_value('deg')
		lat = lat.to_value('deg')
		vertices = np.array([lon, lat]).transpose()

		p = Polygon(vertices, **kws)
		artist = self.add_patch(p)
		return artist


	def circle(self, x, y, diameter, unit='deg', frame=None, **kws):
		p = self.ellipse(x, y, diameter, diameter, pa=0, unit=unit, frame=frame, **kws)
		artist = self.add_patch(p)
		return artist


	def arc(self, x, y, a, b, pa=0, theta1=0.0, theta2=360.0, unit='deg', frame=None, resolution=100, **kws):
		###modified from astropy.visualization.wcsaxes.patches.SphericalCircle
		if b > a: a, b = b, a
		if frame is not None: kws['transform'] = self.get_transform(frame)
		kws['facecolor'] = 'none'
		x = self._process_value(x, unit)
		y = self._process_value(y, unit)
		ha = self._process_value(a, unit)
		hb = self._process_value(b, unit)
		pa = self._process_value(pa, unit).to(u.radian)

		lon = np.pi*u.radian - (np.linspace(theta1, theta2, resolution+1) * u.Unit(unit)).to(u.radian)
		lat = (90 * u.deg - (ha * hb / np.sqrt(hb**2 * np.cos(lon+pa)**2 + ha**2 * np.sin(lon+pa)**2))).to('rad')
		lon, lat = _rotate_polygon(lon, lat, x, y)
		lon = lon.to_value('deg')
		lat = lat.to_value('deg')
		vertices = np.array([lon, lat]).transpose()

		codes = np.full(len(vertices), Path.LINETO)
		codes[0] = Path.MOVETO
		codes[-1] = Path.STOP
		p = Path(vertices, codes)
		p = PathPatch(p, **kws)
		artist = self.add_patch(p)
		return artist


	def arrow(self, endx, endy, headx, heady, unit='deg', frame=None, **kws):
		if frame is not None: kws['transform'] = self.get_transform(frame)
		endx = self._process_value(endx, unit).to('deg')
		endy = self._process_value(endy, unit).to('deg')
		headx = self._process_value(headx, unit).to('deg')
		heady = self._process_value(heady, unit).to('deg')

		artist = super().arrow(endx, endy, headx-endx, heady-endy, **kws)
		return artist


	def beam(self, major, minor, pa=0, unit='deg', corner='bottom left', angle=None, borderpad=0.4, pad=0.5, frame=False, **kws):
		'''
		not implemented yet
		'''
	
		
		from astropy.wcs.utils import proj_plane_pixel_scales
		from mpl_toolkits.axes_grid1.anchored_artists import AnchoredEllipse, AnchoredSizeBar

		major = self._process_value(major, unit).to_value('deg')
		minor = self._process_value(minor, unit).to_value('deg')


		if self.wcs.is_celestial:
			pix_scale = proj_plane_pixel_scales(self.wcs)
			sx = pix_scale[0]
			sy = pix_scale[1]
			degrees_per_pixel = np.sqrt(sx * sy)
		else:
			raise ValueError("Cannot show beam when WCS is not celestial")

		minor /= degrees_per_pixel
		major /= degrees_per_pixel

		CORNERS = {
			"top right": 1,
			"top left": 2,
			"bottom left": 3,
			"bottom right": 4,
			"right": 5,
			"left": 6,
			"bottom": 8,
			"top": 9,
		}
		corner = CORNERS[corner]

		beam = AnchoredEllipse(
			self.transData,
			width=minor,
			height=major,
			angle=angle,
			loc=corner,
			pad=pad,
			borderpad=borderpad,
			frameon=frame,
		)
		beam.ellipse.set(**kws)

		self.add_artist(beam)
		


	def scalebar(self, distance=1):
		'''
		not implemented yet
		'''
		pass



	def gridspectra(self, cube_obj, reproject=False, grid_scale=1, xlim=None, ylim=None, clip=True, **kws):
		'''
		Plot spectra in grid

		cube_obj: str, or HDU
			datacube to plot spectra in grid
		reproject: bool
			whether to reproject the datacube to the wcs of axes
		grid_scale: float
			scale of grid size
		xlim: 2-elements tuple
			x limit of grid
		ylim: 2-elements tuple
			y limit of grid
		clip: bool
			whether to remove grid out of the axes
		**kws:
			other kws passed to plt.step

		return list of [grid_axes, step_artist]
		'''
		###load image
		ewcube = EasyWCSImage.load(cube_obj, naxis=3)

		###convert list to image with either transform or reproject
		if not reproject:
			cubex, cubey = np.meshgrid(np.arange(ewcube.nx), np.arange(ewcube.ny))
			cubecoo = SkyCoord.from_pixel(cubex, cubey, ewcube.wcs.sub(2))
			bgx, bgy = cubecoo.to_pixel(self.wcs)
		else:
			ewcube = ewcube.reproject(self.wcs)
			cubex, cubey = np.meshgrid(np.arange(ewcube.nx), np.arange(ewcube.ny))
			bgx, bgy = cubex, cubey
		if clip:
			mask = (bgx >= -1e-5) & (bgx <= self.fimage.nx-1+1e-5) & (bgy >= -1e-5) & (bgy <= self.fimage.ny-1+1e-5)
		else:
			mask = np.ones_like(bgx, dtype=bool)

		###get image and vaxis
		cube, vaxis = ewcube.cube
		if ylim is None:
			ylim = (np.nanmin(cube), np.nanmax(cube))
			ylim += np.diff(ylim)*0.1*[-1,1]

		###determine grid size
		sx = np.min(np.abs(np.diff(bgx, axis=-1)))
		sy = np.min(np.abs(np.diff(bgy, axis=-2)))
		sz = min(sx, sy) * grid_scale

		artist = []
		for iy, ix in tqdm(np.argwhere(mask)):
			###add axes, plot spectrum, skip if all nan spectrum
			if np.isfinite(cube[:, iy, ix]).any():
				ba = (bgx[iy, ix]-sz/2, bgy[iy, ix]-sz/2, sz, sz)
				axi = inset_axes(self, width='100%', height='100%', bbox_transform=self.transData, \
					bbox_to_anchor=ba,\
					loc = 3, borderpad=0, axes_kwargs={'facecolor':'none'})
				arti = axi.step(vaxis, cube[:, iy, ix], **kws)
				axi.set_xlim(xlim)
				axi.set_ylim(ylim)
				axi.tick_params(axis='x', top=True, bottom=True, labeltop=False, labelbottom=False, direction='in')
				axi.tick_params(axis='y', left=True, right=True, labelleft=False, labelright=False, direction='in')
				artist.append([axi, arti])

		return artist
	


	def set_world_xlim(self, left=None, right=None, **kws):
		if right is None and np.iterable(left):
			left, right = left[:2]
		if self.wcs.is_celestial:
			_, cen = self.wcs.wcs_pix2world(self.wcs.pixel_shape[0]/2, self.wcs.pixel_shape[1]/2, 0)
			if left is not None:
				left_pix, _ = self.wcs.wcs_world2pix(left, cen, 0)
				kws['left'] = left_pix
			if right is not None:
				right_pix, _ = self.wcs.wcs_world2pix(right, cen, 0)
				kws['right'] = right_pix
		super().set_xlim(**kws)



	def set_world_ylim(self, bottom=None, top=None, **kws):
		if top is None and np.iterable(bottom):
			bottom, top = bottom[:2]
		if self.wcs.is_celestial:
			cen, _ = self.wcs.wcs_pix2world(self.wcs.pixel_shape[0]/2, self.wcs.pixel_shape[1]/2, 0)
			if bottom is not None:
				_, bottom_pix = self.wcs.wcs_world2pix(cen, bottom, 0)
				kws['bottom'] = bottom_pix
			if top is not None:
				_, top_pix = self.wcs.wcs_world2pix(cen, top, 0)
				kws['top'] = top_pix
		super().set_ylim(**kws)



	def set_world_box(self, x, y, w, h):
		### set limit centered at `x,y` with width `w` and height `h` in degree
		if self.wcs.is_celestial:
			x_pix, y_pix = self.wcs.wcs_world2pix(x, y, 0)
			try:
				w_pix = w/np.abs(self.wcs.wcs.cd[0,0])
				h_pix = h/np.abs(self.wcs.wcs.cd[1,1])
			except:
				w_pix = w/np.abs(self.wcs.wcs.cdelt[0])
				h_pix = h/np.abs(self.wcs.wcs.cdelt[1])
			super().set_xlim(x_pix-w_pix/2, x_pix+w_pix/2)
			super().set_ylim(y_pix-h_pix/2, y_pix+h_pix/2)




class EasyWCSAxesSubplot(WCSAxesSubplot, EasyWCSAxes):
	def __init__(self, fig, *args, **kws):
		self.figure = fig
		kws = self._init_wcs(**kws)
		super().__init__(self.figure, *args, **kws)
		self._post_setting()



class EasyWCSAxesChannelMaps(EasyWCSAxes):
	def __init__(self, fig, nrows=None, ncols=None, **kws):
		self.figure = fig
		kws = self._init_wcs(**kws)
		self.nrows = nrows
		self.ncols = ncols
		self.subplot_kw = kws
		self.channelmap_subplots = []	#axes only for channelmap, in case other type of axes is added to figure



	def get_channelmap_subplot(self, i):
		### return the i-th subplot, if i>current subplots, add new one.
		if i >= self.nrows*self.ncols:
			raise ValueError('Too many channels')
		if len(self.channelmap_subplots)>0:
			self.subplot_kw['sharex'] = self.channelmap_subplots[0]
			self.subplot_kw['sharey'] = self.channelmap_subplots[0]
		### create new subplot
		while i >= len(self.channelmap_subplots):
			sp = EasyWCSAxesSubplot(self.figure, self.nrows, self.ncols, len(self.channelmap_subplots)+1, **self.subplot_kw)
			self.figure.add_subplot(sp)
			self.channelmap_subplots.append(sp)
			is_bottom = i//self.ncols==self.nrows-1
			is_left = i%self.ncols==0
			sp.coords[0].tick_params(labelbottom=is_bottom)
			sp.coords[1].tick_params(labelleft=is_left)
			if ~(is_bottom & is_left):
				sp.coords[0].set_axislabel(' ')
				sp.coords[1].set_axislabel(' ')
		return self.channelmap_subplots[i]


	def auto_rowcol(self, nc):
		### decide nrows and ncols automatically
		if self.ncols is None:
			if self.nrows is None:
				self.ncols = np.ceil(np.sqrt(nc)).astype(int)
				self.nrows = np.ceil(nc / self.ncols).astype(int)
			else:
				self.ncols = np.ceil(nc / self.nrows).astype(int)
		else:
			if self.nrows is None:
				self.nrows = np.ceil(nc / self.ncols).astype(int)
			else:
				if nc > self.nrows*self.ncols:
					print("Channels beyond nrows x ncols are ignored.")



	def auto_adjust(self):
		### adjust subplots to leave no space between them 
		wcs = self.channelmap_subplots[0].wcs
		xlim = self.channelmap_subplots[0].get_xlim()
		try: mapwidth = (xlim[1]-xlim[0]) * np.abs(wcs.wcs.cd[0,0]) * self.ncols
		except: mapwidth = (xlim[1]-xlim[0]) * np.abs(wcs.wcs.cdelt[0]) * self.ncols
		ylim = self.channelmap_subplots[0].get_ylim()
		try: mapheight = (ylim[1]-ylim[0]) * np.abs(wcs.wcs.cd[1,1]) * self.nrows
		except: mapheight = (ylim[1]-ylim[0]) * np.abs(wcs.wcs.cdelt[1]) * self.nrows
		figwidth = self.figure.get_figwidth()
		figheight = self.figure.get_figheight()
		if mapheight/mapwidth > figheight/figwidth:
			bottom=0.15
			top=0.95
			left = 0.15
			right = figheight*(top-bottom) / mapheight * mapwidth / figwidth + left
		else:
			left = 0.15
			right = 0.95
			bottom = 0.15
			top = figwidth*(right-left) / mapwidth * mapheight / figheight + bottom
		self.figure.subplots_adjust(bottom=bottom, top=top, left=left, right=right, wspace=0, hspace=0)



	def imshow(self, cube_obj, index=None, **kws):
		### show channels of a datacube along the subplots as imshow
		ewcube = EasyWCSImage.load(cube_obj)
		if index is None: index = np.arange(ewcube.nc)
		self.auto_rowcol(len(index))
		index = index[:self.nrows*self.ncols]

		for i,idx in enumerate(index):
			sp = self.get_channelmap_subplot(i)
			m = sp.imshow(ewcube[idx], **kws)
		self.auto_adjust()
		return m



	def contour(self, cube_obj, index=None, **kws):
		### show channels of a datacube along the subplots as contour
		ewcube = EasyWCSImage.load(cube_obj)
		if index is None: index = np.arange(ewcube.nc)
		self.auto_rowcol(len(index))
		index = index[:self.nrows*self.ncols]

		for i,idx in enumerate(index):
			sp = self.get_channelmap_subplot(i)
			m = sp.contour(ewcube[idx], **kws)
		self.auto_adjust()
		return m



	def colorbar(self, mappable, **kws):
		self.channelmap_subplots[-1].colorbar(mappable, **kws)


	def text(self, x, y, texts, **kws):
		for i,t in enumerate(texts[:len(self.channelmap_subplots)]):
			self.channelmap_subplots[i].text(x, y, t, **kws)




def figure(*args, **kws):
	return plt.figure(*args, FigureClass=EasyFigure, **kws)



def axes(*args, **kws):
	### don't know why figure keyword is not allowed for .axes, so deal separately
	fig = kws.pop('figure', None)
	if fig is None: fig = figure()

	if len(args)==0:
		return fig.add_subplot(1, 1, 1, **kws)
	else:
		return fig.add_axes(*args, **kws)



def subplot(*args, **kws):
	### don't know why figure keyword is not allowed for .subplot, so deal separately
	fig = kws.pop('figure', None)
	if fig is None: fig = figure()
	
	if len(args)==0:
		return fig.add_subplot(1, 1, 1, **kws)
	else:
		return fig.add_subplot(*args, **kws)



def subplots(*args, **kws):
	wcs = kws.pop('projection', None)
	if wcs is None: wcs = kws.pop('wcs', None)
	kws['FigureClass'] = EasyFigure
	return plt.subplots(*args, subplot_kw = dict(wcs=wcs), **kws)



def imshow(*image_obj, **kws):
	ax = subplot(wcs=image_obj[0])
	return ax.imshow(*image_obj, **kws)



def contour(image_obj, **kws):
	ax = subplot(wcs=image_obj)
	return ax.contour(image_obj, **kws)



def show():
	plt.show()



def channelmap(nrows=None, ncols=None, projection=None, **kws):
	fig = kws.pop('figure', None)
	if fig is None: fig = figure(**kws)
	return EasyWCSAxesChannelMaps(fig, nrows=nrows, ncols=ncols, projection=projection)


if __name__ == '__main__':
	if 0:
		###prepare
		co = '/Users/shaobo/Work/mwisp/L935/mosaic_U_clipv.fits'
		co13 = '/Users/shaobo/Work/mwisp/L935/mosaic_L_clipv.fits'
		cube = DataCube.openMWISP(co)
		new = cube[50:150, 115:129, 125:143]
		new.write('/Users/shaobo/Work/script/mwisp_package_test/example/test_plot_cube.fits', overwrite=True)
		new.moment(axis=0).write('/Users/shaobo/Work/script/mwisp_package_test/example/test_plot_img.fits', overwrite=True)
		cube = DataCube.openMWISP(co13)
		new = cube[50:150, 115:129, 125:143]
		new.write('/Users/shaobo/Work/script/mwisp_package_test/example/test_plot_cube_L.fits', overwrite=True)
	
	bg = '/Users/shaobo/Work/script/mwisp_package_test/example/mips_1.fits'
	fg = '/Users/shaobo/Work/script/mwisp_package_test/test_m0.fits'
	r = '/Users/shaobo/Work/script/mwisp_package_test/example/rgb_L2.fits'
	g = '/Users/shaobo/Work/script/mwisp_package_test/example/rgb_L.fits'
	b = '/Users/shaobo/Work/script/mwisp_package_test/example/rgb_U.fits'

	gridbg = '/Users/shaobo/Work/script/mwisp_package_test/example/gridmap_m0_U.fits'
	gridfg1 = '/Users/shaobo/Work/script/mwisp_package_test/example/gridmap_cube_U.fits'
	gridfg2 = '/Users/shaobo/Work/script/mwisp_package_test/example/gridmap_cube_L.fits'

	from astropy.visualization.wcsaxes import add_beam

	#fig=figure(figsize=(12,10))

	###axes, subplot, imshow, colorbar
	if 0:
		fig = figure(figsize=(12,10))
		#s1 = EasyWCSAxes([.1,.1,.7,.7], figure=fig, projection=fg)
		s1 = fig.add_subplot(121, projection=fg)
		print(s1.wcs.is_celestial)
		#rgb = EasyWCSImageList.load(r, g, b)
		m = s1.imshow(r,g,b, scale=['lin','lin','lin','lin'], limit=[None, 99, 95], vmin=[1,], vmax=[None,None,None,80])
		#s1.contour(b, levels=np.arange(5,80,15), colors='w', transform=False)
		#from astropy.visualization import LogStretch
		#m = s1.imshow(b, norm = LogStretch())
		s1.colorbar(m, hspace=0.02)

		s2 = subplot(122, figure=fig, projection=fg)
		#m = s2.imshow(r, None, g, b, scale=['lin','lin','lin','lin'], limit=[None, 99, 95], vmin=[1,], vmax=[None,None,None,80])
		#s2.contour(b, levels=np.arange(5,80,15), colors='k', transform=False, alpha=0.3)
		cfalut = mpl.colors.ListedColormap(fits.open('/Users/shaobo/Work/script/mylib/userct/cfa.fits')[0].data)
		m = s2.imshow(b, scale='histeq', vmin=0, vmax=120, cmap=cfalut)
		s2.colorbar(m, hspace=0.02)

	### subplots
	if 0:
		#r = EasyWCSImage.load(r)
		fig, ax = subplots(ncols=3, wcs=r, sharex=True, sharey=True)
		print(ax)
		ax[0].imshow(r, scale='lin')
		ax[1].imshow(g, scale='log')
		ax[2].imshow(g, scale='sqrt')

	### norm
	if 0:
		fig = figure()
		b = fits.open(b)[0].data

		s1 = fig.add_subplot(121)
		s2 = fig.add_subplot(122)
		print('imshow')
		m = s1.imshow(b, norm=EasyNorm.get('log', vmin=0, vmax=100, p=9), cmap='gist_rainbow_r', origin='lower')

		print('func')
		x = np.linspace(0,m.norm.vmax,11)
		s2.plot(x, m.norm(x), '.')

		#s1 = EasyWCSAxesSubplot(121, figure=fig, projection=fg)
		#cfalut = mpl.colors.ListedColormap(fits.open('/Users/shaobo/Work/script/mylib/userct/cfa.fits')[0].data)
		#m = s1.imshow(b, scale='histeq', cmap=cfalut)
		print('colorbar')
		fig.colorbar(m, ax=s1)

		#im = n(b)
		#x = np.linspace(0,1,11)
		#print(m.norm.inverse(x))

	###gridmap, gridtext
	if 0:
		im = EasyWCSImage.load(gridbg)
		im._data = im.data / np.nanmax(im.data) * 180
		s1 = subplot(111, projection=im)
		s1.imshow(im, cmap='Greys')
		s1.scatter(0.5, 0.5, s=500, frame='norm')
		s1.scatter(3, 3, s=500, frame='pixel')
		s1.scatter(85.35, -1.45, s=500, frame='galactic')
		s1.scatter(im, s=15, c=gridbg, cmap='RdBu')
		s1.text(0.5, 0.5, 'Norm', frame='norm', color='red', ha='center')
		s1.text(3, 3, 'Pix', frame='pixel', color='green', ha='left')
		s1.text(85.35, -1.45, 'WCS', frame='galactic', color='b', ha='right')
		#s1.text(im, s=im, c=im, cmap='rainbow_r', fontsize=0.01)
		#s1.vector(im, s=im.data/im.data.max()*500, c=0, cmap='gist_rainbow_r')
		#m = s1.gridspectra(gridfg1, color='b', clip=False, grid_scale=1)
		#s1.gridspectra(gridfg2, color='r', clip=False, grid_scale=1, ylim=m[0][0].get_ylim(), xlim=m[0][0].get_xlim())
		#s1.set_world_xlim(85.4, 85.31)
		#s1.set_world_ylim(-1.55, -1.42)

	### scatter
	if 0:
		fig, ax = subplots(2, 2, projection=r)
		ax = ax.ravel()
		try:ax[0].scatter()
		except:pass

		#ax[1].scatter(r, s=r, c=r)

		ax[2].scatter([84, 85, 86], [-2, -1, -2], s=100, c='k', frame='galactic', marker='x')

		ax[3].scatter([313.36540654, 312.09927537, 314.10086199], [43.17682077, 45.22041731, 45.34991142], \
			s = [200,100,200], frame='icrs', marker='+', color='red', facecolor=(0,0,1,0.9))
		show()

	### text
	if 0:
		fig, ax = subplots(2, 2, projection=r)
		ax = ax.ravel()
		#ax[0].imshow(r)
		ax[0].text(85, 0, 'Gal', frame='galactic')

		#t = np.abs(np.random.normal(0, 1, (5,5)))
		r = fits.open(r)[0]
		r.data[r.data<3] = np.nan
		ax[1].text(r, s=r, c=r)

		ax[2].text([84, 85, 86], [-2, -1, -2], 'abc', s=10, c='k', frame='galactic', linewidths=3)

		ax[3].plot([313.36540654, 312.09927537, 314.10086199], [43.17682077, 45.22041731, 45.34991142], 'k-', frame='icrs')
		ax[3].text([313.36540654, 312.09927537, 314.10086199], [43.17682077, 45.22041731, 45.34991142], 'ABC', \
			s = [2,1,2], frame='icrs', marker='o', color='red', facecolor=(0,1,1,0.5), va=1, ha=0.8)
		show()

	### vector
	if 0:
		fig, ax = subplots(2, 2, projection=r)
		ax = ax.ravel()
		try:ax[0].vector()
		except:pass

		r = fits.open(r)[0]
		r.data[r.data<3] = np.nan
		ax[1].vector(r, r.data, s=r.data*10, c=r, unit='rad')

		ax[2].vector([84, 84, 85, 85, 86, 86], [-2, -1, -2, -1, -2, -1], [0, 45, 90, 120, 150, 180], \
			s=100, c='k', frame='galactic')

		ax[3].vector([313.36540654, 312.09927537, 314.10086199], [43.17682077, 45.22041731, 45.34991142], [0,45,90], \
			s = [200,100,200], frame='icrs', marker='o', c=['r','g','b'], facecolor=(0,1,1,0.5))
		show()

	###scatter, box, circle, arrow, text
	if 0:
		s1 = subplot(111, projection=r)
		s1.plot([84, 85, 86], [-2, -1, -2], 'k.-', frame='galactic')
		s1.scatter([313.36540654, 312.09927537, 314.10086199], [43.17682077, 45.22041731, 45.34991142], frame='icrs', marker='o', color='red', facecolor=(0,1,1,0.5))
		s1.text(84, 1, 'abc', frame='galactic', ha='right', va='center')
		
		#s1.rectangle(313, 44, 1, 1, pa=10, edgecolor='red', facecolor=(1,0,0,0.3), frame='icrs')

		s1.quadrangle(85.7, -1.5, 1, 1, edgecolor='k', facecolor='none', frame='galactic')
		s1.circle(85.7, -1.5, 1, frame='galactic', edgecolor='k', facecolor='none')
		s1.ellipse(85.7, -1.5, 1, 1, frame='galactic', edgecolor='red', facecolor='none')
		for pa in [0,45,90,120, 135, 150]:
			s1.arc(85.7, -1.5, 0.25, 1, pa, 0, 135, edgecolor=((150-pa)/150, 0, pa/150, 0.4), frame='galactic', facecolor='none')
			#s1.arrow(85.7, -1.5, 85.7+0.5, -1.5+pa/60-1.5, edgecolor=((150-pa)/150, 0, pa/150, 0.4), frame='galactic', facecolor='green', head_width=0.1, head_length=0.1)

		s1.quadrangle(313, 44, 1, 1, edgecolor='k', facecolor='none', frame='icrs')
		s1.circle(313, 44, 1, frame='fk5', edgecolor='k', facecolor='none')
		s1.ellipse(313, 44, 1, 1, frame='fk5', edgecolor='red', facecolor='none')
		for pa in [0,45,90,120, 135, 150]:
			s1.arc(313, 44, 0.25, 1, pa, 0, 135, edgecolor=((150-pa)/150, 0, pa/150, 0.4), frame='fk5', facecolor='none')
			#s1.arrow(313, 44, 313+0.5, 44+pa/60-1.5, edgecolor=((150-pa)/150, 0, pa/150, 0.4), frame='fk5', facecolor='green', head_width=0.1, head_length=0.1)
		
	### MWISP guidemap, detail NORM setting
	if 0:
		r = EasyWCSImage.load('/Users/shaobo/Work/mwisp/GuideMap/cleanedTiles/tile_L2_m0clip33_corr.fits')
		g = EasyWCSImage.load('/Users/shaobo/Work/mwisp/GuideMap/cleanedTiles/tile_L_m0clip253_corr.fits')
		b = EasyWCSImage.load('/Users/shaobo/Work/mwisp/GuideMap/cleanedTiles/tile_U_m0clip253_corr.fits')

		print('>>>config')
		rgb = EasyWCSImage.load(fits.PrimaryHDU(data=np.vstack((r.data+g.data/10, g.data, b.data)), header=r.header))
		#print(rgb.nx, rgb.ny, rgb.nc)
		#rgb = EasyWCSImageList.load(r.data+g.data/10, g.data, b)
		rgb.config(scale='sqrt', vmin=(0, 0, -0.3), vmax=(10, 35, 120))
		image, norm = rgb.image

		print('>>start imshow')
		fig, ax = subplots(nrows=3, wcs=rgb, sharey=True)
		ax[0].imshow(image, vmin=0, vmax=1)
		ax[0].set_world_xlim(82, 10)
		ax[0].set_world_ylim(-5.25, 5.25)

		ax[1].imshow(image, vmin=0, vmax=1)
		ax[1].set_world_xlim(152, 82)

		ax[2].imshow(image, vmin=0, vmax=1)
		ax[2].set_world_xlim(222, 152)
		

	###Channel map
	if 0:
		fig = figure(figsize=(10,10))
		sps = channelmap(ncols=5, figure=fig, projection=gridbg)
		m = sps.imshow(gridfg1, index=50+np.arange(29), vmin=0, vmax=20)
		sps.colorbar(m)
		sps.text(0.05, 0.85, ['%+.2f km/s' % v for v in np.linspace(-10,10,29)], frame=None, color='w', ha='left')
		#ax = EasyWCSAxesChannelMaps(figure(figsize=(10,10)), nrows=6, ncols=5, projection=gridbg)
		#ax.imshow(gridfg1, index=np.arange(50, 1200,1), vmin=0, vmax=15)


	### spectra in grid
	if 0:
		cfalut = mpl.colors.ListedColormap(fits.open('/Users/shaobo/Work/script/mylib/userct/cfa.fits')[0].data)

		#L = DataCube.openMWISP('/Users/shaobo/Work/mwisp/GuideMap/cleanedTiles/MOC0400-010_U.fits')
		L = DataCube.openMWISP('/Users/shaobo/Downloads/0400-010U.fits')
		L._data[L._data < -999] = np.nan
		bg = L.subcube(zlo=-20*u.km/u.s, zhi=100*u.km/u.s).moment(order=0)
		s = subplot(111, projection=bg)
		s.imshow(bg/1e3, cmap='gray', aspect='equal')
		#L = L[:, 20:40, 6:15]
		#L = L.rebinvelocity(-150,200,70)
		xi,yi = 6, 10
		L = L[:, yi:yi+15, xi:xi+10]
		s.gridspectra(L, xlim=[-20, 100], ylim=[-5,+15], color='r')
		s.set_xlim(5,15)
		s.set_ylim(10,20)


	### fk5 galaxy
	if 0:
		gxr = '/Users/shaobo/Work/colleague/qhtan/ID21_F444W_CLEAR.fits'
		gxg = '/Users/shaobo/Work/colleague/qhtan/ID21_F277W_CLEAR.fits'
		gxb = '/Users/shaobo/Work/colleague/qhtan/ID21_F150W_CLEAR.fits'

		ax = subplot(111, wcs=gxr)
		m = ax.imshow(gxr,gxg,gxb, scale='lin', limit=[98,98,98], vmin=0)
		#ax.colorbar(m)
		#ax.circle(149.7150892, 2.0643034, diameter=0.5*u.arcsec, edgecolor='r', facecolor='none', frame='fk5')
		#ax.plot(149.7150892+np.array([-2, 2])/3600, 2.0643034+np.array([0,0]), 'r-', frame='fk5')
		#ax.text(149.7150892, 2.0643034, 'RGB', frame='fk5', color='r', fontsize=15, transform=ax.transAxes)
		#ax.text(0.1, 0.9, 'RGB', color='r', fontsize=20, transform=ax.transAxes)
		#ax.set_xlim(150,250)
		#ax.set_ylim(150,250)
		#ax.set_world_xlim(149.7150892-2/3600, 149.7150892+2/3600)
		#ax.set_world_ylim(2.0643034-2/3600, 2.0643034+2/3600)
		ax.set_world_box(149.7150892, 2.0643034, 5/3600, 5/3600)
		ax.coords[0].tick_params(top=False, bottom=False, labeltop=False, labelbottom=False, direction='in')
		ax.coords[1].tick_params(left=False, right=False, labelleft=False, labelright=False, direction='in')


	ax = plt.subplot(111, projection=WCS(naxis=2))
	ax.imshow(fits.open(bg)[0].data)
	print(type(ax))
	for f in dir(ax):
		if 'proj' in f: print(f)
	print(help(ax.reset_wcs))
	ax.reset_wcs(WCS(fits.getheader(fg), naxis=2))
	ax.imshow(fits.open(bg)[0].data)

	#xg,yg = np.meshgrid(np.linspace(312.5, 313.5, 5), np.linspace(43.5, 44.5, 5))
	#s1.quiver(xg.ravel(), yg.ravel(), np.repeat(0.5,25), np.repeat(0.0,25), color='r', frame='icrs')
	
	#s1.beam(major=3*u.deg, minor=3*u.deg, frame=True)
	'''
	print(type(s1.axes))

	s2 = EasyWCSSubplot(122, figure=fig, projection=fg)
	m = s2.imshow(b, scale='lin', limit=99, cmap='Greys')
	m1 = s2.imshow(None, None, g, g, scale='lin', limit=95, cmap='Greys')
	m2 = s2.imshow(r, None, None, r, scale='sqrt', vmin=1, cmap='Greys')
	s2.colorbar(m, hspace=0.02)
	#s2 = EasyWCSAxes([.4,.5,.2,.2], projection=fg, figure=s1.figure, facecolor='g')
	#s2.imshow(r,g,b, limit=99, scale='log', alpha=0.9, zorder=0)

	#im = EasyWCSImageList.load(r,g,b)
	#im.config(scale='log', limit=90)
	#image, norm = im.image
	#s = fig.add_subplot()
	#s.imshow(image, origin='lower')#, norm=norm)

	#fig.colorbar()
	'''
	'''
	import matplotlib as mpl
	s1 = fig.add_subplot(131)
	m = s1.imshow(im.data[0], vmin=10, vmax=90, origin='lower')
	fig.colorbar(m, ax=s1)
	#fig.colorbar(colors.Normalize(), cax=s2, norm=colors.LogNorm(vmin=5, vmax=100))
	
	###as scalar
	s2 = fig.add_subplot(132)
	#print(EasyNorm.get('sqrt', vmin=1, vmax=100)(np.linspace(0,150,20)))
	m = s2.imshow(im.data[0], origin='lower', norm=EasyNorm.get('he', vmin=10, vmax=100))
	#import matplotlib.ticker as ticker
	cb = fig.colorbar(m, ax=s2)
	
	###as channel
	s3 = fig.add_subplot(133)
	norm = EasyNorm.get('he', vmin=10, vmax=100)
	norm_im = norm(im.data[0])
	print(norm.vmin,norm.vmax)
	print(np.nanmin(norm_im))
	#print('after first call', norm_im)
	m = s3.imshow(norm_im, vmin=0, vmax=1, origin='lower')
	cb = fig.colorbar(mpl.cm.ScalarMappable(norm=norm), ax=s3)
	'''
	show()


	'''
	sg = SpectraGridMap(fits.getheader('/Users/shaobo/Work/script/mwisp_package_test/example/test_plot_img.fits'))
	sg.imshow('/Users/shaobo/Work/script/mwisp_package_test/example/test_plot_img.fits', cmap='RdBu_r', alpha=0.8)
	sg.step('/Users/shaobo/Work/script/mwisp_package_test/example/test_plot_cube.fits', color='k')
	#sg.plot('/Users/shaobo/Work/script/mwisp_package_test/example/test_plot_cube_L.fits', 'r-')
	plt.show()
	'''