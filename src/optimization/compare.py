from src.model.inference import generate
from src.model.context import find_policy
q='What are the working hours?';context=find_policy(q)
for optimized in (False,True):
    print('optimized=',optimized,generate(q,context,optimized=optimized))
