# Introduction

I am going to deploy a model on docker and I decided to not make an api but an artitecture in which I can use 2 docker images 1 is for mongo and other is for tensorflow model just for practice. So the artitecture is 

1.  Image and request id is inserted to the mongo db which is running inside a docker container
2.  A python file which is main file of our model is continously listing for a triger of insertion
   when ever a request is inserted into a mongo database. 
   
   * Main convert the base64 image to the PIL or numpy object
   * Run model predictions on the Image
   * Save results back in mongo against the same request id.
   
   
So lets get started with the artitecture


Python notebook from which we can make a request for prediction
[Notebook](./mongo_connection.ipynb) 

# Setup mongo Docker Container

> For this you need to setup a docker ce first on your machine so that you can easily run docker thing on your machine

run this command to pull latest mongo image and for running the container at the same time

```bash
sudo docker run -d -p 27017-27019:27017-27019 --name mongodb mongo
```

**Flags description**

* -d: detach mongo image. other wise your teminal is booked by this image and only show the mongo container outputs
* -p: For Exposing ports
* --name: to give a name to an image while running emm like alise
* mongo: its the original name of our image which is pulled from docker registry and than run on our local machine

Okay now your docker container is in running state lets add some testing sample into the mongodb so that we can test with our python files.

Lets get inside the docker image with this command to insert some values

```bash
sudo docker exec -it mongodb bash
```

**Flags description**
* exec: to execute a command on container startup (by defualt it runs a command configure in your .docker file)
* -i: For interaction session
* -t: opens a tty 
* mongodb: Name(alise) of our image
* bash: It is the command to execute

Go into the mongo after getting inside the container

```bash
mongo
```

> Okay I hope everything go goods. if you get anyerror feel free to raise an issue on github I will try to solve it as soon as possible

**Lets create a datebase now**

```mongo
use model_requests
```
where model_requests is my database name.

Lets insert something into our brand new database
```mongo
db.req.save({"request":12343, "Image":"asdfeewfdsdfe"})
db.req.save({"request":12342, "Image":"ok connected"})
```
Ok so now we have some entries in our collection lets make a query to find them

```mongo
db.req.find({"request":12343})
```
After running the query You can get some results like this
```mongo
{ "_id" : ObjectId("60c4ef75dd0bb78ad0828b89"), "request" : 12343, "Image" : "asdfeewfdsdfe" }

```

yaaayyy we are done in setting up our mongo docker!
> shhuuu thats easy

# Connect Mongo Docker Container
Now lets connect our mongo database with our Notebook which is outside the container.  [Notebook](./mongo_connection.ipynb) 




# Author 

* Sohaib Anwaar
* gmail          : sohaibanwaar36@gmail.com
* linkedin       : [Have Some Professional Talk here](https://www.linkedin.com/in/sohaib-anwaar-4b7ba1187/)
* Stack Overflow : [Get my help Here](https://stackoverflow.com/users/7959545/sohaib-anwaar)
* Kaggle         : [View my master-pieces here](https://www.kaggle.com/sohaibanwaar1203)

# Helping Material

* Google
* Docker Documentation
* Tensorflow Documentation
* Stack-overflow
* [Super Resolution model Github](https://github.com/SohaibAnwaar/super_resolution.git)