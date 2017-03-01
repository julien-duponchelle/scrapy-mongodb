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

import logging
import pymongo
import six

MONGODB_ITEM_ID_FIELD = "_id"

logger = logging.getLogger(__name__)


class MongoDBPipeline(object):
    def __init__(self, mongodb_server, mongodb_port, mongodb_db, mongodb_collection, mongodb_uniq_key,
                 mongodb_item_id_field):
        connection = pymongo.MongoClient(mongodb_server, mongodb_port)
        self.mongodb_db = mongodb_db
        self.db = connection[mongodb_db]
        self.mongodb_collection = mongodb_collection
        self.collection = self.db[mongodb_collection]
        self.uniq_key = mongodb_uniq_key
        self.item_id = mongodb_item_id_field

        if isinstance(self.uniq_key, six.string_types) and self.uniq_key == "":
            self.uniq_key = None

        if self.uniq_key:
            self.collection.ensure_index(self.uniq_key, unique=True)

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(settings.get('MONGODB_SERVER', 'localhost'), settings.get('MONGODB_PORT', 27017),
                   settings.get('MONGODB_DB', 'scrapy'), settings.get('MONGODB_COLLECTION', None),
                   settings.get('MONGODB_UNIQ_KEY', None), settings.get('MONGODB_ITEM_ID_FIELD', MONGODB_ITEM_ID_FIELD))

    def process_item(self, item, spider):
        if self.uniq_key is None:
            result = self.collection.insert_one(dict(item))
        else:
            result = self.collection.update_one({self.uniq_key: item[self.uniq_key]}, {'$set': dict(item)},
                                                upsert=True)

        # If item has _id field and is None
        if self.item_id in item.fields and not item.get(self.item_id, None):
            item[self.item_id] = result

        logger.debug("Item %s wrote to MongoDB database %s/%s, spider: %s" % (
            result.inserted_id, self.mongodb_db, self.mongodb_collection, spider.name))
        return item
