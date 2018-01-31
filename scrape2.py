#!/usr/bin/env python3

import json
import logging as log
import os
import os.path
import re
import sys

from lxml.html import fromstring
import requests

from constants import Constants

def fixText(text):
    if text:
        # replace xml tags
        # copy bold/italic to reddit?
        # text = re.sub(r"</?b+>", '**', text)
        # text = re.sub(r"</?i+>", '*', text)
        # remove unwanted symbols and chars from card text
        # replace multiple spaces
        text = re.sub(r"[ ]{2,}", ' ', text)
        text = text.replace('\xa0', ' ')
        text = text.replace('[[Shiv|S]][[shiv|hiv]]', 'Shiv')
        text = text.replace('[[Poison|P]][[poison|oison]]', 'Poison')
        text = text.replace('[[Weak|W]][[weak|eak]]', 'Weak')
        text = text.replace('[[Vulnerable|V]][[vulnerable|ulnerable]]', 'Vulnerable')
        text = text.replace('[[Block|B]][[block|lock]]', 'Block')
        text = text.replace('[[Block|Bl]][[block|ock]]', 'Block')
        text = text.replace('[[Dexterity|D]][[dexterity|exterity]]', 'Dexterity')
        text = text.replace('[[Poison|Poisoned]]', 'Poisoned')
        text = text.replace('[[Ironclad]]', 'Ironclad')
        text = text.replace('[[Silent]]', 'Silent')
        text = text.replace('[[Map locations|? rooms]]', '? rooms')
        text = text.replace('[[Rest site|Rest Sites]]', 'Rest Sites')
        text = text.replace('[[Rest site|Rest Site]]', 'Rest Site')
        text = text.replace('[[Rest site|rest]]', 'rest')
        text = text.replace('[[Rest site|Rest]]', 'rest')
        text = text.replace('[[Chest|chest]]', 'chest')
        text = text.replace('[[Potions|potions]]', 'potions')
        text = text.replace('[[Potions|potion]]', 'potion')
        text = text.replace('[[Necronomicurse|Cursed]]', 'Cursed')
        text = text.replace('[[Merchant|shops]]', 'shops')
        text = text.replace('[[', '')
        text = text.replace(']]', '')
        text = text.strip()

    return text

def main():
    silent_cards = {}
    r = requests.get("https://slay-the-spire.wikia.com/api.php?action=query&format=json&prop=revisions&rvprop=content&pageids=88")
    data = r.json()
    content = fixText(data['query']['pages']['88']['revisions'][0]['*'])
    cards_info = content.split('|-')
    cards_info = cards_info[1:]
    for card in cards_info:
        card_info = card.split('\n|')
        silent_cards[card_info[1]] = {
                'Rarity' : card_info[3],
                'Type' : card_info[4],
                'Energy' : card_info[5],
                'Description' : card_info[6].replace('\n', '')
        }
    ironclad_cards = {}
    r = requests.get("https://slay-the-spire.wikia.com/api.php?action=query&format=json&prop=revisions&rvprop=content&pageids=92")
    data = r.json()
    content = fixText(data['query']['pages']['92']['revisions'][0]['*'])
    cards_info = content.split('|-')
    cards_info = cards_info[1:]
    for card in cards_info:
        card_info = card.split('\n|')
        ironclad_cards[card_info[1]] = {
                'Rarity' : card_info[3],
                'Type' : card_info[4],
                'Energy' : card_info[5],
                'Description' : card_info[6].replace('\n', '')
        }
    neutral_cards = {}
    r = requests.get("https://slay-the-spire.wikia.com/api.php?action=query&format=json&prop=revisions&rvprop=content&pageids=96")
    data = r.json()
    content = fixText(data['query']['pages']['96']['revisions'][0]['*'])
    groups = content.split('}')
    cards_info = groups[0].split('|-')
    cards_info = cards_info[1:]
    for card in cards_info:
        card_info = card.split('\n|')
        #print(card_info)
        neutral_cards[card_info[1]] = {
                'Rarity' : card_info[3],
                'Type' : card_info[4],
                'Energy' : card_info[5],
                'Description' : card_info[6].replace('\n', '')
        }
    curse_cards = {}
    cards_info = groups[1].split('|-')
    cards_info = cards_info[1:]
    for card in cards_info:
        card_info = card.split('\n|')
        curse_cards[card_info[1]] = {
                'Type' : card_info[3],
                'Description' : card_info[4].replace('\n', '')
        }
    status_cards = {}
    cards_info = groups[2].split('|-')
    cards_info = cards_info[1:]
    for card in cards_info:
        card_info = card.split('\n|')
        status_cards[card_info[1]] = {
                'Type' : card_info[3],
                'Description' : card_info[4].replace('\n', '')
        }

    r = requests.get("https://slay-the-spire.wikia.com/api.php?action=query&format=json&prop=revisions&rvprop=content&pageids=104")
    data = r.json()
    content = fixText(data['query']['pages']['104']['revisions'][0]['*'])
    relics = {}
    relics_info = content.split('|-')
    for relic in relics_info[1:]:
        relic_info = relic.split('\n|')
        relics[relic_info[2]] = {
                'Rarity' : relic_info[3],
                'Description' : relic_info[4].replace('\n', '')
        }
    
    all_items = silent_cards.copy()
    all_items.update(ironclad_cards)
    all_items.update(neutral_cards)
    all_items.update(curse_cards)
    all_items.update(status_cards)
    all_items.update(relics)
    with open('data/items.json', 'w') as out:
        json.dump(all_items, out, sort_keys=True, indent=4)
        
    
main()
