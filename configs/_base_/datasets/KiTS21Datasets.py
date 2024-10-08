# 데이터셋 타입과 경로를 수정
dataset_type = 'KiTS21Datasets'
data_root = './datasets/'
test_data_root = './datasets/test-small/'
test_img_dir = 'images'
test_mask_dir = 'masks'
img_dir = 'images/'
ann_dir = 'labels'

crop_size = (256,256)

train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='LoadAnnotations', reduce_zero_label=False),
    dict(type='RandomResize', scale=(256, 256), ratio_range=(0.5, 2.0), keep_ratio=True),
    dict(type='RandomCrop', crop_size=(256, 256), cat_max_ratio=0.75),
    dict(type='RandomFlip', prob=0.5),
    dict(type='PhotoMetricDistortion'),
    dict(type='PackSegInputs'),
]

# validation 파이프라인 설정
val_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='Resize', scale=(256, 256), keep_ratio=True),
    dict(type='LoadAnnotations', reduce_zero_label=False),  
    dict(type='PackSegInputs'),
]

# test 파이프라인 설정
test_pipeline = val_pipeline

img_ratios = [0.5, 0.75, 1.0, 1.25, 1.5, 1.75]
tta_pipeline = [
    dict(type='LoadImageFromFile', backend_args=None),
    dict(
        type='TestTimeAug',
        transforms=[
            [
                dict(type='Resize', scale_factor=r, keep_ratio=True)
                for r in img_ratios
            ],
            [
                dict(type='RandomFlip', prob=0., direction='horizontal'),
                dict(type='RandomFlip', prob=1., direction='horizontal')
            ], [dict(type='LoadAnnotations')], [dict(type='PackSegInputs')]
        ])
]

train_dataloader = dict(
    batch_size=8, #배치사이즈 24
    dataset=dict(
        type='KiTS21Datasets',
        data_root=data_root,
        data_prefix=dict(img_path=img_dir, seg_map_path=ann_dir),
        pipeline=train_pipeline,
        reduce_zero_label=False,  # 여기서 reduce_zero_label 설정
        ann_file='splits/train.txt', 
    ),
    num_workers=4,
    persistent_workers=True,
    sampler=dict(shuffle=True, type='DefaultSampler')
)

val_dataloader = dict(
    batch_size=1,
    dataset=dict(
        type='KiTS21Datasets',
        data_root=data_root,
        data_prefix=dict(img_path=img_dir, seg_map_path=ann_dir),
        pipeline=val_pipeline,
        reduce_zero_label=False,  # 여기서 reduce_zero_label 설정
        ann_file='splits/val.txt',
    ),
    num_workers=4,
    persistent_workers=True,
    sampler=dict(shuffle=False, type='DefaultSampler')
)

test_dataloader =  dict(
    batch_size=1,
    dataset=dict(
        type='KiTS21Datasets',
        data_root=test_data_root,
        data_prefix=dict(img_path=test_img_dir, seg_map_path=test_mask_dir),
        pipeline=test_pipeline,
        reduce_zero_label=False,  # 여기서 reduce_zero_label 설정
    ),
    num_workers=4,
    persistent_workers=True,
    sampler=dict(shuffle=False, type='DefaultSampler')
)

