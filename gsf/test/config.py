

GSF_SERVER = dict(name='localhost',
                  port='9191')

GSF_SERVICE = dict(name='ENVI')

GSF_TASK = dict(name='SpectralIndex',
                parameters=dict(INPUT_RASTER=dict(url='http://localhost:9191/ese/data/qb_boulder_msi',
                                                  factory='URLRaster'),
                                INDEX='Normalized Difference Vegetation Index')
                )

#: Time it should take to construct a GSF object
INIT_TIME = 2
