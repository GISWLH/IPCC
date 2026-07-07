

def get_ssp(x):
    s = x.scenario
    if 'RCP' in s:
        return 'RCPs Range'
    elif x.model == 'Ev5a':
        return 'ECLIPSE_Ev5a Range'
    elif x.model == 'History' or s == 'History':
        return 'Historical'
    return s.split('-')[0]


def get_type(x):
    models = [
        'CMIP',
        'CMIP5',
        'CMIP6',
        'EDGAR',
        'ECLIPSE',
        'Ev5a',
    ]
    if x.model in models:
        return x.model
    x = x.scenario
    if 'RCP' in x:
        s = x.split('.')
        return '.'.join([s[0][-1], s[1][0]])
    if 'History' in x:
        return ''
    combine_second = '-OS' in x
    vals = x.split('-')
    if len(vals) == 1:
        return vals[0]
    elif combine_second:
        return '-'.join([vals[1], vals[2]])
    else:
        return vals[1]


def get_harmonization(x):
    x = x.scenario
    if x.endswith('Unharmonized'):
        return 'Unharmonized'
    elif 'RCP' in x:
        return 'RCP'
    else:
        return 'default'

def ssp_type(x):
    s, t = get_ssp(x), get_type(x)
    if s.startswith('SSP'):
        return '{}-{}'.format(s, t)
    else:
        return s

def add_categories(df):
    meta = df.meta.index.to_frame()
    df.set_meta(meta.apply(get_ssp, axis=1), name='ssp')
    df.set_meta(meta.apply(get_type, axis=1), name='type')
    df.set_meta(meta.apply(ssp_type, axis=1), name='ssp-type')
    df.set_meta(meta.apply(get_harmonization, axis=1), name='harmonization')
