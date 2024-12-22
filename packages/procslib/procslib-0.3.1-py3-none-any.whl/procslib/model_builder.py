# ===== ADD YOUR MODELS BELOW =====


def get_twitter_logfav_model():
    """A model trained for predicting Twitter log-favorites using AnimeAestheticInference.
    输入anime图片, 输出预测的推特点赞数量(lognp'ed)
    """
    from procslib.models import AnimeAestheticInference

    checkpoint_path = "/rmt/yada/dev/training-flow/models/convbase_twitter_aes_logfav_full_v2cont3_e4_mae0.50.ckpt"
    return AnimeAestheticInference(checkpoint_path=checkpoint_path, column_name="twitter_logfav_score")


def get_weakm_v2_model():
    """A model trained for WeakM aesthetic predictions (v2) with low mean absolute error.
    输入anime图片, 输出预测的weakm v2 score (base score:10)
    """
    from procslib.models import AnimeAestheticInference

    checkpoint_path = "/rmd/yada/checkpoints/aesthetics_weakm-v2_volcanic-salad-49/epoch=4,mae=0.0824,step=0.ckpt"
    return AnimeAestheticInference(checkpoint_path=checkpoint_path, column_name="weakm_v2_score")


def get_siglip_aesthetic_model():
    """A Siglip-based aesthetic model for high-efficiency aesthetic predictions.
    输入anime图片, 输出预测的siglip aesthetic score
        https://github.com/discus0434/aesthetic-predictor-v2-5
    """
    from procslib.models import SiglipAestheticInference

    return SiglipAestheticInference(device="cuda", batch_size=32)


def get_pixiv_compound_score_model():
    """Aesthetic model trained on pixiv data (of the constructed pixiv compound aesthetic score)
    model at "https://bucket-public-access-uw2.s3.us-west-2.amazonaws.com/dist/compound_score_aesthetic_predictor/model.ckpt"
    """
    from procslib.models import PixivCompoundScoreInference

    checkpoint_path = "/rmd/yada/checkpoints/pixiv_compound_aesthetic_convtiny_larry.ckpt"
    return PixivCompoundScoreInference(model_path=checkpoint_path, column_name="pixiv_compound_score")


def get_complexity_ic9600_model():
    """A model trained for predicting image complexity using the IC9600 model.
    输入图片, 输出图片复杂度评分
    """
    from procslib.models import IC9600Inference

    model_path = "/rmd/yada/model_weights/complexity_ic9600_ck.pth"
    return IC9600Inference(model_path=model_path, device="cuda", batch_size=32)


def get_cv2_metrics_model():
    """Calculates OpenCV-based image metrics such as brightness, contrast, noise level, etc.
    输入图片, 输出图片质量评分
    """
    from procslib.models import OpenCVMetricsInference

    return OpenCVMetricsInference(device="cpu", batch_size=32)


def get_rtmpose_model():
    """A model trained for human pose estimation using RTMPose.
    输入图片, 输出人体姿势关键点
    """
    from procslib.models import RTMPoseInference

    onnx_file = "/rmd/yada/checkpoints/rtmpose-l_8xb256-420e_humanart-256x192-389f2cb0_20230611_e2e.onnx"
    return RTMPoseInference(onnx_file=onnx_file, device="cuda")


def get_depth_model():
    """A model trained for depth estimation using MiDaS.
    输入图片, 输出深度图
    """
    from procslib.models import DepthEstimationInference

    return DepthEstimationInference(
        device="cuda",
        batch_size=24,
        lower_percentile=15,
        upper_percentile=95,
    )


def get_q_align_quality_model():
    """A model trained for predicting image quality using QAlign.
    输入图片, 输出图片质量评分
    """
    from procslib.models import QAlignAsyncInference

    return QAlignAsyncInference(task="quality", device="cuda", batch_size=32)


def get_q_align_aesthetics_model():
    """A model trained for predicting image aesthetics using QAlign.
    输入图片, 输出图片美学评分
    """
    from procslib.models import QAlignAsyncInference

    return QAlignAsyncInference(task="aesthetics", device="cuda", batch_size=32)


def get_laion_watermark_model():
    """A model trained for predicting watermarks using Laion.
    输入图片, 输出水印评分
    """
    from procslib.models import LaionWatermarkInference

    return LaionWatermarkInference(device="cuda", batch_size=48)


MODEL_REGISTRY = {
    "twitter_logfav": get_twitter_logfav_model,
    "weakm_v2": get_weakm_v2_model,
    "siglip_aesthetic": get_siglip_aesthetic_model,
    "pixiv_compound_score": get_pixiv_compound_score_model,
    "cv2_metrics": get_cv2_metrics_model,
    "complexity_ic9600": get_complexity_ic9600_model,
    "rtmpose": get_rtmpose_model,
    "depth": get_depth_model,
    "q_align_quality": get_q_align_quality_model,
    "q_align_aesthetics": get_q_align_aesthetics_model,
    "laion_watermark": get_laion_watermark_model,
}


# ============ DO NOT EDIT BELOW THIS LINE ============


def get_model_keys():
    """Retrieves the keys and descriptions of the model registry.

    Returns:
        dict: A dictionary where keys are model names and values are descriptions.
    """
    return {key: func.__doc__.strip() for key, func in MODEL_REGISTRY.items()}


def get_model(descriptor: str):
    """Retrieves the actual model instance associated with the given descriptor.

    Args:
        descriptor (str): The model descriptor key in the MODEL_REGISTRY.

    Returns:
        object: The model instance.

    Raises:
        ValueError: If the descriptor is not found in MODEL_REGISTRY.
    """
    if descriptor not in MODEL_REGISTRY:
        raise ValueError(f"Descriptor '{descriptor}' not found in MODEL_REGISTRY.")
    return MODEL_REGISTRY[descriptor]()
