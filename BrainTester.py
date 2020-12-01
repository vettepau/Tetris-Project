"""
BrainTester - Possibly include this file to test our brain and implement machine learning

I ran out of time however this would have been the class to run and test the brain while adjusting the variables seen in
the rate function of the brain. Over time it would find the optimized values for the best score
"""

import JBrainTetris
import importlib as lib

avg_score = 0
for i in range(5):
    x = JBrainTetris.scoreReturn()
    avg_score += x


avg_score = avg_score / 5
print(avg_score)

#lib.reload(JBrainTetris)
