# An Agent-Based Model for Assessing Agricultural Water Market Structure and Function


## Description
An agent-based model (ABM) is developed to simulate irrigation water rights leasing at  watershed scale in response to drought. The model allows for variation in farm characteristics, water rights seniority, diversion location in the watershed, differences in agent preferences and information, and alternative market frameworks. The model is used to examine the effect of drought on trading activity and gains from trade under three  market models: Bilateral trading with random matching, a “Smart Market” that actively matches bidders based on their bids and asks, and a full-information optimization trading that represents the efficient benchmark against which to assess other market models. The effect of non-pecuniary factors such as preferences for active farming versus leasing and fallowing is also simulated. The results show several patterns.  Gains from trade and market participation are largest with moderate drought severity than with either severe or weak drought. Gains from trade and trading activity are also highest when bids and offers are matched by full information optimization approach, and when senior water rights holders prefer active farming to lease and fallow. The applications presented in this paper illustrate the broad applicability of the ABM framework to water resource problems under appropriative water rights systems of the Western United States. 

### Executing program (replication of paper)

1. Download requirements into a virtual environment:
```
pip install -r requirements.txt
```
2. Locate main.py file and adjust parameters:
  * set N=500, K=100, random_seed = 3145
  * set number of cores to run on around line 81
3. Run the profit maximizing simulation:
  * Set non_pec_prefs_ind to 0
  * run main.py script
  * data outputs
  * rename data folder as "####agents_seed####_pmax"
4. Run the non_pec prefs simulation:
  * Set non_pec_prefs_ind to 2 for seniors pref farming:
  * run main.py script
  * data outputs
  * rename data folder as "####agents_seed####_10_01_nonpec" if seniors pref farming
 5. Run the random uniform prefs simulation:
  * run the "main_SM_uniform_random.py" file
  * data outputs
  * rename data folder as "####agents_seed####_U01_10" if uniform random assignment

5. Note on data management:
   * If the script is run in parallel, sometimes it writes the headers into the CSV file more than once, this will cause an error in the figure scripts. Clean before running.

5. Running the figure scripts:
   * Ensure folders are named correctly before running the figure scripts. Note that some of the profit max figure scripts run from a data folder titled "####agents_seed####".

## Corresponding Repository Authors
* jacob.gifford1@wsu.edu
  
* rb1133@uah.edu




## Publication Link
* Not available yet
## Version History

* 1.0
  - initial release for journal submission.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

## Acknowledgments
* Center for Institutional Research Computing at Washington State University
