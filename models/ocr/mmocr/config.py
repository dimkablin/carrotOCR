# pylint: disable=W,R,E,C
default_hooks = dict(
    checkpoint=dict(interval=1, type='CheckpointHook'),
    logger=dict(interval=1, type='LoggerHook'),
    param_scheduler=dict(type='ParamSchedulerHook'),
    sampler_seed=dict(type='DistSamplerSeedHook'),
    sync_buffer=dict(type='SyncBuffersHook'),
    timer=dict(type='IterTimerHook'),
    visualization=dict(
        draw_gt=False,
        draw_pred=False,
        enable=False,
        interval=1,
        show=False,
        type='VisualizationHook'))
default_scope = 'mmocr'
dictionary = dict(
    dict_file=
    '../models/ocr/mmocr/russian_dict.txt',
    same_start_end=True,
    type='Dictionary',
    with_end=True,
    with_padding=True,
    with_start=True,
    with_unknown=True)
env_cfg = dict(
    cudnn_benchmark=False,
    dist_cfg=dict(backend='nccl'),
    mp_cfg=dict(mp_start_method='fork', opencv_num_threads=0))
load_from = None
log_level = 'INFO'
log_processor = dict(by_epoch=True, type='LogProcessor', window_size=10)
model = dict(
    backbone=dict(type='ResNet31OCR'),
    data_preprocessor=dict(
        mean=[
            127,
            127,
            127,
        ],
        std=[
            127,
            127,
            127,
        ],
        type='TextRecogDataPreprocessor'),
    decoder=dict(
        d_k=512,
        dec_bi_rnn=False,
        dec_do_rnn=0,
        dec_gru=False,
        dictionary=dict(
            dict_file=
            '../models/ocr/mmocr/russian_dict.txt',
            same_start_end=True,
            type='Dictionary',
            with_end=True,
            with_padding=True,
            with_start=True,
            with_unknown=True),
        enc_bi_rnn=False,
        max_seq_len=30,
        module_loss=dict(
            ignore_first_char=True, reduction='mean', type='CEModuleLoss'),
        postprocessor=dict(type='AttentionPostprocessor'),
        pred_concat=True,
        pred_dropout=0.1,
        type='ParallelSARDecoder'),
    encoder=dict(
        enc_bi_rnn=False, enc_do_rnn=0.1, enc_gru=False, type='SAREncoder'),
    type='SARNet')
optim_wrapper = dict(
    optimizer=dict(lr=0.001, type='Adam'), type='OptimWrapper')
param_scheduler = [
    dict(end=5, milestones=[
        3,
        4,
    ], type='MultiStepLR'),
]
randomness = dict(seed=0)
resume = False
test_cfg = dict(type='TestLoop')
test_dataloader = dict(
    batch_size=1,
    dataset=dict(
        datasets=[
            dict(
                ann_file='val.json',
                data_prefix=dict(img_path='val'),
                data_root=None,
                parser_cfg=dict(
                    keys=[
                        'filename',
                        'text',
                    ], type='LineJsonParser'),
                pipeline=None,
                type='RecogTextDataset'),
        ],
        pipeline=[
            dict(type='LoadImageFromFile'),
            dict(
                height=48,
                max_width=160,
                min_width=48,
                type='RescaleToHeight',
                width_divisor=4),
            dict(type='PadToWidth', width=160),
            dict(type='LoadOCRAnnotations', with_text=True),
            dict(
                meta_keys=(
                    'img_path',
                    'ori_shape',
                    'img_shape',
                    'valid_ratio',
                ),
                type='PackTextRecogInputs'),
        ],
        type='ConcatDataset'),
    drop_last=False,
    num_workers=4,
    persistent_workers=True,
    sampler=dict(shuffle=False, type='DefaultSampler'))
test_evaluator = dict(
    dataset_prefixes=[
        'RUS',
    ],
    metrics=[
        dict(
            mode=[
                'exact',
                'ignore_case',
                'ignore_case_symbol',
            ],
            type='WordMetric'),
        dict(type='CharMetric'),
    ],
    type='MultiDatasetsEvaluator')
test_list = [
    dict(
        ann_file='val.json',
        data_prefix=dict(img_path='val'),
        data_root=None,
        parser_cfg=dict(keys=[
            'filename',
            'text',
        ], type='LineJsonParser'),
        pipeline=None,
        type='RecogTextDataset'),
]
test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(
        height=48,
        max_width=160,
        min_width=48,
        type='RescaleToHeight',
        width_divisor=4),
    dict(type='PadToWidth', width=160),
    dict(type='LoadOCRAnnotations', with_text=True),
    dict(
        meta_keys=(
            'img_path',
            'ori_shape',
            'img_shape',
            'valid_ratio',
        ),
        type='PackTextRecogInputs'),
]
train_cfg = dict(max_epochs=10, type='EpochBasedTrainLoop', val_interval=1)
train_dataloader = dict(
    batch_size=30,
    dataset=dict(
        datasets=[
            dict(
                ann_file='train.json',
                data_prefix=dict(img_path='train'),
                data_root=None,
                parser_cfg=dict(
                    keys=[
                        'filename',
                        'text',
                    ], type='LineJsonParser'),
                pipeline=None,
                type='RecogTextDataset'),
        ],
        pipeline=[
            dict(ignore_empty=True, min_size=2, type='LoadImageFromFile'),
            dict(type='LoadOCRAnnotations', with_text=True),
            dict(
                height=48,
                max_width=160,
                min_width=48,
                type='RescaleToHeight',
                width_divisor=4),
            dict(type='PadToWidth', width=160),
            dict(
                meta_keys=(
                    'img_path',
                    'ori_shape',
                    'img_shape',
                    'valid_ratio',
                ),
                type='PackTextRecogInputs'),
        ],
        type='ConcatDataset'),
    num_workers=4,
    persistent_workers=True,
    sampler=dict(shuffle=True, type='DefaultSampler'))
