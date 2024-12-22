# Description: Cache utilities for huggingface.


def find_hf_home_dir() -> str | None:
    """
    Find the huggingface home directory.
    """
    import os
    import logging

    logger = logging.getLogger(__name__)

    result = None
    if "HF_HOME" in os.environ:
        result = os.environ["HF_HOME"]
        if os.path.exists(result) and os.path.isdir(result):
            return result
        else:
            logger.warning(f"Invalid HF_HOME directory: {result}")
    result = os.path.join(os.path.expanduser("~"), ".cache", "huggingface")
    if os.path.exists(result) and os.path.isdir(result):
        return result
    else:
        logger.warning(f"Invalid default HuggingFace home directory: {result}")
    return None


def find_hf_hub_dir() -> str | None:
    """
    Find the huggingface hub cache directory.
    """
    import os
    import logging

    logger = logging.getLogger(__name__)

    result = None
    if "HUGGINGFACE_HUB_CACHE" in os.environ:
        result = os.environ["HUGGINGFACE_HUB_CACHE"]
        if os.path.exists(result) and os.path.isdir(result):
            return result
        else:
            logger.warning(f"Invalid HUGGINGFACE_HUB_CACHE directory: {result}")
    if "HF_HOME" in os.environ:
        result = os.path.join(os.environ["HF_HOME"], "hub")
        if os.path.exists(result) and os.path.isdir(result):
            return result
        else:
            logger.warning(f"Invalid HF_HOME directory: {result}")
    result = os.path.join(os.path.expanduser("~"), ".cache", "huggingface", "hub")
    if os.path.exists(result) and os.path.isdir(result):
        return result
    else:
        logger.warning(f"Invalid default HuggingFace Hub directory: {result}")
    return None


def find_hf_datasets_dir() -> str | None:
    """
    Find the huggingface datasets cache directory.
    """
    import os
    import logging

    logger = logging.getLogger(__name__)

    result = None
    if "HF_DATASETS_CACHE" in os.environ:
        result = os.environ["HF_DATASETS_CACHE"]
        if os.path.exists(result) and os.path.isdir(result):
            return result
        else:
            logger.warning(f"Invalid HF_DATASETS_CACHE directory: {result}")
    if "HF_HOME" in os.environ:
        result = os.path.join(os.environ["HF_HOME"], "datasets")
        if os.path.exists(result) and os.path.isdir(result):
            return result
        else:
            logger.warning(f"Invalid HF_HOME directory: {result}")
    result = os.path.join(os.path.expanduser("~"), ".cache", "huggingface", "datasets")
    if os.path.exists(result) and os.path.isdir(result):
        return result
    else:
        logger.warning(f"Invalid default HuggingFace datasets directory: {result}")
    return None


def find_xdg_cache_home() -> str | None:
    """
    Find the XDG cache directory.
    """
    import os
    import logging

    logger = logging.getLogger(__name__)

    result = None
    if "XDG_CACHE_HOME" in os.environ:
        result = os.environ["XDG_CACHE_HOME"]
        if os.path.exists(result) and os.path.isdir(result):
            return result
        else:
            logger.warning(f"Invalid XDG_CACHE_HOME directory: {result}")
    result = os.path.join(os.path.expanduser("~"), ".cache")
    if os.path.exists(result) and os.path.isdir(result):
        return result
    else:
        logger.warning(f"Invalid default XDG cache directory: {result}")
    return None


# HF_HOME                 ~/.cache/huggingface
# HUGGINGFACE_HUB_CACHE   ~/.cache/huggingface/hub
# HF_DATASETS_CACHE       ~/.cache/huggingface/datasets
# TRANSFORMERS_CACHE      ~/.cache/huggingface/transformers
# TRANSFORMERS_CACHE is deprecated, use `HF_HOME` instead.
# XDG_CACHE_HOME          ~/.cache


def find_model_dir(model: str) -> str | None:
    """
    Find the model directory.
    """
    import os
    import logging

    logger = logging.getLogger(__name__)

    base_dir = find_hf_hub_dir()
    if base_dir is None:
        hf_home = find_hf_home_dir()
        if hf_home is None:
            xdg_cache_home = find_xdg_cache_home()
            if xdg_cache_home is None:
                logger.error("Could not find a suitable cache directory.")
                return None
            else:
                base_dir = os.path.join(xdg_cache_home, "huggingface", "hub")
        else:
            base_dir = os.path.join(hf_home, "hub")

    if base_dir is None:
        logger.error("Could not find a suitable cache directory.")
        return None

    model_path = "models--" + model.replace("/", "--")

    model_dir = os.path.join(base_dir, model_path)

    if not os.path.exists(model_dir):
        logger.error(f"Model directory not found: {model_dir}")
        return None

    model_dir = os.path.join(base_dir, model_path)

    if not os.path.exists(model_dir):
        logger.error(f"Model directory not found: {model_dir}")
        return None

    with open(os.path.join(model_dir, "refs", "main"), "r", encoding="utf-8") as f:
        oid = f.read().replace("\n", "")

    lfs_dir = os.path.join(model_dir, "snapshots", oid)
    if not os.path.exists(lfs_dir):
        logger.error(f"Model directory not found: {lfs_dir}")
        return None

    return lfs_dir


def find_datasets_dir(datasets: str) -> str | None:
    """
    Find the dataset directory.
    """
    import os
    import logging

    logger = logging.getLogger(__name__)

    base_dir = find_hf_datasets_dir()
    if base_dir is None:
        hf_home = find_hf_home_dir()
        if hf_home is None:
            xdg_cache_home = find_xdg_cache_home()
            if xdg_cache_home is None:
                logger.error("Could not find a suitable cache directory.")
                return None
            else:
                base_dir = os.path.join(xdg_cache_home, "huggingface", "datasets")
        else:
            base_dir = os.path.join(hf_home, "datasets")

    if base_dir is None:
        logger.error("Could not find a suitable cache directory.")
        return None

    dataset_path = "datasets--" + datasets.replace("/", "--")

    dataset_dir = os.path.join(base_dir, dataset_path)

    if not os.path.exists(dataset_dir):
        logger.error(f"Dataset directory not found: {dataset_dir}")
        return None

    if not os.path.exists(dataset_dir):
        logger.error(f"Datasets directory not found: {dataset_dir}")
        return None

    with open(os.path.join(dataset_dir, "refs", "main"), "r", encoding="utf-8") as f:
        oid = f.read().replace("\n", "")

    lfs_dir = os.path.join(dataset_dir, "snapshots", oid)
    if not os.path.exists(lfs_dir):
        logger.error(f"Datasets directory not found: {lfs_dir}")
        return None

    return lfs_dir
