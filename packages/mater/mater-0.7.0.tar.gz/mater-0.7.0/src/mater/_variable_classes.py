"""This module"""

from dataclasses import dataclass

import pandas as pd


@dataclass
class Parameter:
    """This a Parameter dataclass to list all the inputs and parameters needed to perform a simulation with the MATER framework

    :param run_name: Name of the scenario to simulate. It will create a new directory in your working directory containing all the output data in `Parquet <https://parquet.apache.org/docs/overview/>`_ files.
    :type params: str
    :param simulation_start_time: The simulation initial time. It needs to be at least one step above the minimal time value of the input data
    :type params: int
    :param simulation_end_time: The simulation final time
    :type params: int
    :param init_non_exo_in_use_stock: Used to initialize the in-use stock value for non exogenously controlled object (endogenously controlled and free objects). The unit is object dependant but has to be consistent with al the other inputs.
    :type params: pd.DataFrame
    :param exogenous_stock: The exogenous reference stock of objects. It can be a random sceanrio for cars or 0 for steel as we want to product just what is consummed at each time step.
    :type params: pd.DataFrame
    :param lifetime_mean_value: The mean value of a log normal distribution for the survival function.
    :type params: pd.DataFrame
    :param lifetime_standard_deviation: The standard deviation of a log normal distribution for the survival function.
    :type params: pd.DataFrame
    :param object_composition: The material intensity of a product (the model does not manage cascade composition yet, e.g. car --> chassis --> steel --> iron)
    :type params: pd.DataFrame
    :param control_flow_shares: The link between the origin process and the controlled production flow. (e.g. The process "steel production" is linked to the production flow of steel).
    :type params: pd.DataFrame
    :param collection_rate: The share of object arriving at their end of life at a given time step that will be actually collected and sent to recycling.
    :type params: pd.DataFrame
    :param recycling_rate: The quantity of material recycled from a product material composition. It includes a downgrading aspect to model the loss of quality of a material in the recycling process (e.g. from high alloyed steel to low alloyed steel).
    :type params: pd.DataFrame
    :param recycling_flow_shares: The link between the origin process and the recycling flow. (e.g. The process "car recycling" is linked to the recycling flow of cars).
    :type params: pd.DataFrame
    :param process_shares: The link between a process and the in-use stock of an object (e.g. The process "steel production is made at X% by blast furnace and Y% by electric arc furnace).
    :type params: pd.DataFrame
    :param process_max_capacity: The max capacity of process per object per time (e.g. 1MW of wind turbine could produce 1MW x 365d x 24h x 3600s = 31,536TJ per year at maximum capacity with a yield factor of 1).
    :type params: pd.DataFrame
    :param process_reference_capacity: The yield factor of a process capacity (e.g. A wind turbine has a yield factor of 0,3. So 1MW installed produces only 31,536TJ x 0,3 = 9,4608TJ in a year).
    :type params: pd.DataFrame
    :param thermodynamic_process: The link between the destination process and the extraneous flow. (e.g. The process "steel production" is linked to the consumption of iron, and heat).
    :type params: pd.DataFrame
    :param object_efficiency: Efficiency (technological efficiency rate and object conversion) of an object to produce a process. (e.g. The heat consumed by the blast furnace when performing the "steel production" process is made by the combustion of coke and that produces CO2) That way it is possible to model two different technologies that produce the same process with a common thermodynamic recepe but convert it in different inputs depending on the technology.
    :type params: pd.DataFrame
    :param control_flow_trade: A bilateral IO matrix to model the regional flows for each object.
    :type params: pd.DataFrame
    """

    run_name: str
    simulation_start_time: int
    simulation_end_time: int
    init_non_exo_in_use_stock: pd.DataFrame
    exogenous_stock: pd.DataFrame
    lifetime_mean_value: pd.DataFrame
    lifetime_standard_deviation: pd.DataFrame
    object_composition: pd.DataFrame
    control_flow_shares: pd.DataFrame
    collection_rate: pd.DataFrame
    recycling_rate: pd.DataFrame
    recycling_flow_shares: pd.DataFrame
    process_shares: pd.DataFrame
    process_max_capacity: pd.DataFrame
    process_reference_capacity: pd.DataFrame
    thermodynamic_process: pd.DataFrame
    object_efficiency: pd.DataFrame
    control_flow_trade: pd.DataFrame

    # def check_param(self):
    #     # ToDo
    #     # check the multiindex of each input parameter
    #     logging.info("Todo: check the multiindex of each input parameter")
