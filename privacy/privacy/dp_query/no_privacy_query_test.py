# Copyright 2019, The TensorFlow Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for NoPrivacyAverageQuery."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl.testing import parameterized
import tensorflow as tf

from privacy.dp_query import no_privacy_query
from privacy.dp_query import test_utils


class NoPrivacyQueryTest(tf.test.TestCase, parameterized.TestCase):

  def test_sum(self):
    with self.cached_session() as sess:
      record1 = tf.constant([2.0, 0.0])
      record2 = tf.constant([-1.0, 1.0])

      query = no_privacy_query.NoPrivacySumQuery()
      query_result, _ = test_utils.run_query(query, [record1, record2])
      result = sess.run(query_result)
      expected = [1.0, 1.0]
      self.assertAllClose(result, expected)

  def test_no_privacy_average(self):
    with self.cached_session() as sess:
      record1 = tf.constant([5.0, 0.0])
      record2 = tf.constant([-1.0, 2.0])

      query = no_privacy_query.NoPrivacyAverageQuery()
      query_result, _ = test_utils.run_query(query, [record1, record2])
      result = sess.run(query_result)
      expected = [2.0, 1.0]
      self.assertAllClose(result, expected)

  def test_no_privacy_weighted_average(self):
    with self.cached_session() as sess:
      record1 = tf.constant([4.0, 0.0])
      record2 = tf.constant([-1.0, 1.0])

      weights = [1, 3]

      query = no_privacy_query.NoPrivacyAverageQuery()
      query_result, _ = test_utils.run_query(
          query, [record1, record2], weights=weights)
      result = sess.run(query_result)
      expected = [0.25, 0.75]
      self.assertAllClose(result, expected)

  @parameterized.named_parameters(
      ('type_mismatch', [1.0], (1.0,), TypeError),
      ('too_few_on_left', [1.0], [1.0, 1.0], ValueError),
      ('too_few_on_right', [1.0, 1.0], [1.0], ValueError))
  def test_incompatible_records(self, record1, record2, error_type):
    query = no_privacy_query.NoPrivacySumQuery()
    with self.assertRaises(error_type):
      test_utils.run_query(query, [record1, record2])


if __name__ == '__main__':
  tf.test.main()
