# Copyright 2020 Google LLC
#
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
# ==============================================================================
"""Tests for lit_nlp.components.ablation_flip."""

from collections.abc import Callable

from absl.testing import absltest
from absl.testing import parameterized
from lit_nlp.api import dataset as lit_dataset
from lit_nlp.api import model as lit_model
from lit_nlp.api import types
from lit_nlp.components import ablation_flip
from lit_nlp.lib import testing_utils

INPUT_SPEC_SPARSE_MULTI = {'input': types.SparseMultilabel()}
INPUT_SPEC_TEXT = {'input': types.TextSegment()}
INPUT_SPEC_URL = {'input': types.URL()}

_RegressionModelForTesting = testing_utils.RegressionModelForTesting


class _ClassificationTestModel(testing_utils.ClassificationModelForTesting):

  def __init__(self, input_spec: types.Spec):
    self._input_spec = input_spec

  def input_spec(self) -> types.Spec:
    return self._input_spec


class _BadOutputTestModel(_ClassificationTestModel):

  def output_spec(self) -> types.Spec:
    return {}


class AblationFlipTest(parameterized.TestCase):

  def setUp(self):
    super(AblationFlipTest, self).setUp()
    self.ablation_flip = ablation_flip.AblationFlip()

  @parameterized.named_parameters(
      ('cls_sparse', _ClassificationTestModel, INPUT_SPEC_SPARSE_MULTI, True),
      ('cls_text', _ClassificationTestModel, INPUT_SPEC_TEXT, True),
      ('cls_url', _ClassificationTestModel, INPUT_SPEC_URL, True),
      ('cls_none', _ClassificationTestModel, {}, False),
      ('reg_sparse', _RegressionModelForTesting, INPUT_SPEC_SPARSE_MULTI, True),
      ('reg_text', _RegressionModelForTesting, INPUT_SPEC_TEXT, True),
      ('reg_url', _RegressionModelForTesting, INPUT_SPEC_URL, True),
      ('reg_none', _RegressionModelForTesting, {}, False),
      ('bad_sparse', _BadOutputTestModel, INPUT_SPEC_SPARSE_MULTI, False),
      ('bad_text', _BadOutputTestModel, INPUT_SPEC_TEXT, False),
      ('bad_url', _BadOutputTestModel, INPUT_SPEC_URL, False),
      ('bad_none', _BadOutputTestModel, {}, False),
  )
  def test_ablation_flip_is_compatible(self,
                                       model_ctr: Callable[[types.Spec],
                                                           lit_model.Model],
                                       input_spec: types.Spec,
                                       exp: bool):
    model = model_ctr(input_spec)
    compatible = self.ablation_flip.is_compatible(
        model, lit_dataset.NoneDataset({'test': model}))
    self.assertEqual(compatible, exp)

if __name__ == '__main__':
  absltest.main()
