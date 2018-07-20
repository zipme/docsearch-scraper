"""AlgoliaHelper
Wrapper on top of the AlgoliaSearch API client"""

from algoliasearch import algoliasearch
from builtins import range
from urlparse import urlparse

class AlgoliaHelper:
    """AlgoliaHelper"""
    def __init__(self, app_id, api_key, index_name, settings, query_rules, replace_domain=None):
        self.algolia_client = algoliasearch.Client(app_id, api_key)
        self.index_name = index_name
        self.index_name_tmp = index_name + '_tmp'
        self.algolia_index = self.algolia_client.init_index(self.index_name)
        self.algolia_index_tmp = self.algolia_client.init_index(self.index_name_tmp)
        self.algolia_client.delete_index(self.index_name_tmp)
        self.algolia_index_tmp.set_settings(settings)
        self.replace_domain = replace_domain

        if len(query_rules) > 0:
            self.algolia_index_tmp.batch_rules(query_rules, True, True)

    def update_domain(self, url, domain):
      return urlparse(url)._replace(netloc=domain).geturl()

    def add_records(self, records, url, from_sitemap):
        """Add new records to the temporary index"""
        record_count = len(records)
        if self.replace_domain is not None:
          for record in records:
            record['url'] = self.update_domain(record['url'], self.replace_domain)
            record['url_without_variables'] = self.update_domain(record['url_without_variables'], self.replace_domain)
            record['url_without_anchor'] = self.update_domain(record['url_without_anchor'], self.replace_domain)

        for i in range(0, record_count, 50):
            self.algolia_index_tmp.add_objects(records[i:i + 50])

        color="96" if from_sitemap else "94"

        print("\033["+color+"m> DocSearch: \033[0m" + url + " (\033[93m" + str(record_count) + " records\033[0m)")

    def add_synonyms(self, synonyms):
        synonyms_list = []
        for key, value in synonyms.iteritems():
            synonyms_list.append(value)

        self.algolia_index_tmp.batch_synonyms(synonyms_list)
        print("\033[94m> DocSearch: \033[0m" + "Synonyms" + " (\033[93m" + str(len(synonyms_list)) + " synonyms\033[0m)")

    def commit_tmp_index(self):
        """Overwrite the real index with the temporary one"""
        # print("Update settings")
        self.algolia_client.move_index(self.index_name_tmp, self.index_name)

    def report_crawling_issue(self):
        self.algolia_index.set_settings({
            'userData': {
                'crawling_issue': True
            }
        })