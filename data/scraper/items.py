# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CerealsItem(scrapy.Item):
    name = scrapy.Field()
    source = scrapy.Field()

    origin = scrapy.Field()
    supplier = scrapy.Field()
    cereal_type = scrapy.Field()
    potential = scrapy.Field()
    dry_yield = scrapy.Field()
    coarse_fine_diff = scrapy.Field()
    moisture = scrapy.Field()
    color = scrapy.Field()
    must_mash = scrapy.Field()
    add_after_boil = scrapy.Field()
    diastatic_power = scrapy.Field()
    max_in_batch = scrapy.Field()
    protein = scrapy.Field()
    notes = scrapy.Field()


class HopsItem(scrapy.Item):
    name = scrapy.Field()
    component = scrapy.Field()
    source = scrapy.Field()

    also_known_as = scrapy.Field()
    characteristics = scrapy.Field()
    purpose = scrapy.Field()
    alpha_acid_composition = scrapy.Field()
    beta_acid_composition = scrapy.Field()
    co_humulone_composition = scrapy.Field()
    country = scrapy.Field()
    cone_size = scrapy.Field()
    cone_density = scrapy.Field()
    seasonal_maturity = scrapy.Field()
    yield_amount = scrapy.Field()
    growth_rate = scrapy.Field()
    resistant_to = scrapy.Field()
    susceptible_to = scrapy.Field()
    storability = scrapy.Field()
    ease_of_harvest = scrapy.Field()
    total_oil_composition = scrapy.Field()
    myrcene_oil_composition = scrapy.Field()
    humulene_oil_composition = scrapy.Field()
    caryophyllene_oil = scrapy.Field()
    farnesene_oil = scrapy.Field()
    substitutes = scrapy.Field()
    style_guide = scrapy.Field()
