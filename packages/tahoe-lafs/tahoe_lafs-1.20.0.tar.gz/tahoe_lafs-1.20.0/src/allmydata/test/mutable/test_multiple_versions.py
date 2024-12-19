"""
Ported to Python 3.
"""

from ..common import AsyncTestCase
from testtools.matchers import Equals, HasLength
from allmydata.monitor import Monitor
from allmydata.mutable.common import MODE_CHECK, MODE_READ
from .util import PublishMixin, CheckerMixin


class MultipleVersions(AsyncTestCase, PublishMixin, CheckerMixin):

    def setUp(self):
        super(MultipleVersions, self).setUp()
        return self.publish_multiple()

    def test_multiple_versions(self):
        # if we see a mix of versions in the grid, download_best_version
        # should get the latest one
        self._set_versions(dict([(i,2) for i in (0,2,4,6,8)]))
        d = self._fn.download_best_version()
        d.addCallback(lambda res: self.assertThat(res, Equals(self.CONTENTS[4])))
        # and the checker should report problems
        d.addCallback(lambda res: self._fn.check(Monitor()))
        d.addCallback(self.check_bad, "test_multiple_versions")

        # but if everything is at version 2, that's what we should download
        d.addCallback(lambda res:
                      self._set_versions(dict([(i,2) for i in range(10)])))
        d.addCallback(lambda res: self._fn.download_best_version())
        d.addCallback(lambda res: self.assertThat(res, Equals(self.CONTENTS[2])))
        # if exactly one share is at version 3, we should still get v2
        d.addCallback(lambda res:
                      self._set_versions({0:3}))
        d.addCallback(lambda res: self._fn.download_best_version())
        d.addCallback(lambda res: self.assertThat(res, Equals(self.CONTENTS[2])))
        # but the servermap should see the unrecoverable version. This
        # depends upon the single newer share being queried early.
        d.addCallback(lambda res: self._fn.get_servermap(MODE_READ))
        def _check_smap(smap):
            self.assertThat(smap.unrecoverable_versions(), HasLength(1))
            newer = smap.unrecoverable_newer_versions()
            self.assertThat(newer, HasLength(1))
            verinfo, health = list(newer.items())[0]
            self.assertThat(verinfo[0], Equals(4))
            self.assertThat(health, Equals((1,3)))
            self.assertThat(smap.needs_merge(), Equals(False))
        d.addCallback(_check_smap)
        # if we have a mix of two parallel versions (s4a and s4b), we could
        # recover either
        d.addCallback(lambda res:
                      self._set_versions({0:3,2:3,4:3,6:3,8:3,
                                          1:4,3:4,5:4,7:4,9:4}))
        d.addCallback(lambda res: self._fn.get_servermap(MODE_READ))
        def _check_smap_mixed(smap):
            self.assertThat(smap.unrecoverable_versions(), HasLength(0))
            newer = smap.unrecoverable_newer_versions()
            self.assertThat(newer, HasLength(0))
            self.assertTrue(smap.needs_merge())
        d.addCallback(_check_smap_mixed)
        d.addCallback(lambda res: self._fn.download_best_version())
        d.addCallback(lambda res: self.assertTrue(res == self.CONTENTS[3] or
                                                  res == self.CONTENTS[4]))
        return d

    def test_replace(self):
        # if we see a mix of versions in the grid, we should be able to
        # replace them all with a newer version

        # if exactly one share is at version 3, we should download (and
        # replace) v2, and the result should be v4. Note that the index we
        # give to _set_versions is different than the sequence number.
        target = dict([(i,2) for i in range(10)]) # seqnum3
        target[0] = 3 # seqnum4
        self._set_versions(target)

        def _modify(oldversion, servermap, first_time):
            return oldversion + b" modified"
        d = self._fn.modify(_modify)
        d.addCallback(lambda res: self._fn.download_best_version())
        expected = self.CONTENTS[2] + b" modified"
        d.addCallback(lambda res: self.assertThat(res, Equals(expected)))
        # and the servermap should indicate that the outlier was replaced too
        d.addCallback(lambda res: self._fn.get_servermap(MODE_CHECK))
        def _check_smap(smap):
            self.assertThat(smap.highest_seqnum(), Equals(5))
            self.assertThat(smap.unrecoverable_versions(), HasLength(0))
            self.assertThat(smap.recoverable_versions(), HasLength(1))
        d.addCallback(_check_smap)
        return d
