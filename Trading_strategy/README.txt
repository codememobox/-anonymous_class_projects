1. indicators.py 
- This file contains the functions to acquire the indicators for strategies. 
- strategy will first use get_price to get the normalized price.
- The sma, BBP, momentum, MACD fucntions with normalized price as parameter will give the according indicator values.

2. marketsimcode.py
- This file contains the market simulator take in trascation dataframe. 
- Manual Strategy, experiment1, experiment2 will give trascation dataframe input to compute_portvals() and return the according portfolio values.

3. RTLearner.py
- This file contains Random Tree classification. 

4. BagLearner.py
- This file contains the BagLearner use RTLearner from RTLearner.py
- StrategyLearner will give bags size and leaf size inside it's add_evidence() method to BagLearner, and call add_evidence() and query() from this file.

5.ManualStrategy.py
- This file contains methods produce in-sample and out-sample output and graphs by setting different parameters.
- This file contains testPolicy() method: indicators' condition for buy or sell signals are in side this method, and will return trading dataframe.
- This file contains benchMark() method: return return trading dataframe
- This file contains port_stats() method: return the statistic values for portfolios, this method will be called by experiment1 and experiment2.
- This file contains compareManual() method(): with parameter symbol,sd,ed,sv,sample: it will give the portfolio values and the graphs for manual 
strategy portfolio and benchmark. 

6. StrategyLearner.py
- This file contains methods to preduce trades dataframe for strategy learner.
- This file contains add_evidence() method: it will calculate indicators by call functions from indicators.py
and call add_evidence() from BagLearner.py
- This file contains testPolicy() method: it will call query()from BagLearner.py

7. experiment1.py
- This file produce the graph and statistics for comparision of: Strategy Learner, Manual Strategy and benchmark.
- This file will call functions and methods from marketsimcode.py, ManualStrategy.py and StrategyLearner.py
- If run this file in the environment, the graph will be saved as png, and statistic ouput will be printed at console.

8. experiment2.py
- This file produce the graph and statistics for comparision of: Strategy Learner with different impact 0, 0.002, 0.005, 0.007 and commission 0
- This file will call functions and methods from marketsimcode.py, and StrategyLearner.py
- If run this file in the environment, the graph will be saved as png, and statistic ouput will be printed at console.


9. testproject.py 
- This file contains all the necessary calls produce the neccessary graphs save as png and statistic output for the report.
- By run PYTHONPATH=../:. python testproject.py