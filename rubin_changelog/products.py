import logging

from .config import TARGET_DIR, PRODUCT_SKIPLIST, EXTRA_TAGS
from .repos_yaml import ReposYaml
from .repository import Repository

class Products(object):
    def __init__(self):
        self._repos_yaml = ReposYaml()
        self._products = {}

    def __getitem__(self, product_name: str) -> Repository:
        if product_name in PRODUCT_SKIPLIST:
            raise KeyError(f"{product_name} is skip-listed")
        if product_name not in self._products:
            logging.debug(f"Materializing {product_name}")
            self._products[product_name] = Repository.materialize(
                self._repos_yaml[product_name]["url"],
                TARGET_DIR,
                branch_name=self._repos_yaml[product_name].get("ref", "master"),
            )
            if product_name in EXTRA_TAGS:
                for tag_name, target in EXTRA_TAGS[product_name]:
                    self._products[product_name].add_tag(tag_name, target)
        return self._products[product_name]

products = Products()
