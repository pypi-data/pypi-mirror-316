# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import Sequence

from hidet.graph.tensor import Tensor
from hidet.runtime.compiled_app import CompiledApp


class ImageClassificationApp:
    def __init__(self, compiled_app: CompiledApp):
        super().__init__()
        self.compiled_app: CompiledApp = compiled_app

    def classify(self, input_images: Sequence[Tensor]):
        return self.compiled_app.graphs["image_classifier"].run_async(input_images)
