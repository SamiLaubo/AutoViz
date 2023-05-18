import numpy as np

SONG_BANK = {}

# SONG_BANK['trolltekno'] = {
#     'times': np.array([0, 15, 20, 30, 40]),
#     'effects': ['troll-1', 'troll-2', 'blue', 'rave1', 'bounce-rainbow']
# }

SONG_BANK["I'm Good (Blue)"] = {
    'times': np.array([0, 15, 30, 
                       45, 60, 75, 
                       90, 105, 120,
                       135, 150, 165]),
    'effects': ['red-rain', 'blue-rain', 'whoopety-whoopety', 
                'half-blue-faster', 'red-rain', 'bounce-rainbow',
                'rainbow-full', 'half-blue-faster', 'bounce-borealis',
                'bounce-half-blue', 'bounce-blue', 'blue-rain']
}