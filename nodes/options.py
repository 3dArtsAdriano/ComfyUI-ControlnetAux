optional_params = {
    "hed": {
        "safe": ("BOOLEAN", {"default": False}),
        "scribble": ("BOOLEAN", {"default": False})
    },
    "openpose": {
        "include_body": ("BOOLEAN", {"default": True}),
        "include_hand": ("BOOLEAN", {"default": True}),
        "include_face": ("BOOLEAN", {"default": True}),
    },
    "mlsd": {
        "thr_v": ("FLOAT", {"default": 0.1, "min": 0.01, "max": 1.0, "step": 0.01}),
        "thr_d": ("FLOAT", {"default": 0.1, "min": 0.01, "max": 1.0, "step": 0.01}),
    },
    "pidi": {
        "safe": ("BOOLEAN", {"default": True}),
        "scribble": ("BOOLEAN", {"default": True}),
        "apply_filter": ("BOOLEAN", {"default": True}),
    },
    "lineart": {
        "coarse": ("BOOLEAN", {"default": False}),
    },
    "leres": {  # Fixed: was "depth_leres", should be "leres" to match model name
        "boost": ("BOOLEAN", {"default": False}),
    },
    "content": {
        "h": ("INT", {"default": 512, "min": 1, "max": 1024, "step": 1}),
        "w": ("INT", {"default": 512, "min": 1, "max": 1024, "step": 1}),
        "f": ("INT", {"default": 10, "min": 1, "max": 1024, "step": 1}),
    },
    "face_detector": {
        'max_faces': ("INT", {"default": 1, "min": 1, "max": 5, "step": 1}),
        "min_confidence": ("FLOAT", {"default": 0.5, "min": 0.01, "max": 1.0, "step": 0.01}),
    },
    "canny": {
        "low_threshold": ("INT", {"default": 100, "min": 1, "max": 200, "step": 1}),
        "high_threshold": ("INT", {"default": 200, "min": 1, "max": 200, "step": 1}),
    }
}
