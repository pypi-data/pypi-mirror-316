**Author: Dhivya Nagasubramanian**

**Purpose:**
The purpose of the Customer Journey Orchestration package is to seamlessly connect and track customer interactions across multiple marketing channels, enabling businesses to gain a holistic view of each customer’s experience over time. By orchestrating touchpoints across channels, the package empowers marketers to deliver personalized, timely, and relevant messages, optimize engagement, and improve customer satisfaction and loyalty. It helps create a unified, data-driven strategy for nurturing and guiding customers through their journey, ultimately driving conversions and business growth.

**Requirements packages:**

**NumPy** - Adds support for large, multi-dimensional arrays, matrices and high-level mathematical functions to operate on these arrays. <br>
**python-dateutil** - Provides powerful extensions to the standard datetime module. <br>
**dask**    - Dask is a flexible parallel computing library for analytics. See documentation for more information. <br>                            
**random**  - generate random numbers with in the set limits.  <br>
**pandas**  -  Dataframe utility. <br>


**Installation Instructions:**

pip install journey-orchestrate

**Example**

|   ID | Timestamp           | Channel     | <br>
|-----:|:--------------------|:------------| <br>
|    1 | 2024-11-18 08:00:00 | email       | <br>
|    1 | 2024-11-18 09:00:00 | sms         | <br>
|    3 | 2024-11-18 10:00:00 | app         | <br>
|    3 | 2024-11-18 11:00:00 | email       | <br>
|    5 | 2024-11-18 12:00:00 | sms         | <br>
|    5 | 2024-11-18 15:00:00 | direct mail | <br>

**Output.** <br>
1  email > sms <br>
3  app > email <br>
5  sms > direct mail <br>

For a customer journey involving multiple marketing channels through which messages were delivered, we can orchestrate and stitch together the individual journey paths for each customer, providing a cohesive view of their interactions across all touchpoints.


How to use it :
There are two main functions of this framework.

**1. customer_journey_orchestrate(data, ID, datetime,channel,join_string ,n_partitions)**

- This is the main functionionility for customer journey orchestration .
    1st parameter -  dataframe where the customer touch point exists. <br>
    2nd parameter -  ID on which data should be grouped. <br> 
    3rd parameter -  timestamp on which we should start. <br>
    4th parameter -  column on which customer journey should be orchestrated . eg: Email, Directmail, Paid display, social media, etc.<br>
    5th parameter -  Join string. for eg: '>','|',etc. if nothing is given, default is '>'.<br>
    6th parameter -  number of partitions in which dask would operate the data for sorting.<br>



**2. generate_random_data(n,nc,startdt, enddt,channel_lst,random_seed)**

- This would generate sample dataset to test the customer journey orchestrate function

   1st parameter - Number of rows to generate. <br>
   2nd parameter - Number of unique IDs you want in the dataset
   3rd parameter - Start date. <br>
   4th parameter - End date. <br>
   5th parameter - Unique Channel list : eg:['EM','SMC','PD','PS']. <br>
   6th parameter - random_seed. <br>


**How to test the package with out data ?** 

**Step1** - Run with  "generate_random_data" by passing appropriate values 

eg: df_example = generate_random_data(1000,30,"2023-01-01",'2024-10-01',['EM','Direct Mail','Paid Display','Search'],230).


**Step2** - Run the orchestrator function  customer_journey_orchestrate(data, ID, datetime,channel,join_string ,n_partitions)

eg:  customer_journey_orchestrate(df_example, 'ID', 'time','channel','>' ,2)
   