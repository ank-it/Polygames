# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import time
from typing import Iterator, Tuple, Callable, Optional, List, Dict
from pathlib import Path
import copy

import torch
import torchviz

import polygames

from ..model_zoo.utils import get_game_info
from .params import GameParams, ModelParams
from .env_creation_helpers import (
    create_model,
)


def draw_model(
    game_params: GameParams,
    model_params: ModelParams,
    out: str,
):
    m = create_model(game_params=game_params,
                     model_params=model_params)
                     
    info = get_game_info(game_params)
    model.eval()  # necessary for batch norm as it expects more than 1 ex in training
    feature_size = info["feature_size"][:3]
    action_size = info["action_size"][:3]
    input_data = torch.zeros([1] + feature_size, device=torch.device("cpu"))
    dot = torchviz.make_dot(model(input_data), params=dict(model.named_parameters()))
    dot.format = 'png'
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    dot.render(out)