train_list = [
    dict(
        ann_file='train.json',
        data_prefix=dict(img_path='train'),
        data_root=None,
        parser_cfg=dict(keys=[
            'filename',
            'text',
        ], type='LineJsonParser'),
        pipeline=None,
        type='RecogTextDataset'),
]
train_pipeline = [
    dict(ignore_empty=True, min_size=2, type='LoadImageFromFile'),
    dict(type='LoadOCRAnnotations', with_text=True),
    dict(
        height=48,
        max_width=160,
        min_width=48,
        type='RescaleToHeight',
        width_divisor=4),
    dict(type='PadToWidth', width=160),
    dict(
        meta_keys=(
            'img_path',
            'ori_shape',
            'img_shape',
            'valid_ratio',
        ),
        type='PackTextRecogInputs'),
]
tta_model = dict(type='EncoderDecoderRecognizerTTAModel')
tta_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(
        transforms=[
            [
                dict(
                    condition="results['img_shape'][1]<results['img_shape'][0]",
                    true_transforms=[
                        dict(
                            args=[
                                dict(cls='Rot90', k=0, keep_size=False),
                            ],
                            type='ImgAugWrapper'),
                    ],
                    type='ConditionApply'),
                dict(
                    condition="results['img_shape'][1]<results['img_shape'][0]",
                    true_transforms=[
                        dict(
                            args=[
                                dict(cls='Rot90', k=1, keep_size=False),
                            ],
                            type='ImgAugWrapper'),
                    ],
                    type='ConditionApply'),
                dict(
                    condition="results['img_shape'][1]<results['img_shape'][0]",
                    true_transforms=[
                        dict(
                            args=[
                                dict(cls='Rot90', k=3, keep_size=False),
                            ],
                            type='ImgAugWrapper'),
                    ],
                    type='ConditionApply'),
            ],
            [
                dict(
                    height=48,
                    max_width=160,
                    min_width=48,
                    type='RescaleToHeight',
                    width_divisor=4),
            ],
            [
                dict(type='PadToWidth', width=160),
            ],
            [
                dict(type='LoadOCRAnnotations', with_text=True),
            ],
            [
                dict(
                    meta_keys=(
                        'img_path',
                        'ori_shape',
                        'img_shape',
                        'valid_ratio',
                    ),
                    type='PackTextRecogInputs'),
            ],
        ],
        type='TestTimeAug'),
]
txt_rus_dataset_root = None
txt_rus_dataset_train = dict(
    ann_file='train.json',
    data_prefix=dict(img_path='train'),
    data_root=None,
    parser_cfg=dict(keys=[
        'filename',
        'text',
    ], type='LineJsonParser'),
    pipeline=None,
    type='RecogTextDataset')
txt_rus_dataset_val = dict(
    ann_file='val.json',
    data_prefix=dict(img_path='val'),
    data_root=None,
    parser_cfg=dict(keys=[
        'filename',
        'text',
    ], type='LineJsonParser'),
    pipeline=None,
    type='RecogTextDataset')
val_cfg = dict(type='ValLoop')
val_dataloader = dict(
    batch_size=1,
    dataset=dict(
        datasets=[
            dict(
                ann_file='val.json',
                data_prefix=dict(img_path='val'),
                data_root=None,
                parser_cfg=dict(
                    keys=[
                        'filename',
                        'text',
                    ], type='LineJsonParser'),
                pipeline=None,
                type='RecogTextDataset'),
        ],
        pipeline=[
            dict(type='LoadImageFromFile'),
            dict(
                height=48,
                max_width=160,
                min_width=48,
                type='RescaleToHeight',
                width_divisor=4),
            dict(type='PadToWidth', width=160),
            dict(type='LoadOCRAnnotations', with_text=True),
            dict(
                meta_keys=(
                    'img_path',
                    'ori_shape',
                    'img_shape',
                    'valid_ratio',
                ),
                type='PackTextRecogInputs'),
        ],
        type='ConcatDataset'),
    drop_last=False,
    num_workers=4,
    persistent_workers=True,
    sampler=dict(shuffle=False, type='DefaultSampler'))
val_evaluator = dict(
    dataset_prefixes=[
        'RUS',
    ],
    metrics=[
        dict(
            mode=[
                'exact',
                'ignore_case',
                'ignore_case_symbol',
            ],
            type='WordMetric'),
        dict(type='CharMetric'),
    ],
    type='MultiDatasetsEvaluator')
vis_backends = [
    dict(type='LocalVisBackend'),
]
visualizer = dict(
    name=
    'time.struct_time(tm_year=2023, tm_mon=9, tm_mday=12, tm_hour=17, tm_min=21, tm_sec=54, tm_wday=1, tm_yday=255, tm_isdst=0)',
    type='TextRecogLocalVisualizer',
    vis_backends=[
        dict(type='LocalVisBackend'),
    ])
work_dir = None
