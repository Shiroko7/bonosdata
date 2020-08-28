import numpy as np
from datetime import date


start_date = date(2020, 1, 5)
end_date = date(2020, 4, 6)

print(np.busday_count(np.datetime64(start_date), np.datetime64(end_date)))
