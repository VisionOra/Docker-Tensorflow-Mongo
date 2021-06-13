#!/usr/bin/env python
# coding: utf-8

# In[3]:


from utils import predict


# # Looping through Mongo DB

# In[7]:


import os
import pymongo
import time



connectionString = "mongodb://192.168.18.4:27017/model_requests";
client = pymongo.MongoClient(connectionString)
db    = client.model_requests #test is my database
col   = db.req #Here spam is my collection
        

def start_processing():
    global col
    
    while True:
        try:
            # Querying to db
            array = col.find_one({ "results" : { "$exists": False } })

            # Getting values from db
            _id     = array["_id"]
            request = array["request_id"]
            base_64 = array["base64"]


            # Predicting Image
            st_time = time.time()
            image   = predict(base_64)
            col.update({"_id":_id},{"$set":{"results":image}})
            print(f"Request processed in {time.time()-st_time}")
        # Passes None Type error means no entry to process
        except TypeError as e:
            time.sleep(2)

        except StopIteration as e:
            col.update({"_id":_id},{"$set":{"results":"Exception Occured"}})
            time.sleep(1)


# In[ ]:


start_processing()


# In[ ]:




