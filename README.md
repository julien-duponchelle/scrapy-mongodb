Description
===========
It's a pipeline which allow you to store scrapy items in MongoDB database.

Install
=======
1) pip install pymongo
2) copy mongodb.py to pipelines directory in your scrapy directory
3) Configure your settings.py:

  ITEM_PIPELINES = [
      'testscrapy.pipelines.mongodb.MongoDBPipeline',
  ]

  MONGODB_SERVER = 'localhost'
  MONGODB_PORT = 27017
  MONGODB_DB = 'scrapy'
  MONGODB_COLLECTION = 'items'
  MONGODB_UNIQ_KEY = 'url'

Licence
=======
Copyright 2011 Julien Duponchelle

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.