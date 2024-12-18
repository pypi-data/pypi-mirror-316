import torch
from pathlib import Path
from torchvision.models import resnet18
from brainscore_vision.model_helpers.activations.pytorch import PytorchWrapper
from brainscore_vision.model_helpers.brain_transformation import ModelCommitment
from brainscore_vision.model_helpers.activations.pytorch import load_preprocess_images
from collections import OrderedDict
from urllib.request import urlretrieve
import functools
import os


# Custom model loader
def get_model(name):
    assert name == 'barlow_twins_custom'
    url = " https://www.dropbox.com/scl/fi/c6b940qscjb43xhgda9om/barlow_twins-custom_dataset_3-685qxt9j-ep-399.ckpt?rlkey=poq82f01jen6u3t005689ge93&st=4u6t330l&dl=1"
    fh, _ = urlretrieve(url)
    print(f"Downloaded weights file: {fh}, Size: {os.path.getsize(fh)} bytes")
    
    checkpoint = torch.load(fh, map_location="cpu")
    state_dict = checkpoint['state_dict'] 
    
    backbone_state_dict = {k.replace("backbone.", ""): v for k, v in state_dict.items() if not k.startswith("projector.")}
    model = resnet18(pretrained=False)
    model.load_state_dict(backbone_state_dict, strict=False)


    preprocessing = functools.partial(load_preprocess_images, image_size=224)

    activations_model = PytorchWrapper(identifier='barlow_twins_custom', model=model, preprocessing=preprocessing)

    
    return ModelCommitment(
        identifier='barlow_twins_custom',
        activations_model=activations_model,
        layers=['layer1', 'layer2', 'layer3', 'layer4', 'avgpool']
    )

def get_model_list():
    return ['barlow_twins_custom']

# Specify layers to test
def get_layers(name):
    assert name == 'barlow_twins_custom'
    return ['layer1', 'layer2', 'layer3', 'layer4', 'avgpool']

def get_bibtex(model_identifier):
    return """
    @misc{resnet18_test_consistency,
    title={ArtResNet18 Barlow Twins},
    author={Claudia Noche},
    year={2024},
    }
    """

if __name__ == '__main__':
    from brainscore_vision.model_helpers.check_submission import check_models
    check_models.check_base_models(__name__)
