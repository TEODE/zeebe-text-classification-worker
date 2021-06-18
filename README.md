Zeebe Text Classification Worker
================================

A [Zeebe](https://zeebe.io) text classifier worker based on [Hugging Face](https://huggingface.co/) NLP pipeline

Configure
---------

Set a virtual python environment for version 3.7.10 and install requirements:

```bash
pip install -r requirements.txt 
```

Specify a local (after downloading under models folder) or an [Hugging Face zero-shot classification model](https://huggingface.co/models?pipeline_tag=zero-shot-classification) in the .env file

Due to high resource consumption of some models, we decided to make this worker configurable in term of task name and associated model.
For example, so it is possible to separate tasks and models with multiple workers for language handling :

* task `text-classification-en` and model (default will be downloaded at worker startup from Hugging Face's website)
* task `text-classification-fr` and local model `models/camembert-base-xnli`
* task `text-classification-ml` and local model `models/xlm-roberta-large-xnli`

Run locally
-----------

If you have a local/docker-compose Zeebe running locally you can run/debug with:

```bash
python index.py
```

Run tests
---------

```bash
python -m unittest
```

Build with Docker
-----------------

```bash
docker build -t zeebe-text-classification-french-worker -f Dockerfile.fr .
```

Run with Docker
-----------------

You must have a local or a port-forwarded Zeebe gateway for the worker to connect then:

```bash
docker run --name zb-txt-class-fr-wkr zeebe-text-classification-french-worker
```

Usage
-----

Example BPMN with service task:

 ```xml
 <bpmn:serviceTask id="my-text-classification" name="My text classification">
   <bpmn:extensionElements>
     <zeebe:taskDefinition type="my-env-var-task-name" />
   </bpmn:extensionElements>
 </bpmn:serviceTask>
 ```

* the worker is registered for the type of your choice (set as an env var)
* required variables:
  * `sequence` - the phrase to classify
  * `candidate_labels` - the list of possible classes
* jobs are completed with variables:
  * `labels` - the list of classes (highest scores first)
  * `scores` - the list of scores sorted in descending order
