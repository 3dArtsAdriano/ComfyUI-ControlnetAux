import traceback
import os
from PIL import Image
from tqdm import tqdm

from controlnet_aux import (
    HEDdetector, MidasDetector, MLSDdetector, OpenposeDetector,
    PidiNetDetector, NormalBaeDetector, LineartDetector,
    LineartAnimeDetector, CannyDetector, ContentShuffleDetector,
    ZoeDetector, MediapipeFaceDetector, SamDetector, LeresDetector, DWposeDetector
)
from .funcs import pil2tensor, tensor2pil, device
from .options import optional_params

# List of controlnet aux models that can be used
models = ["hed", "midas", "mlsd", "openpose", "pidi", "dwpose", "normal_bae", "lineart",
          "lineart_anime", "zoe", "sam", "leres", "canny", "content", "face_detector"]

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

def process_image_wrapper(self, image, detect_resolution=512, image_resolution=512, **kwargs):
    try:
        # Get the model name from the class name
        modaux = self.__class__.__name__.replace("controlaux_", "")
        
        tensor_pil = tensor2pil(image)
        detector = None
        if modaux == "hed":
            detector = HEDdetector.from_pretrained("lllyasviel/Annotators")
        elif modaux == "midas":
            detector = MidasDetector.from_pretrained("lllyasviel/Annotators")
        elif modaux == "mlsd":
            detector = MLSDdetector.from_pretrained("lllyasviel/Annotators")
        elif modaux == "openpose":
            detector = OpenposeDetector.from_pretrained("lllyasviel/Annotators")
        elif modaux == "dwpose":
            script_dir = os.path.dirname(os.path.abspath(__file__))
            det_config = os.path.join(script_dir, "dwpose/yolox_config/yolox_l_8xb8-300e_coco.py")
            pose_config = os.path.join(script_dir, "dwpose/dwpose_config/dwpose-l_384x288.py")
            detector = DWposeDetector(det_config=det_config, pose_config=pose_config, device=device)
        elif modaux == "pidi":
            detector = PidiNetDetector.from_pretrained("lllyasviel/Annotators")
        elif modaux == "normal_bae":
            detector = NormalBaeDetector.from_pretrained("lllyasviel/Annotators")
        elif modaux == "lineart":
            detector = LineartDetector.from_pretrained("lllyasviel/Annotators")
        elif modaux == "lineart_anime":
            detector = LineartAnimeDetector.from_pretrained("lllyasviel/Annotators")
        elif modaux == "zoe":
            detector = ZoeDetector.from_pretrained("lllyasviel/Annotators")
        elif modaux == "sam":
            detector = SamDetector.from_pretrained("ybelkada/segment-anything", subfolder="checkpoints")
        elif modaux == "leres":
            detector = LeresDetector.from_pretrained("lllyasviel/Annotators")
        elif modaux == "canny":
            detector = CannyDetector()
        elif modaux == "content":
            detector = ContentShuffleDetector()
        elif modaux == "face_detector":
            detector = MediapipeFaceDetector()
        else:
            raise ValueError(f"Invalid modaux argument: {modaux}")
        
        # Prepare kwargs for the detector, filtering out ComfyUI-specific parameters
        detector_kwargs = {k: v for k, v in kwargs.items() if k not in ['detect_resolution', 'image_resolution']}
        
        if isinstance(tensor_pil, Image.Image):
            processed_image = detector(tensor_pil, **detector_kwargs) 
            return (pil2tensor(processed_image),)
        
        tensors = []
        pbar = tqdm(range(len(tensor_pil)), desc=f"Processing: {modaux}")
        for tensor in tensor_pil:
            processed_image = detector(tensor, **detector_kwargs)
            tensors.append(processed_image) 
            pbar.update(1)
        return (pil2tensor(tensors),)
    
    except Exception as e:
        traceback.print_exc()
        raise ValueError(f"Error processing image: {e}")

# Create individual classes for each model
for model_name in models:
    def make_input_types(model_name):
        def input_types():
            base_inputs = {
                "required": {
                    "image": ("IMAGE",),
                    "detect_resolution": ("INT", {"default": 512, "min": 256, "max": 1024, "step": 1}),
                    "image_resolution": ("INT", {"default": 512, "min": 256, "max": 1024, "step": 1}),
                }
            }
            
            # Add optional parameters if they exist for this model
            if model_name in optional_params:
                base_inputs["optional"] = optional_params[model_name]
            
            return base_inputs
        return input_types
    
    # Create the class attributes
    class_attrs = {
        "INPUT_TYPES": classmethod(lambda cls, model_name=model_name: make_input_types(model_name)()),
        "RETURN_TYPES": ("IMAGE",),
        "FUNCTION": "process_image",
        "CATEGORY": "ControlNet Auxiliar",
        "process_image": process_image_wrapper
    }
    
    # Create the new class
    new_class = type(f"controlaux_{model_name}", (object,), class_attrs)
    
    # Register the class
    globals()[f"controlaux_{model_name}"] = new_class
    NODE_CLASS_MAPPINGS[f"controlaux_{model_name}"] = new_class
    NODE_DISPLAY_NAME_MAPPINGS[f"controlaux_{model_name}"] = f"ControlNet Aux: {model_name.upper()}"
