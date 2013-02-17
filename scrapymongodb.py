# Copyright 2011 Julien Duponchelle <julien@duponchelle.info>.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""MongoDB Pipeline for scrapy"""

import pymongo
from scrapy.conf import settings
from scrapy import log

MONGODB_SAFE = False
MONGODB_ITEM_ID_FIELD = "_id"

class MongoDBPipeline(object):
    def __init__(self):
        connection = pymongo.Connection(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        self.db = connection[settings['MONGODB_DB']]
        self.collection = self.db[settings['MONGODB_COLLECTION']]
        self.uniq_key = settings.get('MONGODB_UNIQ_KEY', None)
        self.itemid = settings.get('MONGODB_ITEM_ID_FIELD', 
            MONGODB_ITEM_ID_FIELD)
        self.safe = settings.get('MONGODB_SAFE', MONGODB_SAFE)

        if isinstance(self.uniq_key, basestring) and self.uniq_key == "":
            self.uniq_key = None
            
        if self.uniq_key:
            self.collection.ensure_index(self.uniq_key, unique=True)

    def process_item(self, item, spider):
        if self.uniq_key is None:
            result = self.collection.insert(dict(item), safe=self.safe)
        else:
            result = self.collection.update(
                            {self.uniq_key: item[self.uniq_key]},
                            dict(item),
                            upsert=True, safe=self.safe)

        # If item has _id field and is None
        if self.itemid in item.fields and not item.get(self.itemid, None):
            item[self.itemid] = result

        log.msg("Item %s wrote to MongoDB database %s/%s" %
                    (result, settings['MONGODB_DB'], 
                    settings['MONGODB_COLLECTION']),
                    level=log.DEBUG, spider=spider)  
        return item
