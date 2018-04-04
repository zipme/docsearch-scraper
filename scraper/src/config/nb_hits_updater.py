from ..helpers import confirm
import json
import copy
from collections import OrderedDict


class NbHitsUpdater(object):
    new_nb_hit = None
    previous_nb_hits = None
    config_file = None
    config_content = None

    def __init__(self, config_file, config_content, previous_nb_hits, new_nb_hit):
        self.config_file = config_file
        self.config_content = copy.deepcopy(config_content)
        self.new_nb_hit = new_nb_hit
        self.previous_nb_hits = previous_nb_hits

    def update(self):
        if self._update_needed():
            print("previous nb_hits: " + str(self.previous_nb_hits) + "\n")

            if confirm('Do you want to update the nb_hits in ' + self.config_file + ' ?'):
                try:
                    self._update_config()
                    print("\n[OK] " + self.config_file + " has been updated")
                except Exception:
                    print("\n[KO] " + "Was not able to update " + self.config_file)

    def _update_needed(self):
        return self.previous_nb_hits is None or self.previous_nb_hits != self.new_nb_hit

    def _update_config(self):
        self.config_content['nb_hits'] = self.new_nb_hit
        self.config_content = OrderedDict(
            sorted(self.config_content.items(), key=self.key_sort))

        with open(self.config_file, 'w') as f:
            f.write(json.dumps(self.config_content, indent=2, separators=(',', ': ')))

    def key_sort(self, attr):
        ref = {
            "index_name": 0,
            "start_urls": 1,
            "sitemap_urls": 2,
            "sitemap_urls_regexs": 3,
            "stop_urls": 4,
            "force_sitemap_urls_crawling": 5,
            "strict_redirects": 6,
            "selectors": 7,
            "selectors_exclude": 8,
            "stop_content": 9,
            "strip_chars": 10,
            "keep_tags": 11,
            "min_indexed_level": 12,
            "only_content_level": 13,
            "js_render": 14,
            "js_wait": 15,
            "use_anchors": 16,
            "custom_settings": 17,
            "synonyms": 18,
            "docker_memory": 19,
            "docker_cpu": 20,
            "conversation_id": 28,
            "comments": 29,
            "nb_hits": 30
        }
        if attr[0] in ref.keys():
            return ref[attr[0]]
        else:
            return 27
