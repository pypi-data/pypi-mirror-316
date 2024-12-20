# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 17:20:04 2024

@author: mbmad
"""

__version__ = '1.0.1'

__default_setting_keys__ = ['SLEAP',
                            'CONDA',
                            'FFMPEG',
                            'MODEL',
                            'VIDEO_SOURCE',
                            'VIDEO_TRANSCODED',
                            'PREDICTIONS',
                            'H5',
                            'FR_ADJUST_ENABLED',
                            'FR_ADJUSTED',
                            'TARGET_FRAMERATE'
                            ]
__setting_types__ = {'SLEAP': 'externalpath',
                     'CONDA': 'externalpath',
                     'FFMPEG': 'cmd',
                     'MODEL': 'externalpath',
                     'VIDEO_SOURCE': 'projectpath',
                     'VIDEO_TRANSCODED': 'projectpath',
                     'PREDICTIONS': 'projectpath',
                     'H5': 'projectpath',
                     'FR_ADJUST_ENABLED': 'setting',
                     'FR_ADJUSTED': 'projectpath',
                     'TARGET_FRAMERATE': 'setting'
                     }
__default_setting_values__ = {'SLEAP': 'path/to/SLEAP/env',
                              'CONDA': r'C:\Users\<YourUsername>\anaconda3\Scripts\activate.bat',
                              'FFMPEG': '-vsync 0 -f image2pipe -vcodec ppm - | ffmpeg -f image2pipe -framerate 25 -i - -c:v libx264 -crf 23 -pix_fmt yuv420p',
                              'MODEL': 'path/to/SLEAP/model/training_data.json',
                              'VIDEO_SOURCE': 'path/to/untranscodedvideo',
                              'VIDEO_TRANSCODED': 'path/to/tracoded/videos',
                              'PREDICTIONS': 'path/to/predictions',
                              'H5': 'path/to/H5/files',
                              'FR_ADJUST_ENABLED': True,
                              'FR_ADJUSTED': 'path/to/adjusted_framerate',
                              'TARGET_FRAMERATE': 10
                              }

__project_structure__ = {'VIDEO_SOURCE': 'untranscoded_video',
                         'VIDEO_TRANSCODED': 'transcoded_video',
                         'PREDICTIONS': 'prediction_files',
                         'H5': 'h5_files',
                         'FR_ADJUSTED': 'framerate_adjusted_trajectories'
                         }
__default_setting_names__ = {'SLEAP': 'SLEAP conda environment path',
                             'CONDA': 'Anaconda activate.bat script',
                             'FFMPEG': 'FFMPEG command',
                             'MODEL': 'Trained SLEAP model location',
                             'VIDEO_SOURCE': 'Path to original video files',
                             'VIDEO_TRANSCODED': 'Path to store transcoded files',
                             'PREDICTIONS': 'Path to store prediction files',
                             'H5': 'Path to store H5 files',
                             'FR_ADJUST_ENABLED': 'Adjust prediction framerate?',
                             'FR_ADJUSTED': 'Path to store framerate adjusted data',
                             'TARGET_FRAMERATE': 'Target Framerate (fps)'
                             }
__accepted_video_extensions__ = [".mp4", ".mkv", ".mov", ".flv", ".wmv",
                                 ".webm", ".mpg", ".mpeg", ".ts", ".m2ts",
                                 ".3gp", ".vob", ".mxf", ".avi", ".m4v",
                                 ".f4v", ".rm", ".rmvb", ".asf", ".ogv",
                                 ".dv", ".amv", ".qt", ".yuv", ".ivf"
                                 ]
