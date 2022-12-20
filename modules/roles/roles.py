from .Role import Role

guest = Role(
    'guest',
    'Guest',
    '\N{BUST IN SILHOUETTE}',
    'You don\'t play or you don\'t want to tell on which megaserver you play.'
);

na = Role(
    'na',
    'NA',
    '\N{REGIONAL INDICATOR SYMBOL LETTER U}\N{REGIONAL INDICATOR SYMBOL LETTER S}',
    'You play on the NA megaserver.'
);

eu = Role(
    'eu',
    'EU',
    '\N{REGIONAL INDICATOR SYMBOL LETTER E}\N{REGIONAL INDICATOR SYMBOL LETTER U}',
    'You play on the EU megaserver.'
);

f2p = Role(
    'f2p',
    'F2P',
    '\N{SQUARED FREE}',
    'You play on a f2p account, without the expansions.'
);

