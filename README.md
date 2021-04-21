# FireEmblem3HousesGardening
a simple tool to derive good combination for gardening in Fire Emblem: Three Houses

# How to Use
run 
```
python fireemblem_gardening.py <max #. of seeds> <score> <file to dump result to>
```

e.g.
`python .\fireemblem_gardening.py .\fire_emblem.json 5 70 result.txt`

would derive all the combinations that requires at most 5 seeds and can give result score of at least 70.

# Configuration
configure `required_seeds` section to specify the required types of seeds. e.g.
```
"required_seeds": [
        ["mixed_herb"],
        ["Albinean", "angelica"]
    ],
```
means only combinations with 0. required_seeds or 1. both Albinean and angelica would be listed.

configure `pool` to specify what seeds do you have in your inventory.

# Reference and Thanks
for the formulae, this detailed [article](https://serenesforest.net/three-houses/monastery/greenhouse) is referenced.