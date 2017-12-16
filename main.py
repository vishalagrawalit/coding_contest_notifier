"""

If you want to see the latest running contest or the recent upcoming contest,
then run this script.

Otherwise you can run respective websites script and get all the running contests & all the upcoming contest of that
respective website.

"""


from codeforces import fetch_codeforces
from codechef import fetch_codechef
import time

fetch_codechef()
time.sleep(10)
fetch_codeforces(0)
