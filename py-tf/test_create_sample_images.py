import pytest
import create_sample_images
import numpy as np

# $ python create_sample_images.py [-n <cores>] [-v] [-val <%>] [-e <%>] [-p] [-x <width>] [-y <height>] [-o <dir>] [-i <dir>] N
class TestArgParsing:
    """Tests combinations of input arguments to make sure the parser works as expected"""
    def test_one(self):
        cmd = "python create_sample_images.py -n 4 -val 20.0 -p -x 128 1000"
        args = cmd.split(' ')[2:]
        parsed = create_sample_images.get_args(args)

        assert parsed.samples == 1000
        assert parsed.val == 20.0
        assert parsed.empty == 50.0
        assert parsed.width == 128
        assert parsed.height == 256
        assert parsed.permute == True
        assert parsed.output == './data'
        assert parsed.input == './samples'
        assert parsed.v == False
        assert parsed.n == 4
    
    def test_two(self):
        cmd = "python create_sample_images.py -v -e 25 -x 512 -y 512 -o ./dir_name 2000"
        args = cmd.split(' ')[2:]
        parsed = create_sample_images.get_args(args)

        assert parsed.samples == 2000
        assert parsed.val == 10.0
        assert parsed.empty == 25.0
        assert parsed.width == 512
        assert parsed.height == 512
        assert parsed.permute == False
        assert parsed.output == './dir_name'
        assert parsed.input == './samples'
        assert parsed.v == True
        assert parsed.n == 1

class TestDistribution:
    def compute(self, N, e, n, m, k):
        assert e >= 0 and e <= 1
        assert k >= 0 and k <= 1

        d = (N * e) / (n * (1-k) + m * k)

        pn = N * (1 - e) / n + (1 - k) * d
        pm = k * d

        pn = round(pn)
        pm = round(pm)

        return (pn, pm)

    def test_one(self):
        N = 1000
        e = 50.0 / 100.0
        n = 5
        m = 2
        k = 0.5
        
        pn, pm = self.compute(N, e, n, m, k)

        print(f"pn = {pn}, pm = {pm}")

        assert abs(n * pn + m * pm - N) < 5
    
    def test_two(self):
        N = 2000
        e = 70.0 / 100.0
        n = 3
        m = 3
        k = 0.7
        
        pn, pm = self.compute(N, e, n, m, k)

        print(f"pn = {pn}, pm = {pm}")

        assert abs(n * pn + m * pm - N) < 5